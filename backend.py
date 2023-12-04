from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union

# First install fastapi on terminal ''pip install fastapi''

# Run this server on terminal by ''uvicorn backend:app --host 0.0.0.0 --port 80''

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # Add the origin of your ReactJS frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You might want to restrict this to specific methods
    allow_headers=["*"],  # You might want to restrict this to specific headers
)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class Prompt(BaseModel):
    text:str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/sendprompt")
def send_prompt(prompt:Prompt):
    response = "This is an LLM response"
    return response
