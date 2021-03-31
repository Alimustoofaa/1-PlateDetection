'''
@author     : Ali Mustofa HALOTEC
@Created on : 18 March 2021
'''

import os
import cv2
import requests
from config import *
from tqdm import tqdm
from pathlib import Path
from logging import getLogger
import tensorflow as tf

LOGGER = getLogger(__name__)

class PlateDetection:
    '''
    Load models MobileSSD Net v2
    in directory models/frozen_inference_graph.pb
    '''
    def __init__(self):
        self.detection_path = os.path.join(DIRECTORY_MODEL, detection_model['filename'])
        self.check_model()
        self.file       = tf.io.gfile.GFile(self.detection_path, 'rb')
        self.graph_def  = tf.compat.v1.GraphDef()
        self.graph_def.ParseFromString(self.file.read())

    def check_model(self):
        '''
        Checking model in path model/model_name.pb ->
        download model when model in path not found.
        '''
        Path(DIRECTORY_MODEL).mkdir(parents=True, exist_ok=True)
        if not os.path.isfile(self.detection_path):
            LOGGER.warning('Downloading plate detection model, please wait.')
            response = requests.get(detection_model['url'], stream=True)
            progress = tqdm(response.iter_content(1024), 
                        f'Downloading {detection_model["filename"]}', 
                        total=detection_model['file_size'], unit='B', 
                        unit_scale=True, unit_divisor=1024)
            with open(self.detection_path, 'wb') as f:
                for data in progress:
                    f.write(data)
                    progress.update(len(data))
            LOGGER.warning('Done downloaded plate detection model.')
        else:
            LOGGER.warning('Load plate detection model.')

    def predict(self, image):
        '''
        Resize image to (416x416) -> convert to RGB color
        Prediction image object detectionn MobileSSD
        '''
        with tf.compat.v1.Session() as sess:
            sess.graph.as_default()
            tf.import_graph_def(self.graph_def, name='')

            inp = cv2.resize(image, (416, 416))
            inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

            out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                sess.graph.get_tensor_by_name('detection_scores:0'),
                sess.graph.get_tensor_by_name('detection_boxes:0'),
                sess.graph.get_tensor_by_name('detection_classes:0')],
                feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})
            return out

    def filter_and_crop(self, image, prediction, min_score=None):
        '''
        Filter prediction based on minimum score ->
        and crop image based on maximum score
        '''
        height      = image.shape[0]
        width       = image.shape[1]
        num_pred    = int(prediction[0][0])
        score_list  = []
        image_crop_list = []
        for i in range(num_pred):
            # class_id = int(prediction[3][0][i])
            score = float(prediction[1][0][i])
            bbox = [float(v) for v in prediction[2][0][i]]
            top = bbox[1] * width
            left = bbox[0] * height
            right = bbox[3] * width
            bottom = bbox[2] * height
            if min_score:
                if score > min_score: 
                    crop_img = image[int(left-15):int(bottom+15), int(top-15):int(right+15)]
                    image_crop_list.append(crop_img)
                    score_list.append(score)
            else:
                crop_img = image[int(left-15):int(bottom+15), int(top-15):int(right+15)]
                image_crop_list.append(crop_img)
                score_list.append(score)
        # Get image index in score max
        score_hight = max(range(len(score_list)), key=score_list.__getitem__)
        img_detection = image_crop_list[score_hight]
        confidence = score_list[score_hight]
        return img_detection, confidence

# test = LoadModel()
# img = cv2.imread('photo6224513270086216528.jpg')
# results = test.predict(image=img)
# print(int(results[0][0]))
