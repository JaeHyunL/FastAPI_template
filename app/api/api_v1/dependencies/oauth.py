import requests
from fastapi import Depends
from sqlalchemy.orm import Session
from jose import jwt
from datetime import timedelta
from pprint import pprint

from app import crud
from app.api import deps
from app.core import security
from app.core.config import settings
from app.models.user import User, KakaoAccount
from app.schemas.user import Kakao_account, UserCreate

GET_USER_PROFILE_INFO = 'https://kapi.kakao.com/v2/user/me'


def login_division(
        db: Session | None = None,
        response_token: str | None = None):
    access_token = response_token.get("access_token")
    header = {
        "Authorization": f"Bearer {access_token}"
    }

    print(db.query(User).filter(User.email == "swaa23@gmail.com").first())
    user_profile = requests.get(
        GET_USER_PROFILE_INFO, headers=header
    )
    # if not:
    kakao_acount_local_value = user_profile.json().get('kakao_account')
    check_duplication_email = bool(
        kakao_acount_local_value.get('email') == crud.user.get_by_email(
            db, email="swaa23@gmai.com")
    )

    if check_duplication_email:
        # 이메일 조회 시 이미 있는 사용자의 경우 로그인 시도.
        access_token_expires = timedelta( # noqa
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        pass
        # TODO return DB 확인 후 데이터 토근화 리턴.
        # return {
        #     "access_token": security.create_access_token(
        #     user.id, expires_delta=access_token
        #     )

    if not check_duplication_email:
        # 이메일 조회 시 없는 사용자의 경우 회원가입.
        pydantic_kakao_account = Kakao_account(**kakao_acount_local_value)
        create_user_class = UserCreate(
            full_name=pydantic_kakao_account.profile.get("nickname"),
            email=pydantic_kakao_account.email,
            password=access_token,
        )
        create_status = crud.user.create(db, obj_in=create_user_class)
        print(create_status, "@@")
        # db.query()
        return


    # print(Kakao_account(kakao_acount_local_value))
    # print(kakao_acount_local_value.get('email'))

    # ff = crud.user.get_by_email(db, email="swaa23@gmail.com")
    # ff = db.query(User).filter(User.email == "swaa23@gmail.com").first()
    # ff = crud.user.get_by_email(db, email="swaa23@gmail.com")
    # print(ff)
    # print(user_profile.json(), 'aaasdkmasdkljnmdsanljk', crud.user.get_by_email(db, email={"email": "swaa23@gmail.com"}))
    # print(crud.user.get_by_email(db), db, response_token)
    pass

