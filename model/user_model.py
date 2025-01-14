from pydantic import BaseModel

class UserModel(BaseModel):
    username: str
    public_address: str

class UserLogsModel(BaseModel):
    player_id: str
    timestamp: int
    action: str
    description: str