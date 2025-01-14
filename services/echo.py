from config.mongo import get_mongo_client
def prompt_generator(message: str, role: str, username: str):
    # Get 3 history messages of username
    conn, coll = get_mongo_client('player_logs')
    logs_data = []
    with conn:
        logs = coll.find({'player_id': username}).sort('timestamp', -1).limit(3)
            

