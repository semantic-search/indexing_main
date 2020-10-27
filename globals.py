import os
from dotenv import load_dotenv


load_dotenv()
STORAGE_PROVIDER = os.getenv("STORAGE_PROVIDER")
KAFKA_HOSTNAME = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT = os.getenv("KAFKA_PORT")
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
KAFKA_CLIENT_ID = os.getenv("KAFKA_CLIENT_ID")
MONGO_HOST = os.getenv("MONGO_HOST")
DB = os.getenv('MONGO_DB')
PORT = os.getenv('MONGO_PORT')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
REDIS_DB = '0'
UNOCONV_SERVER = os.getenv('UNOCONV_SERVER')
BLOB_STORAGE_CONTAINER_NAME = os.getenv('BLOB_STORAGE_CONTAINER_NAME')
DASHBOARD_API_URL_UPDATE_LAST_FILE = os.getenv('DASHBOARD_API_URL_UPDATE_LAST_FILE')
DASHBOARD_API_URL_REMOVE_FILE = os.getenv('DASHBOARD_API_URL_REMOVE_FILE')
DASHBOARD_API_CLIENT_ID = os.getenv('DASHBOARD_API_CLIENT_ID')
LOGGER_SERVER_HOST = os.getenv('LOGGER_SERVER_HOST')
LOGGER_SERVER_PORT = os.getenv('LOGGER_SERVER_PORT')
CORS_ORIGIN = os.getenv('CORS_ORIGIN')
image_captioning_containers = None
ocr_containers = None
object_detection_containers = None
scene_recognition_containers = None
image_recognition_containers = None
image_search_containers = None
face_recognition_containers = None
sound_classification_containers = None
audio_fingerprinting_containers = None
speech_to_text_containers = None
entity_recognition_containers = None
search_containers = None
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
    "wav": "audio/x-wav",
    "wav1": "audio/wav",# sox
    "m4a": "video/mp4",
    "m4a1": "audio/mp4",# ffmpeg
    "aiff": "audio/x-aiff",  # sox
    "aiff1": "audio/aiff"

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
    "avi1": "video/avi", # ffmpeg
    "webm": "video/webm"  # ffmpeg
}
FAKE_DOC_IMAGE_EXTENSIONS = [
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".pdf",
    ".epub",
    ".odt",
    ".svg",
    ".png",
    ".jpg",
    ".jpeg"
]
FAKE_AUDIO_EXTENSIONS = [
 ".mp4",
 ".mkv",
 ".avi",
 ".webm"
]