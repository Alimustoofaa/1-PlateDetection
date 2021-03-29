import os

DIRECTORY_MODEL = 'models'

detection_model = {
    'filename': 'plate_detection.pb',
    'url' : 'https://github.com/Alimustoofaa/wpod-license-plate/releases/download/v1.0/frozen_inference_graph.pb',
    'file_size' : 19161802
}

area_code = {
    'filename': 'kode_wilayah.json',
    'url': 'https://github.com/Alimustoofaa/wpod-license-plate/releases/download/v1.0/kode_wilayah.json',
    'file_size' : 121
}