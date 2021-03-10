
import os
import logging
from datetime import datetime as dt

def setup():
    attachments_path = os.path.join(os.getcwd(), 'attachments')
    images_path = os.path.join(os.getcwd(), 'images')
    logs_path = os.path.join(os.getcwd(), 'logs')

    for p in [attachments_path, images_path, logs_path]:
        if not os.path.isdir(p):
            os.mkdir(p)

    logs_file_name = f'{logs_path}/{dt.now().strftime("%d_%m_%Y_%Hh%Mmin")}.log'
    logging.basicConfig(
        handlers=[
            logging.FileHandler(logs_file_name),
            logging.StreamHandler()
        ],
        encoding='utf-8', level=logging.INFO
    )

    return images_path, attachments_path