from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

class MongoDBLibrary:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_one(self, collection_name, data):
        try:
            result = self.db[collection_name].insert_one(data)
            return result.inserted_id
        except DuplicateKeyError:
            raise DuplicateKeyError("Document with the same key already exists")

    def find_one(self, collection_name, query):
        return self.db[collection_name].find_one(query)

    def find_many(self, collection_name, query):
        return list(self.db[collection_name].find(query))

    def update_one(self, collection_name, query, update_data):
        result = self.db[collection_name].update_one(query, {"$set": update_data})
        return result.modified_count

    def delete_one(self, collection_name, query):
        result = self.db[collection_name].delete_one(query)
        return result.deleted_count

    def insert_todo(self, task, status, date):
        new_todo = {
            "task": task,
            "status": status,
            "date": date
        }
        return self.insert_one("todos", new_todo)

    def get_todo_by_id(self, todo_id):
        return self.find_one("todos", {"_id": ObjectId(todo_id)})

    def get_all_todos(self):
        return self.find_many("todos", {})

    def update_todo_by_id(self, todo_id, update_data):
        return self.update_one("todos", {"_id": ObjectId(todo_id)}, update_data)

    def delete_todo_by_id(self, todo_id):
        return self.delete_one("todos", {"_id": ObjectId(todo_id)})
