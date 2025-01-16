from pydantic import BaseModel

class PromptModel(BaseModel):
    public_address: str
    message: str