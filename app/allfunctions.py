import base64
import datetime

def decode_str(encrypt_text):
    try:
        decoded = base64.b64decode(encrypt_text).decode('ascii')
        return decoded
    except Exception as e:
        return str(e)

def decode_id(id):
    return int(decode_str(id))

def set_username(first_name=None, last_name=None, check=0):
    name = ""
    now_timestamp = datetime.datetime.now().timestamp()
    if first_name != None or first_name != "":
        name = first_name

    if last_name != None or last_name != "":
        name = f"{name}.{last_name}"
    name = name + str(now_timestamp)

    return name