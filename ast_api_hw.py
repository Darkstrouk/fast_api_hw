from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get("/dogs/", response_model=List[Dog])
async def read_dogs():
    return list(dogs_db.values())

@app.get("/dogs/{dog_id}", response_model=Dog)
async def read_dog(dog_id: int):
    if dog_id not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dogs_db[dog_id]

@app.post("/dogs/", response_model=Dog)
async def create_dog(dog: Dog):
    dogs_db[dog.pk] = dog
    return dog

@app.put("/dogs/{dog_id}", response_model=Dog)
async def update_dog(dog_id: int, dog: Dog):
    if dog_id not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    dogs_db[dog_id] = dog
    return dog

@app.get("/")
async def root():
    return {"message": "Hello World!"}
