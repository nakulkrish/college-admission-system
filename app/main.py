import importlib
import logging
import os
import pkgutil
import re
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import init_db

logger = logging.getLogger("app")


def _import_all(package_name: str) -> list:
    """Imports a package and every module inside it. A package that does not exist is skipped."""
    try:
        package = importlib.import_module(package_name)
    except ModuleNotFoundError as exc:
        if exc.name == package_name:
            return []
        raise
    modules = [package]
    if hasattr(package, "__path__"):
        for info in pkgutil.iter_modules(package.__path__):
            modules.append(importlib.import_module(f"{package_name}.{info.name}"))
    return modules


# Importing the model modules registers their tables on Base.metadata.
for _name in ("app.models", "app.db_models"):
    _import_all(_name)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"http://(localhost|127[.]0[.]0[.]1)(:[0-9]+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter(prefix="/api")


@api.get("/health")
def health():
    return {"status": "ok", "project": settings.APP_NAME}


_seen = set()
for _pkg in ("app.routers", "app.routes"):
    for _module in _import_all(_pkg):
        _router = getattr(_module, "router", None)
        if isinstance(_router, APIRouter) and id(_router) not in _seen:
            _seen.add(id(_router))
            api.include_router(_router)
            logger.info("Mounted router from %s", _module.__name__)

app.include_router(api)

# The AI often defines "/tasks/" while the frontend calls "/tasks". Instead of answering with a
# redirect to an absolute backend URL (fragile behind the dev proxy), serve the slash form directly.
_slash_state = {}


def _needs_slash(path: str) -> bool:
    if "patterns" not in _slash_state:
        try:
            templates = list(app.openapi().get("paths", {}))
        except Exception:
            templates = []
        patterns = []
        for tpl in templates:
            regex = "/".join(
                "[^/]+" if seg.startswith("{") and seg.endswith("}") else re.escape(seg)
                for seg in tpl.split("/")
            )
            patterns.append((tpl.endswith("/"), re.compile("^" + regex + "$")))
        _slash_state["patterns"] = patterns
    patterns = _slash_state["patterns"]
    if any(rx.match(path) for _, rx in patterns):
        return False
    return any(ends_with_slash and rx.match(path + "/") for ends_with_slash, rx in patterns)


@app.middleware("http")
async def _tolerate_trailing_slash(request, call_next):
    path = request.scope["path"]
    if path.startswith("/api/") and not path.endswith("/") and _needs_slash(path):
        request.scope["path"] = path + "/"
        request.scope["raw_path"] = (path + "/").encode()
    return await call_next(request)


# Optional static UI (only for projects generated without a separate frontend/)
if os.path.isdir("static"):
    @app.get("/", include_in_schema=False)
    def _index():
        return FileResponse("static/index.html")

    app.mount("/", StaticFiles(directory="static", html=True), name="static")
