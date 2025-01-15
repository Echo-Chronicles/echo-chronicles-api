from config.mongo import get_mongo_client
from fastapi.exceptions import HTTPException
from uuid import uuid4
from datetime import datetime
from services.echo import prompt_generator


def check_user(username: str):
    conn, coll = get_mongo_client('player_data')
    with conn:
        user = coll.find_one({'nickname': username})
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")

def create_user(username: str, public_address: str):
    conn, coll = get_mongo_client('player_data')
    content = {"_id": uuid4().hex,
               "nickname": username,
               "public_address": public_address,
               "last_move": ["inital user"],
               "created_at": datetime.now(),
               }
    with conn:
        coll.insert_one(document=content).inserted_id
        content = prompt_generator("Hello, my name is "   + username + ". I am a new player in this world.","user", username)
        return content    

    
