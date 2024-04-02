from fastapi import FastAPI, File, UploadFile
import base64
import uvicorn
import io
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

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000,reload=True,log_level=0)