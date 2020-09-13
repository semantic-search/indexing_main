import os
from dotenv import load_dotenv
load_dotenv()
SEND_TOPIC_FULL = "IMAGE_RESULTS"
SEND_TOPIC_TEXT = "TEXT"
KAFKA_HOSTNAME = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT = os.getenv("KAFKA_PORT")
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
RECEIVE_TOPIC = 'KERAS_MODELS'
ALLOWED_IMAGE_TYPES = ["jpg", "png"]
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
DB = os.getenv('MONGO_DB')
PORT = os.getenv('MONGO_PORT')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
CONNECTION_STRING=os.getenv('CONNECTION_STRING')

MIME_TYPES_DOCUMENTS = {
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "odt": "application/vnd.oasis.opendocument.text",
    "pdf": "application/pdf",
    "epub": "application/epub+zip"
}
MIME_TYPES_LEGACY_DOCUMENTS = {
    "doc": "application/msword",
    "ppt": "application/vnd.ms-powerpoint",
    "xls": "application/vnd.ms-excel",
}
MIME_TYPES_AUDIO = {
    "mp3": "audio/mpeg",  # sox
    "wav": "audio/x-wav",  # sox
    "m4a": "video/mp4",   # ffmpeg
    "aiff": "audio/x-aiff",  # sox

}
MIME_TYPES_IMAGES = {
    "jpg": "image/jpeg",
    "png": "image/png",
    "svg": "image/svg+xml"
}
MIME_TYPES_VIDEO = {
    "mp4": "video/mp4",  # ffmpeg
    "mkv": "video/x-matroska",  # ffmpeg
    "avi": "video/x-msvideo",  # ffmpeg
    "webm": "video/webm"  # ffmpeg
}
