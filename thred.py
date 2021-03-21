from threading import Thread
import time
from queue import Queue

class ThreadCuk:
    def __init__(self):
        self.plate = None
        self.classi = None
        self.queue = Queue()
        self.threads_list = list()

    def license_plate(self,image):
        time.sleep(3)
        # print('License Plate')
        self.plate = 'B 1234'
        return {'License_Plate': 'B 1234'}

    def classification_vehicle(self, image):
        time.sleep(2)
        # print('Clasification Vehicle')
        self.classi = 'Car'
        return {'Clasification_Vehicle':'car'}

    def process(self, img_plate):
        # plate = Thread(name='license_plate', target=self.license_plate(arg1), args=(self.queue))
        plate = Thread(target=lambda p, arg1: p.put(self.license_plate(arg1)), args=(self.queue, 'world!'))
        classification = Thread(target=lambda c, arg2: c.put(self.classification_vehicle(arg2)), args=(self.queue, 'world!'))
        # classification =Thread(name='classification_vehicle', target=self.classification_vehicle)


        plate.start()
        classification.start()
        # test = plate.join()
        # tust = classification.join()
        self.threads_list.append(plate)
        self.threads_list.append(classification)

        for join_threads in self.threads_list:
            join_threads.join()

        ss = list()
        while not self.queue.empty():
            ss.append(self.queue.get())

       
        return {k:v for x in ss for k,v in x.items()}
'''
Estimasi waktu: 
    classification = 4s
    detection = 3s
    ocr = 3s

best time = max([classification, detection+ocr]) 
'''

anjg = time.time()
jancik = ThreadCuk()
bgst = jancik.process('poto_mobil')
print('result : ', type(bgst))
print(time.time() - anjg)