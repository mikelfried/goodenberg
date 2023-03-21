from subprocess import run
import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


from os.path import exists
import os
import re

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse

from starlette.background import BackgroundTask


def cleanup(path: str) -> None:
    try:
        os.remove(path)
    except Exception:
        logger.exception(f'Error during remove of path: {path}')


valid_key_and_type = re.compile(r'[A-Za-z0-9]+')

app = FastAPI()

@app.post('/convert', response_class=FileResponse)
async def convert(file: UploadFile, key: str, cache = False, outputtype: str = 'pdf'):
    try:
        if not valid_key_and_type.fullmatch(key):
            logger.info(f'key is invalid. should contain letters and digits only')
            raise HTTPException(status_code=422, detail=f'key is invalid. should contain letters and digits only')
        
        if not valid_key_and_type.fullmatch(outputtype):
            logger.info(f'outputtype is invalid. should contain letters and digits only')
            raise HTTPException(status_code=422, detail=f'outputtype is invalid. should contain letters and digits only')

        # Check if key valid, and outputtype valid
        converted_file_path = f'/tmp/{key}.{outputtype}'
        already_exist = True

        if not exists(converted_file_path):
            already_exist = False
            logger.info(f'key does not exist already, running unoconvert on the file.')

            try:
                run(['unoconvert', '--convert-to', outputtype, '-', converted_file_path], stdin=file.file)
            except Exception:
                logger.exception(f'Error during unoconvert run')

        if cache or already_exist:
            logger.debug('returning cached file')
            return FileResponse(converted_file_path)
    
        logger.debug(f'cache not exist, returning the file {converted_file_path} and then removing it.')

        return FileResponse(
            converted_file_path,
            background=BackgroundTask(cleanup, converted_file_path)
        )
    except Exception:
        logger.exception(f'Failed converting {file.filename}')
        raise HTTPException(status_code=500, detail=f'Failed converting {file.filename}')
