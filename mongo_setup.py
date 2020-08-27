import mongoengine
from dotenv import load_dotenv
import os
load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")
DB = os.getenv('MONGO_DB')


def global_init():
    """First thing we need to do here is pass alias here"""
    # with alias we can have multiple connections to multiple data bases registered
    mongoengine.register_connection(
        db=DB,
        host=MONGO_HOST,
        alias='core',
    )
    mongoengine.connect(db=DB, host=MONGO_HOST)
    """Now this registers our mongo db connection"""
    """NOTE: global_init() is required to call once in main script before interacting with the db"""
