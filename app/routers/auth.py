from fastapi import APIRouter



router = APIRouter(tags=["Authentication"])


@router.get("/login")
async def login():
    return {"message": "Login"}