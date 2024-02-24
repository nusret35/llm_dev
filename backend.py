from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union
from solution import Solution
import os
import shutil
import base64
#import 

# First install fastapi on terminal ''pip install fastapi''

# Run this server on terminal by ''uvicorn backend:app --host 0.0.0.0 --port 80''

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # Add the origin of your ReactJS frontend
]

UPLOAD_FOLDER = 'pdf_uploads'

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


class PDFData(BaseModel):
    pdfData: list[int]

@app.post("/sendpdf")
async def receive_pdf_data(pdf_data: PDFData):
    try:
        # Extract the PDF data from the request
        pdf_bytes = bytes(pdf_data.pdfData)
        
        # You can save the PDF data to a file or perform any other processing here
        # For example, save it to a file named "received.pdf"
        with open("received.pdf", "wb") as file:
            file.write(pdf_bytes)

        solution_instance = Solution('./received.pdf')

        title, insights, found_images = solution_instance.solution_pipeline()

        response = title + '\n' + insights + '\n' + str(found_images)

        return {"message":response}

    except Exception as e:
        return {"message": f"Error receiving and saving PDF data: {str(e)}"}


#send document
    # - take user prompt to guide LLM
    # - by using user prompt handle insight extraction task 
    # - search for recommendations
# 



