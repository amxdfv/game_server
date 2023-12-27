import datetime

SESSIONS = {}


def add_client_to_list(websocket):
    global SESSIONS
    SESSIONS[websocket] = datetime.datetime.now()


def remove_client_from_list(websocket):
    global SESSIONS
    del SESSIONS[websocket]
