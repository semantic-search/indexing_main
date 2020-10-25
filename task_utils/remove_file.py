import requests
from globals import DASHBOARD_API_URL_REMOVE_FILE, DASHBOARD_API_CLIENT_ID
import init


def remove_api(file, last_file):
    payload = {
        'last_file': last_file,
        'value': file,
        'client_id': DASHBOARD_API_CLIENT_ID
    }
    try:
        requests.request("POST", DASHBOARD_API_URL_REMOVE_FILE, data=payload)

    except Exception as e:
        init.send_log_msg(msg=str(e) + " EXCEPTION IN REMOVE FILE API CALL__", error=True)
