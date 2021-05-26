from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, CollectionInvalid
import logging
logging.basicConfig(filename='./logs/drugs_errors.log', level=logging.INFO)


class MongoConnect():
    def __init__(self, db_name, collection_name, conn_string='mongodb://192.168.56.30:27017'):
        self.conn_string = conn_string
        self.db_name = db_name
        self.collection_name = collection_name

    def connect(self):
        '''Function to create a connection with MongoDB
        INPUTS: The function expects two input variables, namely:
            db_name: Name of the Database holding the collection
            collection_name: Name of the collection to retrieve
        OUTPUT:
            collection: An object of the given collection name
        '''
        try:
            client = MongoClient(self.conn_string)
            db = client[self.db_name]
            collection = db[self.collection_name]
            return collection
        
        except CollectionInvalid:
            print("Invalid Collection Name provided, check Collection name!")
            logging.error("Exception occurred at mongo_connection", exc_info=True)
        except Exception as e:
            print('Something went wrong check logs for more info!')
            logging.error("Exception occurred at mongo_connection", exc_info=True)