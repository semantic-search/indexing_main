from task_worker.celery import celery_app
from task_utils.extract_text_from_website import extract
from db_models.models.web_model import Web
from db_models.mongo_setup import global_init

@celery_app.task()
def index_web(url):
    global_init()
    text = extract(url)
    web_obj = Web()
    web_obj.text = text
    web_obj.url = url
    web_obj.save()

