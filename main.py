import json
from fastapi import FastAPI, WebSocket
from logic import database_logic, response_logic
from service_logic import logs_logic
import logging

app = FastAPI()


@app.websocket("/gameserver")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
  #  print(websocket)
    logging.basicConfig(filename="logs//logs.log", level=20, encoding="UTF-8")
    while True:                                         # TODO убрать этот колхоз и сделать дисконнект
        data = await websocket.receive_text()
        response = await processing_message(data)
        await websocket.send_text(response)


async def processing_message(msg):
    try:
        method_name = json.loads(msg)["command"].lower()
        response = getattr(database_logic, method_name)(msg)
        logging.info(logs_logic.construct_log(json.loads(msg), response))
        return str(response)
    except KeyError:
        response = response_logic.construct_response(json.loads(msg)["command"], "ERROR",
                                                     "Missing required filed in incoming message")
        logging.error(logs_logic.construct_log(json.loads(msg), response))
        return str(response)
    except Exception as error:
        response = response_logic.construct_response(json.loads(msg)["command"], "ERROR", str(error))
        logging.error(logs_logic.construct_log(json.loads(msg), response))
        return str(response)
