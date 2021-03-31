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
        area_code_list = list()
        # Get area code
        for i in text_conf:
            if i[0] in self.area_code['wilayah']:
                plate_dict.update({'area_code' : i})
                plate_dict.update({'area_name' : self.area_code['wilayah'][i[0]]})
                area_code_list.append(i)
                break
            else:
                try:
                    if i[0].isnumeric:
                        if int(i[0]) == 5:
                            char = ['F', 1]
                        elif int(i[0]) == 0:
                            char = ['O', 1]
                    else:
                        if i[0] == 'I':
                            char = ['F', 1]
                    try:
                        find_key = self.area_code['wilayah'][char[0]]
                        plate_dict.update({'area_code' : char})
                        plate_dict.update({'area_name' : find_key})
                        area_code_list.append(i)
                        break
                    except KeyError:
                        pass
                except ValueError:
                    pass
        
        # Get unique no and back code plate
        new_text_conf = [elem for elem in text_conf if elem not in area_code_list]
        for i in new_text_conf:
            len_back_code = 0
            if (len(i[0]) >= 1 and len(i[0]) <=3) or len([0]) == 3 or len([0]) == 2 and (i[0].isalnum() or i[0].isalpha()):
                plate_dict.update({'back_code' : i})
                len_back_code = len(i[0])
            if len(i[0]) >= len_back_code and (i[0].isnumeric() and not i[0].isalpha()) and i[0][0] != '0':
                plate_dict.update({'unique_no' : i})
        return plate_dict

    def extract_dict(self, plate_dict, text_conf):
        '''
        -> Get area code, no unique, back code in param plate_dict
            if KeyError process with text_conf.
        -> Marge result to variable license_plate
        -> Calculate confidence level  
        '''
        conf_list = []
        try:
            area_code = plate_dict['area_code'][0]
            conf_list.append( plate_dict['area_code'][1])
        except KeyError:
            area_code = [word for word,_ in text_conf][0]
            conf_list.append([conf for _, conf in text_conf][0])

        try:
            no_unique = plate_dict['unique_no'][0]
            conf_list.append(plate_dict['unique_no'][1])
        except KeyError:
            no_unique = [word for word,_ in text_conf][1]
            # replacing str in word to str int
            for char in no_unique:
                if char == 'T':
                    no_unique = no_unique.replace(char, '1')
                elif char == 'I':
                    no_unique = no_unique.replace(char, '1')
                elif char == 'L':
                    no_unique = no_unique.replace(char, '4')

            conf_list.append([conf for _, conf in text_conf][1])

        try:
            back_code = plate_dict['back_code'][0]
            conf_list.append(plate_dict['back_code'][1])
        except KeyError:
            back_code = [word for word,_ in text_conf][2]
            conf_list.append([conf for _, conf in text_conf][2])
        
        try:
            area_name = plate_dict['area_name']
        except KeyError:
            area_name = None

        # Merge License Plate
        license_plate = (f'{area_code} {no_unique} {back_code}')
        confidence = round((sum(conf_list)/len(conf_list)), 2)
        
        respone_dict = {
            'license_plate': license_plate,
            'confidence': confidence,
            'area_name': area_name,
        }
        return respone_dict

    def result_ocr(self, result):
        result.sort(reverse=False)
        text_conf_list  = [[i[1], i[2]] for i in result]
        filtered_text   = self.filter_text_conf(text_conf_list)
        filtered_plate  = self.filter_plate(filtered_text)
        responsed       = self.extract_dict(filtered_plate, filtered_text)
        return responsed

