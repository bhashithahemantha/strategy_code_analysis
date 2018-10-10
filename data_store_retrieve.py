import pymongo
import configparser
import os


class DatabaseModel:

    def __init__(self, conf):
        self.conf = conf
        config = configparser.ConfigParser()
        # config.read('dbConfig.ini')
        config.read(os.path.join(os.path.dirname(__file__), 'db_config.ini'))

        client = pymongo.MongoClient(config[self.conf]['url'])
        db = client[config[self.conf]['db']]
        collection = db[config[self.conf]['collection']]
        self.subCollection = collection[config[self.conf]['subCollection']]

    def insert(self, docs):
        self.subCollection.insert_many(docs)

    def find_all(self, query):
        output = []
        retrieved_data = self.subCollection.find(query)
        for doc in retrieved_data:
            output.append(doc)
        return output

