import cv2
import logging
from fastapi import FastAPI, HTTPException

from .schemas.easyocr import Methods
from .app.filter_text import FilterText
from .app.plate_ocr import OpticalCharacterRecognition
from .app.plate_detection import PlateDetection

prediction_plate = PlateDetection()
ocr_plate = OpticalCharacterRecognition()
pattren_plate = FilterText()

def classification(img):
    pass

def plate_detection(image):
    predictions = prediction_plate.predict(image)
    logging.info('Detection Plate Number')
    croped, conf = prediction_plate.filter_and_crop(image, predictions)
    logging.info(f'Got Detection Plate Number : {round(conf, 2)} %')
    return croped

def detection_char(image):
    detected_char = ocr_plate.detect_char_in_image(image)
    if detected_char[0]:
        logging.info(f'Detection Char in Image Plate Number : {" ".join([str(i) for i in detected_char[0]])}')
    else:
        logging.info(f'None Detection Char in Image Plate Number')
    return detected_char

def ocr(image):
    config = Methods(
        beam_width = 20,
        batch_size = 10,
        text_threshold = 0.4,
        link_threshold = 0.7,
        low_text = 0.4,
        slope_ths = 0.9,
    )
    result = ocr_plate.read_text_in_image(image, config)
    logging.info(f'Ocr Image Plate Number : {" ".join([i[1] for i in result])}')
    return result

def resize(image):
    scale_percent = 175
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    logging.info(f'Resize Image Plate from : {image.shape} to {img.shape}')
    return img

def main_process(image):
    img_plate = plate_detection(image)
    if img_plate.shape[1] < 175:
        img_plate = resize(img_plate)
    detected_char =  detection_char(img_plate)
    img = img_plate if detected_char[0] else image
    result_ocr = ocr(img)
    patrend = pattren_plate.result_ocr(result_ocr)
    return patrend

