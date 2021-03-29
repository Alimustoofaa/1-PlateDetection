import os
import json
import requests
from config import *
from tqdm import tqdm
from pathlib import Path
from logging import getLogger

LOGGER = getLogger(__name__)

class FilterText:
    '''
    Load area code plate number indonesian
    in directory models/kode_wilayah.json
    '''
    def __init__(self):
        self.area_code_path = os.path.join(DIRECTORY_MODEL, area_code['filename'])
        self.check_model()
        self.area_code_file = open(self.area_code_path, encoding='utf-8-sig')
        self.area_code = json.load(self.area_code_file)
    
    
    def check_model(self):
        '''
        Checking model in path model/kode_wilayah.json ->
        download model when model in path not found.
        '''
        Path(DIRECTORY_MODEL).mkdir(parents=True, exist_ok=True)
        if not os.path.isfile(self.area_code_path):
            LOGGER.warning(f'Downloading {area_code["filename"]}, please wait.')
            response = requests.get(area_code['url'], stream=True)
            progress = tqdm(response.iter_content(1024), 
                        f'Downloading {area_code["filename"]}', 
                        total=area_code['file_size'], unit='B', 
                        unit_scale=True, unit_divisor=1024)
            with open(self.area_code_path, 'wb') as f:
                for data in progress:
                    f.write(data)
                    progress.update(len(data))
            LOGGER.warning(f'Done downloaded {area_code["filename"]}.')
        else:
            LOGGER.warning(f'Load {area_code["filename"]}.')

    def filter_text_conf(self, text_conf):
        '''
        Remove space in list and add create new list
        '''
        new_text_conf = list()
        for text, conf in text_conf:
            remove_space = text.split(' ')
            for word in remove_space:
                if word.isalnum():
                    new_text_conf.append([word, conf])
        return new_text_conf

    def filter_plate(self, text_conf):
        '''
        Get area code, no unique, back code in list
        '''
        plate_dict = dict()
        # Get area code
        for i in text_conf:
            if i[0] in self.area_code['wilayah']:
                plate_dict.update({'area_code' : i})
                plate_dict.update({'area_name' : self.area_code['wilayah'][i[0]]})
                text_conf.remove(i)
                break
            else:
                try:
                    find_key = self.area_code['wilayah'][i]
                    plate_dict.update({'area_code' : i})
                    plate_dict.update({'area_name' : find_key})
                    break
                except ValueError:
                    break
        
        # Get unique no and back code plate
        for i in text_conf:
            len_back_code = 0
            if len(i[0]) >= 1 and len(i[0]) <=3:
                plate_dict.update({'back_code' : i})
                len_back_code = len(i[0])
            if len(i[0]) > len_back_code or i[0].isnumeric() and i[0].isalpha():
                plate_dict.update({'unique_no' : i})
        return plate_dict


    def result_ocr(self, result):
        result.sort(reverse=False)
        text_conf_list = [[i[1], i[2]] for i in result]
        filtered_text = self.filter_text_conf(text_conf_list)
        filtered_plate = self.filter_plate(filtered_text)
        return filtered_plate

