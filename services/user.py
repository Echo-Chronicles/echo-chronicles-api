from config.mongo import get_mongo_client
from fastapi.exceptions import HTTPException

def check_user(username: str):
    conn, coll = get_mongo_client('player_data')
    with conn:
        user = coll.find_one({'username': username})
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
        
