import sys
sys.path.append(r"D:\workspace\FastAPI_template")
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from app import crud, schemas
from app.core.config import settings
from app.db import session

Base = declarative_base()


def init_db(db: Session) -> None:

    Base.metadata.create_all(bind=session.engine)
    print("워워어어어", Base.metadata, session.engine)
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)

    print("22")
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)
    print("33")