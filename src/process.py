import cv2

from .schemas.easyocr import Methods
from .app.plate_ocr import OpticalCharacterRecognition
from .app.plate_detection import PlateDetection

prediction_plate = PlateDetection()
ocr_plate = OpticalCharacterRecognition()

def classification(img):
    pass

def plate_detection(image):
    predictions = prediction_plate.predict(image)
    return prediction_plate.filter_and_crop(image, predictions)

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
    img = img_plate.copy()
    result_ocr = ocr(img)
    print(result_ocr)
    return result_ocr

