# indexing_main
Starts indexing files from az storage

## Installation

```
sudo apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig

pip install -r requirements.txt
```

## Providing Permission
```
cd Services

chmod u+x pdfimages

chmod u+x pdftotext
```
## Container Required
```
cd docker-unoconv-webservice

docker build -t docker-unoconv-webservice .

docker run --env-file=docker.env -p 80:3000 docker-unoconv-webservice
```

## Starting Celery

```
celery -A task_worker worker -l info
```
## Monitor through Flower

```
flower -A task_worker --address=0.0.0.0 --port=5555
```
## Env
Dont Forget to add the environment variables in the `.env` file
```.env
REDIS_HOSTNAME=
REDIS_PORT=
REDIS_PASSWORD=
KAFKA_HOSTNAME=
KAFKA_PORT=
MONGO_HOST=
MONGO_PORT=
MONGO_DB=
CONNECTION_STRING=
MONGO_USER=
MONGO_PASSWORD=
BLOB_STORAGE_CONTAINER_NAME=
KAFKA_CLIENT_ID=
KAFKA_USERNAME=
KAFKA_PASSWORD=
UNOCONV_SERVER =
```

## Usage
```
python main.py config.yaml
```
