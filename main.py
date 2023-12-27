import json

import starlette.websockets
from fastapi import FastAPI, WebSocket
from logic import database_logic, response_logic
from service_logic import logs_logic, websocket_logic
import logging

app = FastAPI()

SESSIONS = {}


@app.websocket("/gameserver")
async def websocket_endpoint(websocket: WebSocket):  # TODO переделать запуск сокета, иначе менеджмент соединений не будет работать
    income_client = websocket.client
    logging.basicConfig(filename="logs//logs.log", level=20, encoding="UTF-8")
    try:
        await websocket.accept()
        websocket_logic.add_client_to_list(websocket)
        logging.info({income_client: 'Connected successfully'})
        while True:
            try:
                data = await websocket.receive_text()
                response = await processing_message(data)
                await websocket.send_text(response)
            except starlette.websockets.WebSocketDisconnect:
                logging.info({income_client: "Disconnected"})
            except Exception as inner_error:
                await websocket.send_text(str(inner_error))
                logging.error({income_client: str(inner_error)})
    except starlette.websockets.WebSocketDisconnect:
        logging.info({income_client: "Disconnected"})
    except Exception as error:
        logging.error({income_client: str(error)})
    finally:
        websocket_logic.remove_client_from_list(websocket)


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
