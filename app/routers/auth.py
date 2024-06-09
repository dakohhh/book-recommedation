from fastapi import APIRouter


router = APIRouter(tags=["Authentication"], prefix="/auth")


@router.post("/login")
async def login():

    return {
        "status": 200,
        "message": "login user successfully",
        "success": True,
        "data": {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjYyMmU1ZjBkZmY5NjNiOTRiMWJjZjk4IiwiZXhwIjoxNzIwNDM0OTc2fQ.ExxEjpojtjrN9w41wZMgsb1GoIfb7_B61Cbiu2JuKzI"
        },
    }
