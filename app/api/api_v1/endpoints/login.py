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

    return response_token.json()


@router.get("/oauth/kakao/redirect")
def request_access_token_for_kakao(response):
    pass
