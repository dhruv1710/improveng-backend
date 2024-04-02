from fastapi import FastAPI, File, UploadFile
import base64
import uvicorn
import io
import requests
from fastapi.middleware.cors import CORSMiddleware
import boto3
boto3.setup_default_session(region_name='ap-south-1',aws_access_key_id='AKIAVJMOT2XBVTZA6SNN',
    aws_secret_access_key='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')
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {'hello':'world'}

@app.get('/doc')
def read_root():
    return {'hello':'world'}



textract_client = boto3.client('textract')
@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    # Read the image file
    print('got file')
    image_bytes = await file.read()
    image = {'Bytes': image_bytes}
    response = textract_client.detect_document_text(Document=image)
    # Return the extracted text
    print(response)
    textList = []
    for k in response['Blocks']:
        if k['BlockType'] == 'WORD':
            textList.append(k['Text'])
    return {'text':textList}

@app.get('/grammar')
def grammar_corrections(text: str):
    url = "https://api.ai21.com/studio/v1/gec"
    payload = { "text": text }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer RX92sajEHPI95UryWjQdFNVeQ343CY1Q"
    }

    response = requests.post(url,json=payload, headers=headers)
    print(response.json())
    return response.json()

@app.get('/text-improvements')
def text_improvements(text: str):
    url = "https://api.ai21.com/studio/v1/improvements"

    payload = {
        "types": ["fluency", "vocabulary/specificity", "vocabulary/variety", "clarity/short-sentences", "clarity/conciseness"],
        "text": text
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer RX92sajEHPI95UryWjQdFNVeQ343CY1Q"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    return response.json()
