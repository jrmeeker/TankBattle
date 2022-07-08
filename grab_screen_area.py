#import numpy as np
#import cv2
#import pyautogui
from PIL import Image
from PIL import ImageGrab
from sklearn_decoder import ImgRecognizer


input('PRESS ENTER TO CAPTURE')

#home screen
#board_box = (1457, 963, 1551, 979)

#your turn
#board_box = (753, 467, 1151, 864)
#board_box = (720, 465, 1186, 927)

#VICTORY
#board_box = (848, 566, 1051, 610)
board_box = (400, 900, 460, 927)
img = ImageGrab.grab()
img = img.crop(board_box)
img.save('capture.bmp')
