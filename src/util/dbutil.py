from pymongo import MongoClient

class DBUtil:

    @classmethod
    def connect(cls):
        cls._client = MongoClient("mongodb://localhost:27017")
        db = cls._client["ManageDb"]
        return db
    
    @classmethod
    def close(cls):
        cls._client.close()