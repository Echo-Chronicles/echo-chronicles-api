from fastapi import APIRouter
from services.user import check_user, create_user
from model.user_model import UserModel
from services.user import rate_limit
from services.echo import get_user_history as history

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)


@router.get("/check_user")
async def check_user_init(username: str):
    return check_user(username)


@router.post("/create_user")
async def create_user_init(model: UserModel):
    try:
        rate_limit(model.username)
        return create_user(model.username, model.public_address)
    except Exception as e: 
        return {"error": str(e)}
    
@router.get("/history")
async def get_user_history(username: str):
    try:
        return history(username);
    except Exception as e:
        raise e