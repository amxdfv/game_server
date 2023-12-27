import json

import pymysql
from logic import response_logic, config_logic


def get_connection():
    config = config_logic.read_config()
    return pymysql.connect(host=config["sql_host"], user=config["sql_user"],
                           password=config["sql_password"], database=config["sql_database"])


def get_user(msg):
    con = get_connection()
    try:
        login = json.loads(msg)["login"]
        pas = json.loads(msg)["password"]

        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE login=%(login)s AND password=%(password)s",
                       {'login': login, 'password': pas})
        data = None

        rows = cursor.fetchall()

        if cursor.rowcount > 2:
            return response_logic.construct_response("GET_USER", "ERROR", "Found more than one user")
        elif cursor.rowcount < 1:
            return response_logic.construct_response("GET_USER", "ERROR", "User not found")

        for row in rows:
            data = {"login": row[0], "password": row[1], "name": row[2],
                    "date_of_creation": row[3].strftime("%Y-%m-%d %H:%M:%S"), "score": row[4]}
        return response_logic.construct_response("GET_USER", "SUCCESS", data)

    except Exception as error:
        return response_logic.construct_response("GET_USER", "ERROR", str(error))
    finally:
        con.close()


def create_user(msg):
    con = get_connection()
    try:
        user = json.loads(msg)
        if 'name' not in user:
            user["name"] = None

        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO users (login, password, name, date_of_creation, score) VALUES (%(login)s,%(password)s,%(name)s,now(),0)",
            {'login': user["login"], 'password': user["password"], "name": user["name"]})
        con.commit()

        return response_logic.construct_response("CREATE_USER", "SUCCESS", "Пользователь успешно создан")
    except Exception as error:
        return response_logic.construct_response("CREATE_USER", "ERROR", str(error))
    finally:
        con.close()


def update_score(msg):
    con = get_connection()
    try:
        check_user = get_user(msg)
        if check_user["result"] is "ERROR":
            return response_logic.construct_response("UPDATE_SCORE", "ERROR", check_user["message"])
        user = json.loads(msg)

        cursor = con.cursor()
        cursor.execute(
            "UPDATE users SET score=%(score)s WHERE login=%(login)s AND password=%(password)s",
            {'login': user["login"], 'password': user["password"], "score": str(user["score"])})
        con.commit()
        return response_logic.construct_response("UPDATE_SCORE", "SUCCESS", "Счет пользователя успешно обновлен")
    except Exception as error:
        return response_logic.construct_response("UPDATE_SCORE", "ERROR", str(error))
    finally:
        con.close()
