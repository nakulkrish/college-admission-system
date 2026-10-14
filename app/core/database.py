from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# Synchronous SQLAlchemy only: no async drivers, so no greenlet/aiosqlite surprises.
DATABASE_URL = settings.DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")
_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=_connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    # Generated models often use the pre-2.0 style (`items: List[Item] = relationship(...)`),
    # which SQLAlchemy 2.x rejects unless the base class allows unmapped annotations.
    __allow_unmapped__ = True


metadata = Base.metadata


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
