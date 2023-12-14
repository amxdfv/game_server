import json


def construct_response(command, result, message):
    response = {"command": command, "result": result, "message":message}
    return response
