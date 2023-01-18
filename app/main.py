import sys

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router

from pydantic import AnyHttpUrl


version = f"{sys.version_info.major}.{sys.version_info.minor}"


app = FastAPI(title="기초 백앤드 탬플릿", openapi_url="/api/v1/openapi.json")

app.include_router(api_router, prefix="/api/v1")
# TODO config 파일 아래서 설정 변경하게.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[AnyHttpUrl],
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/")
async def read_root():
    message = f"FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}
