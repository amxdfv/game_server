import json
from fastapi import FastAPI, WebSocket

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
        response = {"output": json.loads(msg)["input"]}
        return str(response)
    except KeyError:
        response = {"output": {"error": "В сообщении отсутствует поле input"}}
        return str(response)
    except Exception as error:
        response = {"output": {"error": error}}
        return str(response)
