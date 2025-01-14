from fastapi import APIRouter
from model.echo_model import PromptModel
from services.echo import prompt_generator
from services.user import check_user

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
        check_user(prompt_model.username)
        return prompt_generator(prompt_model.message, "user", prompt_model.username)
    except Exception as e:
        return {"error": str(e)}
    