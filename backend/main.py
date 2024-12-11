from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


db: dict[int, Item] = {}


@app.get("/items")
async def read_items():
    global db
    return db


@app.post("/items")
async def create_item(item: Item):
    global db
    item_id = len(db) + 1
    db[item_id] = item
    return item


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    global db
    return db[item_id]
