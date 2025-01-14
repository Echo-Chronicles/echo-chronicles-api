from fastapi import APIRouter
from model.echo_model import PromptModel

router = APIRouter(
    prefix="/echo",
    tags=["echo"],
    responses={404: {"description": "Not found"}}
)


@router.get("/init_world")
async def init_world():
    return {"message": "World Initialized"}


@router.post("/prompt")
async def prompt(prompt_model : PromptModel):
    pass
    