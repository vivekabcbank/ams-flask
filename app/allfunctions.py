import base64
import datetime
from enum import Enum
from jsonmerge import merge
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

class User_Type_id(Enum):
    ADMIN = 1
    SUPERVISER = 2
    EMPLOYEE = 3

def collect_allErrors(errors1=None, errors2=None):
    errors1 = get_json_errors(errors1)
    errors2 = get_json_errors(errors2)

    errors = merge(errors1, errors2)

    return errors


def get_json_errors(error_list_data):
    __field_errors = {}

    field_errors = [(k, v[0]) for k, v in error_list_data.items()]

    for key, error_list in field_errors:
        __field_errors[key] = error_list

    return __field_errors