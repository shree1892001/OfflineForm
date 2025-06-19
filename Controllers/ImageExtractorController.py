from fastapi import APIRouter, UploadFile, File, HTTPException
from Services.DocumentProcessor import DocumentProcessor
from Services.CallAiService import CallAiService
from Constants.constant import API_KEYS_FILE
import os
import shutil

router = APIRouter()

BASE_DIRECTORY = os.getcwd()


@router.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    try:
        temp_dir = os.path.join(BASE_DIRECTORY, "temp_images")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        temp_file_path = os.path.join(temp_dir, file.filename)
        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
        api_keys = CallAiService().read_api_keys(API_KEYS_FILE)
        current_key_index = 0
        while current_key_index < len(api_keys):
            try:
                api_key = api_keys[current_key_index]
                service = DocumentProcessor(api_key)
                extracted_data = service.process_file(temp_file_path)
                if not extracted_data:
                    os.remove(temp_file_path)
                    raise HTTPException(status_code=500, detail="No data found")
                else:
                    os.remove(temp_file_path)
                    return extracted_data
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
