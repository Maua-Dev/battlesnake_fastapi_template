from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# TODO: Implement my logic here to handle the requests from Battlesnake

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/create_item")
def create_item(request: dict):
    item_id = request.get("item_id")
    name = request.get("name")

    return {"item_id": item_id,
            "name": name}   


handler = Mangum(app, lifespan="off")
