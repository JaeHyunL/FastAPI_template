from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item # noqa


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")
    kauth_id = relationship("KakaoAccount", back_populates='kauth')


class KakaoAccount(Base):

    id = Column(Integer, primary_key=True, index=True)
    age_arange = Column(String)
    birth_day = Column(String)
    email = Column(String)
    gender = Column(String)
    profile = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    kauth = relationship("User", back_populates="kauth_id")
