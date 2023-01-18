from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base


def init_db(db: Session) -> None:
    pass