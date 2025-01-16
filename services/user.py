from config.mongo import get_mongo_client
from fastapi.exceptions import HTTPException
from uuid import uuid4
from datetime import datetime, timedelta
from services.echo import prompt_generator
from config.solana import get_token_accounts_by_owner

def check_user(username: str):
    conn, coll = get_mongo_client('player_data')
    with conn:
        user = coll.find_one({'nickname': username})
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
        
def check_address(address: str):
    conn, coll = get_mongo_client('player_data')
    with conn:
        user = coll.find_one({'public_address': address})
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

def check_token_amount(username: str):
    conn, coll = get_mongo_client('player_data')
    with conn:
        user = coll.find_one({'nickname': username})
        # get public address
        public_address = user['public_address']
        # get token amount
        token = get_token_accounts_by_owner(public_address)
        return token
    
def rate_limit(username: str):
    conn, coll = get_mongo_client('limit')
    with conn:
        user = coll.find_one({'player_id': username})
        if not user:
            content = {"_id": uuid4().hex,
                       "player_id": username,
                       "limit": 1,
                       "buffer": datetime.now()+timedelta(hours=24),
                       }
            coll.insert_one(document=content).inserted_id
        else:
            buffer = user['buffer']
            if datetime.now() < buffer:
                limit_before = user['limit']
                print(limit_before)
                if limit_before < 10:
                    coll.update_one({'player_id': username}, {'$set': {'limit': limit_before+1 }})
                else:
                    if check_token_amount(username) < 1000:
                        raise HTTPException(status_code=429, detail="Limit user "+username+" has reached")
            else:
                coll.update_one({'player_id': username}, {'$set': {'limit': 1, 'buffer': datetime.now()+timedelta(hours=24) }})
    return True
