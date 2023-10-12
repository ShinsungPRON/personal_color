# server.py
# 대충 기능만 몇개 구현한 파일
# underconnor | 23.10.13

import pymongo

# db관리
class MongoDBHandler:
    def __init__(self, db_name="pron", collection_name="pron"):
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data):
        existing = self.find_data(data.get("id"))
        if existing:
            return print("! | id 중복됨 (db반영X) \n")  # id 중복처리 

        return self.collection.insert_one(data)

    def find_data(self, id):
        return self.collection.find_one({"id": id})

    def update_status(self, id, new_status):
        self.collection.update_one({"id": id}, {"$set": {"status": new_status}})

    def update_color(self, id, new_color):
        self.collection.update_one({"id": id}, {"$set": {"data.ColorCode": new_color}})

    def delete_data(self, id):
        self.collection.delete_one({"id": id})

    def close(self):
        self.client.close()


# 에제

db = MongoDBHandler()

data = {
    "id" : 1,
    "ClientName": "CHROMEBOOK_02",
    "data": {
        "CustomerName": "홍길동",
        "ColorCode": 0xFFFFFF
    },
    "status": "waiting"
}

db.insert_data(data)


print(db.find_data(0))

db.update_status(0, "inprogress")
db.update_color(0, 0x696969)

print(db.find_data(0))

