import cv2
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
    return prediction_plate.filter_and_crop(image, predictions)

def detection_char(image):
    return ocr_plate.detect_char_in_image(image)

def ocr(image):
    config = Methods(
        beam_width = 20,
        batch_size = 10,
        text_threshold = 0.4,
        link_threshold = 0.7,
        low_text = 0.4,
        slope_ths = 0.9,
    )
    return ocr_plate.read_text_in_image(image, config)

def resize(image):
    scale_percent = 175
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

def main_process(image):
    img_plate = plate_detection(image)
    if img_plate.shape[1] < 175:
        img_plate = resize(img_plate)
    detected_char =  detection_char(img_plate)
    if detected_char[0]:
        print('character found')
    else:
        print('character not found')

    img = img_plate if detected_char[0] else image
    result_ocr = ocr(img)
    print(result_ocr)
    patrend = pattren_plate.result_ocr(result_ocr)
    return patrend

