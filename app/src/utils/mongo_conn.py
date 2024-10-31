from pymongo import MongoClient
from os import environ

MONGO_CONN_URI = environ['MONGO_CONN_URI']
MONGO_DATABASE = environ['MONGO_DATABASE']


class MongoConnection():

    def __init__(self):
        self.cnx = MongoClient(MONGO_CONN_URI)
        self.__database = MONGO_DATABASE

    def db(self):
        return self.cnx[self.__database]

    def __enter__(self):
        return self.db()

    def __exit__(self, type, value, tb):
        self.cnx.close()
