from fastapi import APIRouter
from model.echo_model import PromptModel
from services.echo import prompt_generator
from services.user import check_user, rate_limit, check_token_amount
from config.mongo import get_mongo_client
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix="/echo",
    tags=["echo"],
    responses={404: {"description": "Not found"}}
)


@router.get("/health")
async def init_world():
    return {"message": "World Already Initialized"}


@router.post("/prompt")
async def prompt(prompt_model : PromptModel):
    # check if user exists
    try:
        conn, coll = get_mongo_client('player_data')
        username = ""
        with conn:
            user = coll.find_one({'public_address': prompt_model.public_address})
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            username = user['nickname']
        check_user(username)
        limits = rate_limit(username)
        if not limits:
            token_total =  check_token_amount(public_address=prompt_model.public_address)
            if token_total < 10000:
                raise HTTPException(status_code=429, detail="Your token amount is "+str(token_total)+". You can only make 10 requests per day.")
        return prompt_generator(prompt_model.message, "user", username)
    except Exception as e:
        raise e
    