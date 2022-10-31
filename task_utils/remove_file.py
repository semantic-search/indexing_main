import requests
from globals import DASHBOARD_API_URL_REMOVE_FILE, DASHBOARD_API_CLIENT_ID
import init


def remove_api(file, last_file):
    payload = {
        'last_file': last_file,
        'value': file,
        'client_id': DASHBOARD_API_CLIENT_ID
    }

    requests.request("POST", DASHBOARD_API_URL_REMOVE_FILE, data=payload)
    init.send_log_msg(msg=str(e) + " EXCEPTION IN REMOVE FILE API CALL__", error=True)
