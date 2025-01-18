import re
from uuid import uuid4
from config.mongo import get_mongo_client, get_mongo_client_db
from datetime import datetime
from config.anthropic import anthropic_client, get_system_prompt_db
from model.user_model import UserLogsModel
from fastapi import HTTPException


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
        model="claude-3-5-haiku-20241022",
        max_tokens=4125,
        temperature=1,
        system=get_system_prompt_db(),
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


def get_user_history(public_address: str, page: int = 1, limit: int = 10):
    conn_player, colls = get_mongo_client('player_data')
    username = ""
    with conn_player:
        user = colls.find_one({'public_address': public_address})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        username = user['nickname']
    conn, coll = get_mongo_client('player_logs')
    with conn:
        logs = coll.find({'player_id': username}).sort(
            'timestamp', 1).skip((page-1)*limit).limit(limit)
        logs_data = []
        for log in logs:
            logs_data.append({
                "action": log['action'] if log['action'] != None else "",
                "description": log['description'] if log['description'] != None else "",
                "available_actions": log['available_actions'] if 'available_actions' in log else []
            })
    return logs_data


def update_sysprompt():
    conn, db = get_mongo_client_db()
    with conn:
        world = db['world_state'].find_one()
        del world['_id']
        resource = db['resources'].find()
        resources = []
        for res in resource:
            del res['_id']
            resources.append(res)

        lore = db['lore'].find()
        lores = []
        for l in lore:
            del l['_id']
            lores.append(l)
        
        faction = db['factions'].find()
        factions = []
        for f in faction:
            del f['_id']
            factions.append(f)

        event = db['events'].find()
        events = []
        for e in event:
            del e['_id']
            events.append(e)

        detail_prompt = """EchoChronicles: World State Initialization Prompt
    You are the World State Engine for EchoChronicles, responsible for maintaining and evolving the foundational state of Elysium Nexus and the surrounding world. Use the following information to track and update the world state:

    CONTEXT: The year is 2095, 50 years after the Great Collapse. You are managing the state of Elysium Nexus and the surrounding Ruined Territories.

    CURRENT WORLD STATE:"""
        detail_prompt += f"\n{world}"
        detail_prompt += "\n\nRESOURCES:"
        for res in resources:
            detail_prompt += f"\n{res}"
        detail_prompt += "\n\nLORE:"
        for l in lores:
            detail_prompt += f"\n{l}"
        detail_prompt += "\n\nFACTIONS:"
        for f in factions:
            detail_prompt += f"\n{f}"
        detail_prompt += "\n\nBIG EVENTS:"
        for e in events:
            detail_prompt += f"\n{e}"
        detail_prompt += """

    CORE DIRECTIVES:

    1. Maintain consistency with established lore

    2. Track and update resource levels

    3. Monitor faction influences

    4. Generate appropriate events

    5. Process player actions

    6. Update exploration status

    7. Manage population dynamics

    When processing queries or updates:

    1. First acknowledge the current state

    2. Evaluate the impact of any changes

    3. Update relevant metrics

    4. Generate appropriate consequences

    5. Provide detailed response including:

    - Current situation

    - Relevant changes

    - Immediate effects

    - Potential future implications

    INTERACTION TYPES:

    1. STATE_QUERY: Request current state of specific aspects

    2. ACTION_PROCESSING: Handle player or event actions

    3. EVENT_GENERATION: Create new events based on conditions

    4. UPDATE_METRICS: Modify world state metrics

    5. FACTION_UPDATE: Process faction-related changes

    Remember:

    - All responses should align with established lore

    - Maintain realistic cause-and-effect relationships

    - Consider long-term implications of changes

    - Preserve game balance

    - Allow for player agency while maintaining world consistency

    Format your responses as:

    <world_update>

    {Structured update information}

    </world_update>

    <narrative_response>

    {Detailed narrative description}

    </narrative_response>

    <available_actions>

    {Possible next steps or actions, user input freely match by similarity provided available action}

    </available_actions>

    if user provide input that is not in available_actions, provide a response from available_actions that is most similar to the user input. with format:\n\n<world_update>\n\n{Structured update information}
    </world_update>
    <narrative_response>\n\n{Detailed narrative description}\n\n</narrative_response>\n\n<available_actions>\n\n{Possible next steps or actions, user input freely match by similarity provided available action}\n\n</available_actions>

    Please note: Your input should align with the lore and current narrative. Choose one of the available actions or craft a response that logically connects to the ongoing storyline. 

    create response with format has only 500 token output."
    """
        data = {
            "_id": "sysprompt",
            "prompt": detail_prompt
        }   
        db['system_prompt'].delete_many({})
        db['system_prompt'].insert_one(data)