from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://root:example@mongo:27017/")
db = client["flask_mongodb_crud"]
collection = db["items"]

# Routes
@app.route('/items', methods=['GET'])
def get_items():
    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify(items), 200

@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    item_id = collection.insert_one(data).inserted_id
    return jsonify(str(item_id)), 201

@app.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        item['_id'] = str(item['_id'])
        return jsonify(item), 200
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route('/items/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": data})
    if result.modified_count == 1:
        return jsonify({"message": "Item updated"}), 200
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    result = collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 1:
        return jsonify({"message": "Item deleted"}), 200
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
