'''
API Lisence Plate Recognition v1

@Author     : Ali Mustofa HALOTEC
@Created on : 19 March 2021
'''

import io

import cv2
import numpy as np
from fastapi import FastAPI, File
from PIL import Image
import logging
from src.utils.logger import *
from src.process import main_process
import src.process

app = FastAPI(title='Lisence Plate Recognition',
              description='''Plate detection adn read text in image with open source
              library easyocr https://github.com/JaidedAI/EasyOCR''',
              version='1.0')
Logger()

@app.get('/')
def index():
    return {'title': 'Lisence Plate Recognition'}

@app.post('/v1/lpn-service')
def input_image_for_predictions(file: bytes = File(...)):
    image = Image.open(io.BytesIO(file)).convert("RGB")
    image = np.array(image)
    image = image[:,:,::-1].copy()
    logging.info('================= processing image =================')
    result = main_process(image)
    # predictions = prediction_plate.predict(image)
    # cropped_predictions = prediction_plate.filter_and_crop(image, predictions)
    # cv2.imwrite('result.jpg', img)
    return {'prediction': 'got predictions', 'results': result}
