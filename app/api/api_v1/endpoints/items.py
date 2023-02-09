from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def initalize_main():
    return {"안녕하시요", 'hy you?'}
