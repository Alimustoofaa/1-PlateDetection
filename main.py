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

from app.plate import LoadModel

app = FastAPI(title='Lisence Plate Recognition',
              description='''Plate detection adn read text in image with open source
              library easyocr https://github.com/JaidedAI/EasyOCR''',
              version='1.0')

prediction_plate = LoadModel()

@app.get('/')
def index():
    return {'title': 'Lisence Plate Recognition'}

@app.post('/v1/lpn-service')
def input_image_for_predictions(file: bytes = File(...)):
    image = Image.open(io.BytesIO(file)).convert("RGB")
    image = np.array(image)
    image = image[:,:,::-1].copy()
    predictions = prediction_plate.predict(image)
    cropped_predictions = prediction_plate.filter_and_crop(image, predictions)
    cv2.imwrite('result.jpg', cropped_predictions)
    return {'prediction': 'got predictions'}
