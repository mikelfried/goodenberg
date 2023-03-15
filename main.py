from subprocess import run
import logging
from os.path import exists
import re

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse

from starlette.background import BackgroundTask

def cleanup(path: str) -> None:
    os.remove(path)

valid_key_and_type = re.compile(r'[A-Za-z0-9]+')

app = FastAPI()

@app.post('/convert', response_class=FileResponse)
async def convert(file: UploadFile, key: str, cache = False, outputtype: str = 'pdf'):
    try:
        if not valid_key_and_type.fullmatch(key):
            logging.info(f'key is invalid. should contain letters and digits only')
            raise HTTPException(status_code=422, detail=f'key is invalid. should contain letters and digits only')
        
        if not valid_key_and_type.fullmatch(outputtype):
            logging.info(f'outputtype is invalid. should contain letters and digits only')
            raise HTTPException(status_code=422, detail=f'outputtype is invalid. should contain letters and digits only')

        # Check if key valid, and outputtype valid
        converted_file_path = f'/tmp/{key}.{outputtype}'

        if not exists(converted_file_path):
            run(['unoconvert', '--convert-to', outputtype, '-', converted_file_path], stdin=file.file)

        if cache:
            return FileResponse(converted_file_path)

        return FileResponse(
            converted_file_path,
            background=BackgroundTask(cleanup, converted_file_path)
        )
    except Exception:
        logging.exception(f'Failed converting {file.filename}')
        raise HTTPException(status_code=500, detail=f'Failed converting {file.filename}')
