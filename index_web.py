from task_worker.celery import celery_app
from task_utils.extract_text_from_website import extract
from db_models.models.web_model import Web


@celery_app.task()
def index_web(url):
    text = extract(url)
    web_obj = Web()
    web_obj.text = text
    web_obj.url = url
    web_obj.save()

