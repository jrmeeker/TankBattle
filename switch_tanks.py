import win32api, win32con
import time
import ctypes
import random as ran
import pyautogui
import math

g_pos = (817, 982)
repair_pos = 950, 715
first_pos = (450, 930)
second_pos = (680, 931)
third_pos = (980, 939)
fourth_pos = (1280, 932)
repair_all_pos = (951, 652)
NUM_TANKS = 25
ERROR_MARGIN = 2
positions = [first_pos, second_pos, third_pos, fourth_pos]
exit_pos = (434,322)

#mouse click function
def click(x, y):
    pyautogui.moveTo(x, y, 0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.31)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

#click and drag mouse function
def click_n_drag(x, y):
    #win32api.SetCursorPos((x, y))
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.05)
    pyautogui.mouseDown()
    #time.sleep(.05)
    #pyautogui.mouseDown()
    #time.sleep(.05)
    #pyautogui.mouseDown()
    time.sleep(0.31)
    #win32api.SetCursorPos((x - 300, y))
    pyautogui.moveTo(x, y, 1.35)
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    pyautogui.mouseUp()

#open garage
def open_garage():
    pyautogui.moveTo(g_pos[0], g_pos[1], 0.65)
    pyautogui.click(g_pos[0] + ran.randint(1, 18), g_pos[1] + ran.randint(1, 18))

#repair
def repair():
    pyautogui.moveTo(repair_pos[0], repair_pos[1], 0.35)
    pyautogui.click(repair_pos[0], repair_pos[1])
    #pyautogui.click(repair_pos[0], repair_pos[1])
    #pyautogui.click(repair_pos[0], repair_pos[1])

#select first tank
def select_first():
    pyautogui.moveTo(first_pos[0], first_pos[1], 0.25)
    pyautogui.click(first_pos[0], first_pos[1])

#select second tank
def select_second():
    pyautogui.moveTo(second_pos[0], second_pos[1], 0.25)
    pyautogui.click(second_pos[0], second_pos[1])

#select third tank
def select_third():
    pyautogui.moveTo(third_pos[0], third_pos[1], 0.25)
    pyautogui.click(third_pos[0], third_pos[1])

#select fourth tank
def select_fourth():
    pyautogui.moveTo(fourth_pos[0], fourth_pos[1], 0.25)
    pyautogui.click(fourth_pos[0], fourth_pos[1])
    #pyautogui.click(fourth_pos[0], fourth_pos[1])
    #pyautogui.click(fourth_pos[0], fourth_pos[1])

#scroll to next tank
def scroll_next():
    time.sleep(.2)
    pyautogui.moveTo(fourth_pos[0], fourth_pos[1], .2)
    pyautogui.mouseDown()
    time.sleep(.4)
    click_n_drag(fourth_pos[0] - 210, fourth_pos[1])

#select and repair a tank given a position (1-4)
def select_and_repair(x, y):
    pyautogui.moveTo(x, y, 0.75)
    #win32api.SetCursorPos((x, y))
    time.sleep(.2)
    pyautogui.click(x, y)
    #pyautogui.click(x, y)
    time.sleep(.23)
    repair()

#select and repair tank in last position
def click_drag_repair():
    scroll_next()
    time.sleep(.2)
    #select_fourth()
    pyautogui.moveTo(fourth_pos[0] - 80, fourth_pos[1], 0.25)
    pyautogui.click(fourth_pos[0] - 80, fourth_pos[1])
    time.sleep(0.2)
    pyautogui.moveTo(repair_pos[0], repair_pos[1], 0.25)
    repair()

#repair all tanks sequence
def repair_fleet(tanks):
    #select and repair first four tanks

    for pos in positions:
        select_and_repair(pos[0], pos[1])
        time.sleep(3)

    #repair remaining tanks
    for i in range(tanks + ERROR_MARGIN):
        click_drag_repair()
        time.sleep(3.5)


    #repair last tank in case it was missed
    pyautogui.moveTo(1384, 958, 0.25)
    select_and_repair(1384, 958)

#scroll back to first tank
def scroll_to_first():
    for i in range(math.ceil(NUM_TANKS / 3)):
        pyautogui.moveTo(first_pos[0], first_pos[1], 0.25)
        pyautogui.mouseDown()
        #pyautogui.mouseDown()
        time.sleep(.4)
        pyautogui.moveTo(1559, 949, 0.25)
        pyautogui.mouseUp()

#switch to next tank from main screen
def next_tank():
    open_garage()
    #win32api.SetCursorPos(second_pos)
    pyautogui.moveTo(second_pos[0], second_pos[1], 0.25)
    pyautogui.mouseDown()
    #pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.moveTo(first_pos[0] - 20, first_pos[1], 1)
    pyautogui.mouseUp()
    time.sleep(0.1)
    pyautogui.moveTo(fourth_pos[0] + 100, fourth_pos[1], 0.25)
    time.sleep(0.1)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()
    leave_garage()

#leave garage
def leave_garage():
    pyautogui.moveTo(exit_pos[0], exit_pos[1], 0.65)
    pyautogui.mouseDown()
    time.sleep(0.12)
    pyautogui.mouseUp()

#handle all garage events
def prep_all_from_home_screen(tanks):
    open_garage()
    time.sleep(1.63)
    repair_fleet(tanks)
    scroll_to_first()
    time.sleep(1.5)
    select_first()
    leave_garage()
    return

#repair all tanks using "Repair all tanks" button
def click_repair_all():
    pyautogui.moveTo(repair_all_pos[0], repair_all_pos[1], 0.25)
    pyautogui.click(repair_all_pos[0], repair_all_pos[1])

    #wait for metamask to open
    time_wait = 40
    time.sleep(time_wait)
    print('waiting ' + str(time_wait) + ' seconds for metamask to open...')

    #scroll down
    pyautogui.moveTo(1910, 685, 0.25)
    pyautogui.click(1910, 685)
    time.sleep(3)

    #click on confirm
    pyautogui.moveTo(1790, 707, 0.25)
    pyautogui.click(1790, 707)


################################################################################
if __name__ == "__main__":
    #driver code
    #repair_fleet()
    #prep_all_from_home_screen()

    for i in range(NUM_TANKS - 4):
        next_tank()

        #for i in range(5):
        #click_drag_repair()
