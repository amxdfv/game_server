import json
import datetime

import starlette.websockets


def construct_log(inc_msg, out_msg):
    log_message = {'Timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Incoming message': inc_msg,
                   'Outcoming message': out_msg}
    return json.dumps(log_message)


def construct_technical_log(client, msg):
    log_message = {'Timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(client): msg}
    return json.dumps(log_message)
