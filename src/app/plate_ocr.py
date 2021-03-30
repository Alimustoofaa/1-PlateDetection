'''
@author     : Ali Mustofa HALOTEC
@Created on : 19 March 2021
'''

import cv2
import torch
import easyocr
import numpy as np

class OpticalCharacterRecognition:
    '''
    Set configuration for ocr plate number in library EasyOCR 
    '''
    def __init__(self):
        self.enggine = True if torch.cuda.is_available() else False
        self.list_langs = ['en', 'id']
        self.recog_network = 'english_g2'
        self.reader = easyocr.Reader(self.list_langs, gpu=self.enggine, recog_network=self.recog_network)
        
    def extract_text(self, bounds):
        '''
        Extract results to arr [text],[confidence]
        '''
        text_conf = []
        for bound in bounds:
            text_conf.append([bound[1], bound[2]])
        return text_conf
    
    def detect_char_in_image(self, image):
        return self.reader.detect(image)
    
    def read_text_in_image(self, image, config):# image, item
        '''
        config and value config set for ocr plate number
        '''
        results = self.reader.readtext(
            image,
            detail          = config.detail,
            decoder         = config.decoder,
            beamWidth       = config.beam_width,
            batch_size      = config.batch_size,
            workers         = config.workers,
            allowlist       = config.allow_list,
            blocklist       = config.blocklist,
            paragraph       = config.paragraph,
            min_size        = config.min_size,
            rotation_info   = config.rotation_info,
            # Contrast
            contrast_ths    = config.contrast_ths,
            adjust_contrast = config.adjust_contrast,
            # Text detection
            text_threshold  = config.text_threshold + 0.1 if self.enggine else config.text_threshold,
            low_text        = config.low_text,
            link_threshold  = config.link_threshold,
            canvas_size     = config.canvas_size,
            mag_ratio       = config.mag_ratio

        )
        return results

# test = OpticalCharacterRecognition()
# image = cv2.imread('test.jpg')
# print(type(image))
# asu = Methods()
# test.read_text_in_image(image, asu)