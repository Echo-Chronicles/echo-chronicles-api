from fastapi import APIRouter
from services.user import check_user, create_user, check_address
from model.user_model import UserModel
from services.user import rate_limit, check_token_amount
from services.echo import get_user_history as history

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)


@router.get("/check_user")
async def check_user_init(username: str):
    return check_user(username)

@router.get("/check_address")
async def check_address_init(address: str):
    try:
        return check_address(address)
    except Exception as e:
        raise e
    
@router.get("/check_token_amount")
async def check_token_amount_init(public_address: str):
    try:
        return check_token_amount(public_address=public_address)
    except Exception as e:
        raise e

@router.post("/create_user")
async def create_user_init(model: UserModel):
    try:
        rate_limit(model.username)
        return create_user(model.username, model.public_address)
    except Exception as e: 
        return {"error": str(e)}
        
    
@router.get("/history")
async def get_user_history(public_address: str, page: int = 1, limit: int = 5):
    try:
        return history(public_address, page, limit);
    except Exception as e:
        raise e