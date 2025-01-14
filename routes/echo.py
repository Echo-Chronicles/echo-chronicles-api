from fastapi import APIRouter
from model.echo_model import PromptModel
from services.echo import prompt_generator

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
    return prompt_generator(prompt_model.message, "user", prompt_model.username)
    
    