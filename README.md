# indexing_main
Starts indexing files from Cloud storage

## Installation
```
git clone --recurse-submodules https://github.com/semantic-search/indexing_main.git
```

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
## Additional Requirements
1. Document Conversion Container Required
```
cd docker-unoconv-webservice

docker build -t docker-unoconv-webservice .

docker run --env-file=docker.env -p 80:3000 docker-unoconv-webservice
```
2. Extra Server Requirements

- Mongo Db with Authentication applied

- Redis with Authentication applied

- Apache Kafka Server with Authentication Applied (plain text Method)
> Starting Kafka Server

>Zookeeper
```
export KAFKA_OPTS="-Djava.security.auth.login.config=/home/jainal09/kafka_2.13-2.6.0/config/zookeeper_jaas.conf"

kafka_2.13-2.6.0/bin/zookeeper-server-start.sh config/zookeeper.properties
````
> Server
```
export KAFKA_OPTS="-Djava.security.auth.login.config=/home/jainal09/kafka_2.13-2.6.0/config/kafka_server_jaas.conf"

kafka_2.13-2.6.0/bin/kafka-server-start.sh kafka_2.13-2.6.0/config/server.properties
```


## Starting Celery

```
celery -A task_worker worker -l INFO
```
## Monitor through Flower

```
flower -A task_worker --address=0.0.0.0 --port=5550 
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
STORAGE_PROVIDER = 
```

## Usage
```
python main.py config.yaml
```
## Extra Notes
- Currently we tested on Azure Blob Storage

- You can add your preferred service provider by creating 
a simple elif condition to download a file in `task_utils/download_file_from_storage.py` 
- Don't Forget to add the Variable `STORAGE_PROVIDER =`
in .env 