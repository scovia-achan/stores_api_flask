import uuid
from flask import Flask, request
from db import stores, items

app = Flask(__name__)

# get all stores
@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

# create a new store
@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201

# create a new item in a store
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item,201
        
    return {"message": "Store not found"}, 404

# get a specific store
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404
    
# get store details/item
@app.get("/store/<string:name>/item")
def get_store_item(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"], "status message": "200 OK"}
    return {"message": "Store not found"}, 404


