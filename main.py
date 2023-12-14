import json
from fastapi import FastAPI, WebSocket
from logic import database_logic, response_logic

app = FastAPI()


@app.websocket("/gameserver")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:                                       #TODO убрать этот колхоз и сделать дисконнект
        data = await websocket.receive_text()
        response = await processing_message(data)
        await websocket.send_text(response)


async def processing_message(msg):
    try:
        method_name = json.loads(msg)["command"].lower()
        response = getattr(database_logic, method_name)(msg)
        return str(response)
    except KeyError:
        response = response_logic.construct_response(json.loads(msg)["command"], "ERROR", "В сообщении отсутствует необходимое поле")
        return str(response)
    except Exception as error:
        response = response_logic.construct_response(json.loads(msg)["command"], "ERROR", str(error))
        return str(response)
