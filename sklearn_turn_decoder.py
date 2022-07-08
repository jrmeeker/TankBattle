from sklearn import svm
from sklearn.model_selection import train_test_split
import joblib
from PIL import Image
from PIL import ImageGrab
import os
import numpy as np
import pyautogui
import time

'''
 tile values:
- 0 Your Turn
- 1 Other
'''


class ImgRecognizer2:
    def __init__(self):
        self.training_data = []
        self.target_values = []
        self.svc = svm.SVC(gamma=0.001, kernel='linear', C=100)
        self.downscale_res = (32, 32)

    def _load(self, path, target_value):
        training_imgs = os.listdir(path)
        for f in training_imgs:
            img = Image.open(path+'/'+f)
            img = img.resize(self.downscale_res, Image.BILINEAR)
            self.training_data.append(np.array(img.getdata()).flatten())
            self.target_values.append(target_value)

    def load(self):
        self._load('Training_Data/Your_Turn', 0)
        self._load('Training_Data/Not_Your_Turn', 1)
        #self._load('Training_Data/Bomb', 2)
        #self._load('Training_Data/x2', 3)
        #self._load('Training_Data/Shield', 4)


    def train(self):
        if os.path.isfile('svc2.dat'):
            self.svc = joblib.load('svc2.dat')
        else:
            self.load()
            np_data = np.array(self.training_data)
            np_values = np.array(self.target_values)
            self.svc.fit(np_data, np_values)
            joblib.dump(self.svc, 'svc2.dat', compress=6)

    def test(self):
        np_train_data = np.array(self.training_data)
        np_values = np.array(self.target_values)
        data, test_data, train_target, test_target = train_test_split(np_train_data, np_values, test_size=0.4, random_state=0)
        #data = data.reshape(-1, 1)
        #test_data = test_data.reshape(-1, 1)
        #train_target = train_target.reshape(-1, 1)
        #test_target = test_target.reshape(-1, 1)

        self.svc.fit(data, train_target)
        print(self.svc.score(test_data, test_target))

    def predict(self, img):
        resized_img = img.resize(self.downscale_res, Image.BILINEAR)
        np_img = np.array(resized_img.getdata()).flatten()
        np_img = [np_img]
        return int(self.svc.predict(np_img))

#driver
'''
board_box = (764,633,1155,683)
turn_recognizer = ImgRecognizer2()
turn_recognizer.train()

while(1):
    time.sleep(.25)
    img = ImageGrab.grab()
    img = img.crop(board_box)
    pred = turn_recognizer.predict(img)
    if pred == 0:
        print('YOUR TURN')
    else:
        print('.')
'''
