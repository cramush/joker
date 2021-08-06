from flask import Flask, jsonify, request
from flask_sslify import SSLify
from bson.objectid import ObjectId
from datetime import datetime
import pymongo
from config import db_host, db_name
from waitress import serve
from loguru import logger

app = Flask(__name__)
sslify = SSLify(app)

client = pymongo.MongoClient(f"mongodb://{db_host}/{db_name}?authSource=admin")
db = client["joker_database"]
collection = db["jokes"]
if collection.estimated_document_count() == 0:
    collection.drop()
    collection.create_index([("tag", pymongo.ASCENDING), ("date", pymongo.ASCENDING)])


@app.route("/", methods=["GET"])
def hello():
    response = "Hello, I`m Joker"
    logger.info(response)
    return response


@app.route("/health", methods=["GET"])
def get_health():
    response = jsonify({"health": "OK"})
    response.status_code = 200
    logger.info(response)
    return response


@app.route("/add/one", methods=["POST"])
def add_joke():
    tag = request.json["tag"]
    data = request.json["data"]
    content = request.json["content"]
    date = datetime.now()
    joke = {
            "tag": tag,
            "data": data,
            "content": content,
            "date": date
        }
    collection.insert_one(joke)

    response = jsonify("Added successfully")
    response.status_code = 200
    logger.info(response)
    return response


@app.route("/add/many", methods=["POST"])
def add_many():
    json = request.json
    joke_list = json["jokes"]
    date = datetime.now()

    for element in joke_list:
        tag = element["tag"]
        data = element["data"]
        content = element["content"]
        joke = {
            "tag": tag,
            "data": data,
            "content": content,
            "date": date
        }
        collection.insert_one(joke)

    response = jsonify("Added successfully")
    response.status_code = 200
    logger.info(response)
    return response


@app.route("/update/<joke_id>", methods=["PUT"])
def update_joke(joke_id):
    tag = request.json["tag"]
    data = request.json["data"]
    content = request.json["content"]
    date = datetime.now()
    update = {
        "tag": tag,
        "data": data,
        "content": content,
        "date": date
    }
    collection.update_one({"_id": ObjectId(joke_id)}, {"$set": update})

    response = jsonify("Updated successfully")
    response.status_code = 200
    logger.info(response)
    return response


@app.route("/get/one", methods=["GET"])
def get_one_joke():
    random_joke = collection.aggregate([{"$sample": {"size": 1}}])
    random_joke = [{
        "id": str(el["_id"]),
        "tag": el["tag"],
        "data": el["data"],
        "content": el["content"],
        "date": el["date"]
        } for el in random_joke]

    response = jsonify({"random_joke": random_joke})
    response.status_code = 200
    logger.info(response)
    return response


@app.route("/get/<quantity>", methods=["GET"])
def get_quantity_jokes(quantity):
    box = collection.aggregate([{"$sample": {"size": int(quantity)}}])
    box = [{
        "id": str(el["_id"]),
        "tag": el["tag"],
        "data": el["data"],
        "content": el["content"],
        "date": el["date"]
        } for el in box]

    response = jsonify({"jokes": box})
    response.status_code = 200
    logger.info(response)
    return response


@app.route("/delete/one/<joke_id>", methods=["DELETE"])
def delete_joke(joke_id):
    collection.delete_one({"_id": ObjectId(joke_id)})

    response = jsonify("Deleted successfully")
    response.status_code = 200
    logger.info(response)
    return response


@app.route("/delete/all", methods=["DELETE"])
def delete_jokes():
    collection.drop()

    response = jsonify("Deleted successfully")
    response.status_code = 200
    logger.info(response)
    return response


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
