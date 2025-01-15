import re
from uuid import uuid4
from config.mongo import get_mongo_client
from datetime import datetime
from config.anthropic import anthropic_client, get_system_prompt
from model.user_model import UserLogsModel


def prompt_generator(prompts: str, role: str, username: str):
    # Get 3 history messages of username
    conn, coll = get_mongo_client('player_logs')
    logs_data = []
    with conn:
        logs = coll.find({'player_id': username}).sort(
            'timestamp', -1).limit(3)
        for log in logs:
            logs_data.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": log['action']
                    }
                ]
            })
            logs_data.append({
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": log['description']
                    }
                ]
            })
    logs_data.append({
        "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompts
                    }
                ]
    })
    xlient = anthropic_client()
    message = xlient.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4125,
        temperature=1,
        system=get_system_prompt(),
        messages=logs_data
    )

    content = message.content
    response = content[0].text
    print("response")
    print(response)
    print("====================================")
    regex_world_update = r"<world_update>\n(.*?)\n</world_update>"
    regex_narrative_response = r"<narrative_response>\n(.*?)\n</narrative_response>"
    regex_available_actions = r"<available_actions>\n(.*?)\n</available_actions>"

    world_update = re.findall(regex_world_update, response, re.DOTALL)
    print("world_update: ", world_update)
    print("====================================")
    narrative_response = re.findall(
        regex_narrative_response, response, re.DOTALL)
    print("narrative_response: ", narrative_response)
    print("====================================")
    available_actions = re.findall(
        regex_available_actions, response, re.DOTALL)
    available_actions_split = available_actions[0].split("\n")
    print("available_actions: ", available_actions)
    print("====================================")

    logs = {
        "player_id": username,
        "timestamp": datetime.now(),
        "action": prompts,
        "description": narrative_response[0],
        "available_actions": available_actions_split
    }
    connections, colls = get_mongo_client('player_logs')
    with connections:
        logs['_id'] = uuid4().hex
        colls.insert_one(logs)

    return {"narrative_response": narrative_response, "available_action": available_actions_split}


def get_user_history(username: str):
    conn, coll = get_mongo_client('player_logs')
    with conn:
        logs = coll.find({'player_id': username}).sort(
            'timestamp', -1).limit(3)
        logs_data = []
        for log in logs:
            logs_data.append({
                "action": log['action'],
                "description": log['description'],
                "available_actions": log['available_actions']
            })
            
    return logs_data
