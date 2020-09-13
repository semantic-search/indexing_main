import requests
import uuid


def convert(file, target_extension):
    target_file = "Services/converted_files/" + str(uuid.uuid4()) + "." + target_extension
    url = 'http://localhost:80/unoconv/' + target_extension
    file_to_convert = [('file', open(file, 'rb'))]
    response = requests.request("POST", url, files=file_to_convert)
    with open(target_file, 'wb') as file_obj:
        file_obj.write(response.content)
    return target_file
