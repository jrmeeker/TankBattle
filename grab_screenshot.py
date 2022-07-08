import numpy as np
#import cv2
#import pyautogui
from PIL import Image
from PIL import ImageGrab
from sklearn_decoder import ImgRecognizer
#import win32api, win32con
#import time
#import random


new_capture = True

#settings for cropping screenshot and getting cells
#board_box = (753, 467, 1151, 864)
board_box = (720, 465, 1186, 927)
board_size = 6
img_size = (board_box[2]-board_box[0], board_box[3]-board_box[1])
cell_size = (img_size[0]/6, img_size[1]/6)


#if new capture required
if new_capture:
    img = ImageGrab.grab()
    img = img.crop(board_box)
    #img.show()
    img.save('capture.bmp')
else:
    img = Image.open('capture.bmp')

#divide screenshot into cells
cells = []
for y in range(0, 6):
    for x in range(0, 6):
        cell_box = (x*cell_size[0], y*cell_size[1], (x+1)*cell_size[0], (y+1)*cell_size[1])
        cell = img.crop(cell_box)
        cells.append(cell)

#divide into individual cells

i = 0
for cell in cells:
    s = 'cell{n}.bmp'
    cell_name = s.format(n = i)
    cell.save(cell_name)
    i += 1


#train the recognizer
print('loading recognizer...')
recognizer = ImgRecognizer()

print('training recognizer...\n')
recognizer.train()



game_board = np.zeros((board_size, board_size), dtype=np.int32)
for y in range(0, 6):
    for x in range(0, 6):
        cells = []
        cell_box = (x*cell_size[0], y*cell_size[1], (x+1)*cell_size[0], (y+1)*cell_size[1])
        cell = img.crop(cell_box)
        cells.append(cell)
        #cell.show()
        pred = recognizer.predict(cell)
        game_board[y][x] = pred
        print(pred, ' ', end='')
    print('\n')
