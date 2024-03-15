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
from message_types import Message, SetMessage, ReportCompleted, ErrorMessage, DataMessage
from clean_response import remove_double_quotes, convert_to_string_array, convert_images_to_base64
from upload_image import *

# First install fastapi on terminal ''pip install fastapi''


app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # Add the origin of clients
]

UPLOAD_FOLDER = 'pdf_uploads'


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You might want to restrict this to specific methods
    allow_headers=["*"],  # You might want to restrict this to specific headers
)

DEBUG_MODE = True

@app.websocket("/")
async def websocket_interaction(websocket: WebSocket):

    async def send_message(message:Message):
        msg_str = str(message)
        await websocket.send_text(msg_str)
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
                await send_message(SetMessage("File is set"))

            is_ready = await websocket.receive_bytes()

            
            if is_ready != b"Ready to receive":
                raise(ValueError('Client sent the wrong message: ' + is_ready))

            else:
                # Now you can use the file_data for further processing
                solution_instance = Solution('./received.pdf')
                
                if DEBUG_MODE:
                    title, insights, found_images = await solution_instance.solution_pipeline_debug(send_message)    
                else:
                    title, insights, found_images = await solution_instance.solution_pipeline(send_message)
                
                report_data = {"title":remove_double_quotes(title), 
                "insightsArray":convert_to_string_array(insights),
                "imagesAndExplanations": convert_images_to_base64(found_images)}

                await send_message(ReportCompleted(report_data))

                with open("response2.txt", "w") as file:
                    # Write the string to the file
                    file.write(str(report_data))

        websocket.close()

    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        await send_message(ErrorMessage(error_message))

def main():
    uvicorn.run(app, host="0.0.0.0", port=80,ws_ping_interval=300,ws_ping_timeout=300)

if __name__ == "__main__":
    main()

#send document
    # - take user prompt to guide LLM
    # - by using user prompt handle insight extraction task 
    # - search for recommendations
# 



