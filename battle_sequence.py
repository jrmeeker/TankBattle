import numpy as np
#import cv2
import pyautogui
from PIL import Image
from PIL import ImageGrab
from sklearn_decoder import ImgRecognizer
import win32api, win32con
import time
import random
from switch_tanks import *
from fight_actions import *

battle_pos = (1451, 954)
rockets_pos = (1085, 923)
lightning_pos = (818, 918)
shield_pos = (952, 921)

#click on BATTLE
def enter_battle():
    pyautogui.moveTo(battle_pos[0], battle_pos[1], 0.65)
    pyautogui.click(battle_pos[0], battle_pos[1])

#select ultimate rocket power up
def click_rockets():
    pyautogui.moveTo(rockets_pos[0], rockets_pos[1], 0.15)
    pyautogui.click(rockets_pos[0], rockets_pos[1])

#select lightning power up
def click_lightning():
    pyautogui.moveTo(lightning_pos[0], lightning_pos[1], 0.15)
    pyautogui.click(lightning_pos[0], lightning_pos[1])

#select shield power up
def click_shield():
    pyautogui.moveTo(shield_pos[0], shield_pos[1], 0.1)
    pyautogui.click(lightning_pos[0], lightning_pos[1])

#powerups list
powerups = [click_rockets, click_lightning, click_shield]

#battle sequence
enter_battle()
time.sleep(8)

#one loop for each starting power up
for i in range(3):

    #select power up
    powerups[i]
    time.sleep(3)

    #set start time
    t0 = time.time()
    t1 = time.time()
    t = t1 - t0

    #puzzle solve for 12 seconds
    while(t < 12):
        capture = grab_board()
        move = solver(functions_list)
        try:
            click1, click2 = map[move[0]], map[move[1]]
            click(click1[0], click1[1])
            click(click1[0], click1[1])
            time.sleep(.03)
            click(click2[0], click2[1])
        except:
            pass
        t1 = time.time()
        t = t1 - t0
        time.sleep(0.12)

    #wait for round to end
    time.sleep(45)
