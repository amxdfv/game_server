import datetime
import json

import starlette.websockets
import uvicorn
from fastapi import FastAPI, WebSocket
from logic import database_logic, response_logic, config_logic
from service_logic import logs_logic
from threading import Thread
import logging

app = FastAPI()


@app.websocket("/gameserver")
async def websocket_endpoint(
        websocket: WebSocket):  # TODO переделать на нормальную тему, это какой-то пиздец
    logging.basicConfig(filename="logs//logs.log", level=20, encoding="UTF-8")
    ttl = config_logic.read_config()

    income_client = websocket.client
    connection_time = datetime.datetime.now()
    try:
        await websocket.accept()
        logging.info(logs_logic.construct_technical_log(income_client, 'Connected successfully'))
        while (datetime.datetime.now() - connection_time).seconds < ttl["connection_lifetime"]:
            if (datetime.datetime.now() - connection_time).seconds > ttl["connection_lifetime"]:
                break
            else:
                try:
                    data = await websocket.receive_text()
                    response = await processing_message(data)
                    await websocket.send_text(response)
                except starlette.websockets.WebSocketDisconnect:
                    logging.info(logs_logic.construct_technical_log(income_client, "Disconnected"))
                except Exception as inner_error:
                    await websocket.send_text(str(inner_error))
                    logging.error(logs_logic.construct_technical_log(income_client, str(inner_error)))
        await websocket.close()
    except starlette.websockets.WebSocketDisconnect:
        logging.info(logs_logic.construct_technical_log(income_client, "Disconnected"))
    except Exception as error:
        logging.error(logs_logic.construct_technical_log(income_client, str(error)))


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


if __name__ == "__main__":
    logging.basicConfig(filename="logs//logs.log", level=20, encoding="UTF-8")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
