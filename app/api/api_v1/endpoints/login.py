import requests
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.api.api_v1.dependencies.oauth import login_division
# from app.utils import (
#     generate_password_rest_token,
#     verify_password_reset_token,
# )


router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> any:
    """
    OAuth2 compatible token login, get an access token for future request
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> any:
    """
    Test access token
    """
    return current_user


@router.get("/oauth/kakao/login")
def kakao_oauth_login_action(code):
    """
    소셜로그인 카카오 토큰 발행

    카카오 로그인세션 인가코드 -> 토큰 발행

    Args:
        code: 클라이언트에서 발급받은 인가 코드

    Returns:
        _type_: TODO
    """
    CLIENT_ID = settings.KAKAO_OAUTH_CLIENT_ID
    REDIRECT_URI = settings.KAKAO_OAUTH_REDIRECT_URL
    oAuthTokenRequestUrl = "https://kauth.kakao.com/oauth/token?"
    payload = f"grant_type=authorization_code&client_id={CLIENT_ID}"
    payload += f"&redirect_uri={REDIRECT_URI}&code={code}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache"
    }
    tokenRequestURL_Join_PayLoad = oAuthTokenRequestUrl + payload

    response_token = requests.get(tokenRequestURL_Join_PayLoad, headers=headers)
    if response_token.status_code == 200:
        response_token.json()
        # TODO 로그인 성공시 로그인 할지 회원가입 할지 로직 채크...
    else:
        return response_token.json()

    return response_token.json()


@router.get("/tmp")
def tmp_api(
    db: Session = Depends(deps.get_db),
    # access_token = response_token.get("access_token")
):
    print(db.query)
    ds = {
        "access_token": "",
        "token_type": "bearer",
        "refresh_token": "gaiNjyojjDNw7SY8Yt8gM75xZN7PoS0zgAFHlCGBCisNHgAAAYY0gEQU",
        "id_token": "eyJraWQiOiI5ZjI1MmRhZGQ1ZjIzM2Y5M2QyZmE1MjhkMTJmZWEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJlNTFiYWM4OWY2YTBjYzViYmRkODczM2VmOWM4OTEwMSIsInN1YiI6IjE4MDUxNzc3ODAiLCJhdXRoX3RpbWUiOjE2NzU5MTgwNjYsImlzcyI6Imh0dHBzOi8va2F1dGgua2FrYW8uY29tIiwibmlja25hbWUiOiLsnbTsnqztmIQiLCJleHAiOjE2NzU5Mzk2NjYsImlhdCI6MTY3NTkxODA2NiwicGljdHVyZSI6Imh0dHA6Ly9rLmtha2FvY2RuLm5ldC9kbi9kcGs5bDEvYnRxbUdoQTJsS0wvT3owd0R1Sm4xWVYyREluOTJmNkRWSy9pbWdfMTEweDExMC5qcGciLCJlbWFpbCI6ImNoMDgwODA4QG5hdmVyLmNvbSJ9.pUIi0XEOEa9FjBBYtewOYSUqCGZwwobp28H2hrYCS1v5RpFPgf4coEqOHeTbZQoyEH10GSAmE1JwOKr4WBqy1MKHCniydAFjjAkH7PP2M1ZeNOq4i5TwnUl-J3_TA5Pf_wEGC1onl-Av14bibdyZN7dknsr88rnmX-a11sCaS4M2DyPI8Sy6UBnRVLUmqJ7WulywL4wOxLgI4lcBuIPZpYGo-Yg7qRWPTmdFo4mjT8f90jMinpTFfZvnWXyVAB3kpnxUYJdJ5YFPJS-zuKzSfRMQ-bH5XT5iOT9dQPDbDN_pMpmvt8cWzYqKtS9ofDWx2i-NDw0QjZ2GbwKo6u23HA",
        "expires_in": 21599,
        "scope": "age_range birthday account_email profile_image story_read talk_message gender openid profile_nickname story_publish story_permalink friends",
        "refresh_token_expires_in": 5183999
    }
    login_division(db=db, response_token=ds)
    return "hpehe"
