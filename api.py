from fastapi import FastAPI, File, UploadFile, Form
import uuid
import os
from task import main
from Services.YamlParserService import parse
from index_web import index_web

app = FastAPI()


@app.post("/index/file/")
def index_file(file: UploadFile = File(...), yaml:  UploadFile = File(...)):
    yaml_file = yaml.filename
    with open(yaml_file, 'wb') as f:
        f.write(yaml.file.read())
    group_array = parse(yaml_file)
    print(group_array)
    new_directory = "Downloads/" + str(uuid.uuid4()) + "/"
    os.mkdir(new_directory)
    file_name = file.filename
    saved_file = new_directory + str(file_name)
    with open(saved_file, 'wb') as f:
        f.write(file.file.read())
    saved_file_info = {
        "file": saved_file,
        "directory": new_directory
    }
    main.delay(saved_file_info, group_array, api_mode=True)
    return True


@app.post("/index/websites/")
def website(urls: list = Form(...)):
    for url in urls:
        index_web(str(url))



