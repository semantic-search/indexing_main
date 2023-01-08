# NERP-MultiSearch 
<p align="center"><img src="https://github.com/semantic-search/indexing_main/raw/master/nERP.png" width="200" height="200" alt="project-image"></p>
Neural Information Extraction, Retrieval, and Processing for Multi-Modal Neural Search

## Introduction

This project proposes an architecture for efficiently and securely extracting, processing, and searching for information from digital media through the use of deep learning approaches. The architecture is designed to make digital content more accessible through semantic search and explore the domains of information extraction from digital media.

## Keywords

-   Neural Search
-   Information Retrieval
-   Semantic Search

## Proposed Architecture and Approaches

The proposed architecture consists of three serving layers: extraction, transformation, and loading.

### Extraction

The extraction phase retrieves data from various sources (e.g. cloud storage, databases, websites) and categorizes it based on its MIME type (e.g. document, audio/video, image). Necessary text and images are extracted and stored in a document database, while extracted images are passed to the transformation phase for further processing. The extraction phase also involves the creation of a config.yaml file, which contains configurations for various file types and information retrieval techniques.

-   Document extraction: Extracting data (text and images) from document types such as .doc, .ppt, .xls, and .pdf
-   Video extraction: Extracting video frames and audio and storing them separately
-   Web-page extraction: Parsing HTML to extract text and image data from websites

### Transformation Phase

The transformation phase converts raw data from the extraction phase into a normalized format and stores it using an asynchronous task distributed system (e.g. Apache Kafka, Redis). It consists of three blocks: audio transformation, image transformation, and video transformation. Tools like OpenCV and Pillow may be used for image and video processing.

The transformation phase also includes a consumer block with worker nodes that listen to queues and process incoming tasks. These workers have the ability to act as producers, triggering additional tasks and chaining them together. The producer block consists of web nodes that handle web requests and enqueue jobs in the task queue when a new task is received. The task queue, implemented using a Redis transport, acts as the broker, controlling the flow of information into the system and storing tasks temporarily in case of system failure.

### Loading

The loading phase performs the important processes of information retrieval and indexing, and provides an abstraction layer for searching through all indexed data. The process of indexing begins with the creation of a config.yaml file, which specifies the deep learning-based information retrieval techniques and containers to be used for processing.

A single task goes through the following procedures:

1.  Downloading a single file or retrieving it from cloud storage, a binary storage database, or an API
2.  Parsing the binary or file metadata to determine the MIME type and categorizing the file accordingly
3.  Starting the necessary containers for information retrieval based on the config.yaml file and the file's MIME type
4.  Extracting relevant information from the file using the specified information retrieval techniques
5.  Indexing the extracted information for searching

## Searching
The search phase of the implementation allows users to search indexed data using four methods: text search with semantic search and full-text search, audio search using audio fingerprinting, image-to-image search using Euclidean distance, and face search using facial vectors and the Dlib library. Text search uses BERT and Elasticsearch, while full-text search uses Typesense. Image search uses Xception. The search process starts when a client sends a request to the API Gateway, which routes the request to the appropriate microservice.

## Conclusion

This architecture presents a solution for efficiently extracting, processing, and searching for information from digital media through the use of deep learning techniques and an asynchronous task distributed system. It aims to make digital content more accessible through semantic search and improve the process of indexing and storing large amounts of digital media.

## Demos
### Image Caption Search
Search images based on senetences, phrases or captions

![enter image description here](https://github.com/semantic-search/indexing_main/raw/master/demos/Picture1.png)
### Reverse Image Search
Search similar images based on uploaded images

![enter image description here](https://github.com/semantic-search/indexing_main/raw/master/demos/Picture2.png)

### Elastic Search with BERT
Search documents with similar meaning using bert vectorization over elastic search

![enter image description here](https://github.com/semantic-search/indexing_main/raw/master/demos/Picture3.png)

### Face Search
Search similar persons based on facial data using face-to-face search

![enter image description here](https://github.com/semantic-search/indexing_main/raw/master/demos/Picture4.png)
### Ocr
Search images using ocr text
![enter image description here](https://github.com/semantic-search/indexing_main/raw/master/demos/Picture9.png)
### Typo-Tolerant Search
Search millions of documents within seconds with type errors using typo-tolerant-search
![enter image description here](https://github.com/semantic-search/indexing_main/raw/master/demos/Picture11.png)


# Project Structure
## indexing_main (THIS Repository)
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

>logstash Server

[Setup a Logstash by following this blog](https://medium.com/swlh/python-async-logging-to-an-elk-stack-35498432cb0a)

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
KAFKA_CLIENT_ID=
KAFKA_USERNAME=
KAFKA_PASSWORD=
MONGO_HOST=
MONGO_PORT=
MONGO_DB=
MONGO_USER=
MONGO_PASSWORD=
CONNECTION_STRING=
BLOB_STORAGE_CONTAINER_NAME=
UNOCONV_SERVER=
STORAGE_PROVIDER= 
DASHBOARD_API_URL_UPDATE_STATE=
DASHBOARD_API_URL_REMOVE_FILE=
DASHBOARD_API_CLIENT_ID=
LOGGER_SERVER_HOST=
LOGGER_SERVER_PORT=
CORS_ORIGIN=
```

## Usage
```
python main.py config.yaml
```
## Extra Notes
- Currently we tested on Azure Blob Storage

- You can add your preferred service provider by creating 
a simple elif condition to download a file in `task_utils/download_file_from_storage.py` 
- Don't Forget to add the Variable `STORAGE_PROVIDER=`
in .env 
