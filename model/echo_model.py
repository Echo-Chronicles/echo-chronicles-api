from pydantic import BaseModel

class PromptModel(BaseModel):
    username: str
    message: str