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
        if coll.find_one({'public_address': public_address}):
            raise HTTPException(status_code=409, detail="Address Already Exist")
        coll.insert_one(document=content).inserted_id
        content = prompt_generator("Hello, my name is "   + username + ". I am a new player in this world.","user", username)
        return content

def check_token_amount(public_address: str):
    conn, coll = get_mongo_client('player_data')
    with conn:
        user = coll.find_one({'public_address': public_address})
        # get public address
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
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
                if limit_before < 10:
                    coll.update_one({'player_id': username}, {'$set': {'limit': limit_before+1 }})
                else:
                    token_total =  check_token_amount(username)
                    if token_total < 10000:
                        raise HTTPException(status_code=429, detail="Your token amount is "+str(token_total)+". You can only make 10 requests per day.")
            else:
                coll.update_one({'player_id': username}, {'$set': {'limit': 1, 'buffer': datetime.now()+timedelta(hours=24) }})
    return True
