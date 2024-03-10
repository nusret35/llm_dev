from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union
from solution import Solution
import os
import asyncio
import shutil
import base64
import json
import uvicorn
from threading import Thread, Lock

# First install fastapi on terminal ''pip install fastapi''

# Run this server on terminal by ''uvicorn backend:app --host 0.0.0.0 --port 80''
# uvicorn main:app --reload --ws-ping-interval=0


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


@app.websocket("/")
async def websocket_interaction(websocket: WebSocket):
    async def send_message(msg):
        await websocket.send_text(msg)
        await asyncio.sleep(0)
    
    is_app_open = True
    try:
        # Accept WebSocket connection
        await websocket.accept()
        while is_app_open:
            # Initialize an empty bytes object to accumulate file data
            file_data = b''
            async for chunk in websocket.iter_bytes():
                if chunk == b"END_OF_FILE":
                    break
                # Append the received chunk to the file data
                file_data += chunk
        
            # You can save the file data to a file or perform any other processing here
            # For example, save it to a file named "received.pdf"
            with open("received.pdf", "wb") as file:
                file.write(file_data)
                await send_message("File is set")

            is_ready = await websocket.receive_bytes()

            if is_ready == b"Ready to receive":
                # Now you can use the file_data for further processing
                solution_instance = Solution('./received.pdf')
                title, insights, found_images = await solution_instance.solution_pipeline(websocket)

                response = title + '\n' + insights + '\n' + str(found_images)

                # Send final response to the client
                await send_message(json.dumps({'report':response}))

        websocket.close()

    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        await websocket.send_text(error_message)

uvicorn.run(app, host="0.0.0.0", port=80,ws_ping_interval=300,ws_ping_timeout=300)

#send document
    # - take user prompt to guide LLM
    # - by using user prompt handle insight extraction task 
    # - search for recommendations
# 



