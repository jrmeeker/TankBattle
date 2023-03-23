import numpy as np
#import cv2
import pyautogui
from PIL import Image
from PIL import ImageGrab
from sklearn_decoder import ImgRecognizer
from sklearn_turn_decoder import ImgRecognizer2
from sklearn_victory_decoder import ImgRecognizer4
from sklearn_speed_decoder import ImgRecognizer5
from switch_tanks import *
import win32api, win32con
import time
import random
import sys
#import debug_utils as dbg
#import simple_solver
#import cProfile
#import pstats

NUM_TANKS = 35

debug = False

def grab_board():
    global game_board
    cells = []

    if debug:
        img = Image.open('capture.bmp')
    else:
        img = ImageGrab.grab()
        img = img.crop(board_box)
        #img.save('capture.bmp')

    for y in range(0, 6):
        for x in range(0, 6):
            cell_box = (x*cell_size[0], y*cell_size[1], (x+1)*cell_size[0], (y+1)*cell_size[1])
            cell = img.crop(cell_box)
            cells.append(cell)
            #cell.show()
            pred = recognizer.predict(cell)
            game_board[y][x] = pred
            if debug:
                print(pred, ' ', end='')
            #time.sleep(5)
        if debug:
            print('\n')

    #set breakpoint
    #import pdb; pdb.set_trace()

    if debug:
        save_cells(cells)


    return img

def save_cells(cells):
    i = 0
    for cell in cells:
        s = 'cell{n}.bmp'
        cell_name = s.format(n = i)
        cell.save(cell_name)
        i += 1

def check_right(x, y):
    #check neighbor to the right
    cell_val = game_board[x, y]
    right_index = y + 1

    #make sure neighbor is valid cell
    if 0 <= right_index <= 5:
        #extract value from cell
        right_cell_val = game_board[x, right_index]

        #check for match
        if cell_val == right_cell_val:

            #if two in row, check kitty corner neighbors
            check_x, check_y = x + 1, y + 2

            #make sure checked cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(x, check_y), (check_x, check_y)]

            #check x - 1
            check_x = x - 1

            #make sure checked cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(x, check_y), (check_x, check_y)]

            #check 3 to the right
            check_x, check_y = x, y + 3

            #make sure checked cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(x, y + 2), (x, y + 3)]

    #no move found
    return False, None

def check_left(x, y):
    #check neighbor to the left
    cell_val = game_board[x, y]
    left_index = y - 1

    #make sure neighbor is valid cell
    if 0 <= left_index <= 5:
        #extract value from left neighbor
        left_cell_val = game_board[x, left_index]

        #check for match
        if cell_val == left_cell_val:

            #if two in row, check kitty corner neighbors
            check_x, check_y = x - 1, y - 2

            #make sure cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(x, check_y), (check_x, check_y)]

            #check x + 1
            check_x = x + 1

            #make sure cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(x, check_y), (check_x, check_y)]

            #check third to the left
            check_x, check_y = x, y - 3

            #make sure cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(x, y - 2), (x , y - 3)]


    return False, None

def check_up(x, y):
    #check neighbor above
    cell_val = game_board[x, y]
    up_index = x - 1

    #make sure index is valid
    if 0 <= up_index <= 5:
        #get cell value
        up_cell_val = game_board[up_index, y]

        #check for match
        if cell_val == up_cell_val:

            #two in row, check kitty corner neighbors
            check_x, check_y = x - 2, y - 1

            #make sure cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, y), (check_x, check_y)]

            #check y + 1
            check_y = y + 1

            #make sure cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, y), (check_x, check_y)]

            #check third upward
            check_x, check_y = x - 3, y

            #make sure cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(x - 2, y), (x - 3, check_y)]

    return False, None

def check_down(x, y):
    #check neighbor below
    cell_val = game_board[x, y]
    down_index = x + 1

    #make sure index is valid
    if 0 <= down_index <= 5:
        #get cell value
        down_cell_val = game_board[down_index, y]

        #check for match
        if cell_val == down_cell_val:

            #two in a row, check kitty corner neighbors
            check_x, check_y = x + 2, y - 1

            #make sure cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, y), (check_x, check_y)]

            #check y + 1
            check_y = y + 1

            #make sure cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, y), (check_x, check_y)]

            #check third downward
            check_x, check_y = x + 3, y

            #make sure cell is valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(x + 2, y), (x + 3, y)]

    return False, None

def check_two_right(x, y):
    #extract cell value and index to check
    cell_val = game_board[x, y]
    two_right_index = y + 2

    #make sure index is valid
    if 0 <= two_right_index <= 5:
        #extract value from cell
        right_cell_val = game_board[x, two_right_index]

        #check for match
        if cell_val == right_cell_val:

            #if match, check nearest neighbor up
            check_x, check_y = x - 1, y + 1

            #make sure indices are valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, check_y), (x, check_y)]

            #check x + 1, nearest neighbor down
            check_x = x + 1

            #make sure indices are valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, check_y), (x, check_y)]

    return False, None

def check_two_left(x, y):
    #extract cell value and index to check
    cell_val = game_board[x, y]
    two_left_index = y - 2

    #make sure index is valid
    if 0 <= two_left_index <= 5:
        #extract value from cell
        left_cell_val = game_board[x, two_left_index]

        #check for match
        if cell_val == left_cell_val:

            #if match, check nearest neighbor up
            check_x, check_y = x - 1, y - 1

            #make sure indices are valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, check_y), (x, check_y)]

            #check x + 1, nearest neighbor down
            check_x = x + 1

            #make sure indices are valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, check_y), (x, check_y)]

    return False, None

def check_two_up(x, y):
    #get value
    cell_val = game_board[x, y]
    up_index = x - 2

    #make sure index is valid
    if 0 <= up_index <= 5:
        #get cell value
        up_cell_val = game_board[up_index, y]

        #check for match
        if cell_val == up_cell_val:

            #if match, check nearest neighbor to left
            check_x, check_y = x - 1, y - 1

            #make sure indices are valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, y), (check_x, check_y)]

            #check y + 1, nearest neighbor to the right
            check_y = y + 1

            #make sure indices are valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, check_y), (x - 1, y)]

    return False, None

def check_two_down(x, y):
    #get value
    cell_val = game_board[x, y]
    down_index = x + 2

    #make sure index is valid
    if 0 <= down_index <= 5:
        #get cell value
        down_cell_val = game_board[down_index, y]

        #check for match
        if cell_val == down_cell_val:

            #if match, check nearest neighbor to left
            check_x, check_y = x + 1, y - 1

            #make sure indices are valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, check_y), (check_x, y)]

            #check y+ 1, nearest neighbor to the right
            check_y = y + 1

            #make sure indices are valid
            if 0 <= check_x <= 5 and 0 <= check_y <= 5:

                #if cell is a match, return move
                if game_board[check_x, check_y] == cell_val:
                    return True, [(check_x, check_y), (check_x, y)]

    return False, None

functions_list = [check_right, check_left, check_up, check_down,
                    check_two_right, check_two_left, check_two_up,
                        check_two_down]

def solver(functions):
    start = random.randint(0, board_size - 1)
    for i in range(start, board_size):
        for j in range(board_size):
            for function in functions_list:
                move_found, move = function(i, j)
                if move_found:
                    return move

    for i in range(board_size):
        for j in range(board_size):
            for function in functions_list:
                move_found, move = function(i, j)
                if move_found:
                    return move

def generate_mapping():
    coordinate_map = dict()
    #old map
    #y = [767, 838, 910, 982, 1054, 1126]
    #x = [476, 551, 621, 695, 766, 844]

    #new map
    #y = [785, 850, 916, 981, 1046, 1112]
    #x = [502, 567, 633, 698, 764, 826]

    #new map #2
    y = [759, 838, 911, 989, 1066, 1138]
    x = [511, 589, 660, 741, 810, 892]

    for i in range(board_size):
        for j in range(board_size):
            coordinate_map[(i, j)] = (y[j], x[i])
    return coordinate_map

#moues click function
def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.08)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

#go to garage
def open_garage():
    pyautogui.moveTo(814, 984, 0.3)
    click(814, 984)

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
    pyautogui.moveTo(shield_pos[0], shield_pos[1], 0.25)
    pyautogui.click(shield_pos[0], shield_pos[1])


board_size = 6
#original board box
#board_box = (768, 381, 1142, 770)

#new board box
board_box, board_box2 = (720, 465, 1186, 927), (764,633,1155,683)
board_box3, board_box4 = (1453,959,1551,979), (848, 566, 1051, 610)
board_box5 = (400, 900, 460, 927)

img_size = (board_box[2]-board_box[0], board_box[3]-board_box[1])
cell_size = (img_size[0]/6, img_size[1]/6)
game_board = np.zeros((board_size, board_size), dtype=np.int32)
cells = []
map = generate_mapping()


#################### SHOWTIME ##################################################
#train learner then wait for input
print('TRAINING AI...')
recognizer, turn_recognizer = ImgRecognizer(), ImgRecognizer2()
victory_recognizer, speed_recognizer = ImgRecognizer4(), ImgRecognizer5()

recognizer.train(), turn_recognizer.train()
victory_recognizer.train(), speed_recognizer.train()

#button positions
battle_pos, rockets_pos, lightning_pos, shield_pos = (1451, 954), (1085, 923), (818, 918), (952, 921)

#prepare fleet
print('PREPARING FLEET...')
#if len(sys.argv) < 2:
    #prep_all_from_home_screen(NUM_TANKS + 4)                  ### UNCOMMENT BEFORE RUNNING FROM BEGINNING!!!! ############################
#input('FLEET READY -- PRESS ENTER TO JOIN BATTLE')
print('FLEET READY!')
time.sleep(2)

#track wins and losses
wins, losses = 0, 0

#start time
start_time = time.time()

#index to start from
if len(sys.argv) < 2:
    START_INDEX = 0
else:
    START_INDEX = int(sys.argv[1])

#START = 13
#NUM_TANKS = 1
#battle every tank one-by-one
for i in range(START_INDEX, NUM_TANKS + 2):

    if i > 0:
        pyautogui.moveTo(g_pos[0], g_pos[1], 0.65)
        #open_garage()
        time.sleep(2.5)

        '''
        if i == 1:
            print('SELECT SECOND')
            select_second()
            leave_garage()
        elif i == 2:
            print('SELECT THIRD')
            select_third()
            leave_garage()
        elif i == 3:
            print('SELECT FOURTH')
            select_fourth()
            leave_garage()
        else:
            print('NEXT TANK')
            next_tank()
        '''


    for i in range(5):
        print('ENTERING BATTLE')

        #enter battle and wait
        enter_battle()
        time.sleep(1)

        #click on PVE
        click(517, 698)  #ADDED THIS IN 7/7/2022 TO CLICK ON PVE MODE

        time.sleep(3)

        #track if time has been adjusted or not for timing purposes
        time_adjusted = False

        #check speed, fix if wrong
        '''for i in range(2):
            speed = ImageGrab.grab()
            speed = speed.crop(board_box5)
            speed_pred = speed_recognizer.predict(speed)
            print('speed_pred:', speed_pred)
            if speed_pred == 0 or speed_pred == 1:
                time_adjusted = True
                pyautogui.moveTo(429, 913, 0.15)
                click(429, 913)
                time.sleep(.1)'''

        if not time_adjusted:
            time.sleep(1)

        #powerups list
        powerups = [click_rockets, click_lightning, click_shield]

        #one loop for each starting power up
        for i in range(10):

            #input('YOUR TURN -- PRESS ENTER')
            if i > 0:
                c = 0
                your_turn = False
                while not your_turn and c < 65:
                    time.sleep(.25)
                    img2 = ImageGrab.grab()
                    img2 = img2.crop(board_box2)
                    pred2 = turn_recognizer.predict(img2)
                    if pred2 == 0:
                        print('YOUR TURN')
                        time.sleep(1)
                        your_turn = True
                    else:
                        print('.')
                    c += 1

            time.sleep(.5)

            #select power up
            if i < 3:
                powerups[i]()
                time.sleep(3)

            #set start time
            t0 = time.time()
            t1 = time.time()
            t = t1 - t0


            #detect if battle over
            img4 = ImageGrab.grab()
            img4 = img4.crop(board_box4)
            pred4 = victory_recognizer.predict(img4)
            game_over = False
            if pred4 == 0:
                print('VICTORY')
                wins += 1
                game_over = True
                break
            elif pred4 == 1:
                print('DEFEAT')
                losses += 1
                game_over = True
                break
            else:
                print('BATTLE CONTINUES...')


            #puzzle solve for 12 seconds
            while(t < 12):
                capture = grab_board()
                move = solver(functions_list)
                try:
                    click1, click2 = map[move[0]], map[move[1]]
                    click(click1[0], click1[1])
                    click(click1[0], click1[1])
                    time.sleep(.01)
                    click(click2[0], click2[1])
                    click(click2[0], click2[1])
                except:
                    pass
                t1 = time.time()
                t = t1 - t0
                time.sleep(0.01)

            #wait for round to end
            if i < 2:
                for t in range(15):
                    time.sleep(1)
                    print(t, 'seconds passed')

            #detect if battle over
            img4 = ImageGrab.grab()
            img4 = img4.crop(board_box4)
            pred4 = victory_recognizer.predict(img4)
            game_over = False
            if pred4 == 0:
                print('VICTORY')
                wins += 1
                game_over = True
                break
            elif pred4 == 1:
                print('DEFEAT')
                losses += 1
                game_over = True
                break
            else:
                print('BATTLE CONTINUES...')

        #return to home screen
        if game_over:
            pyautogui.moveTo(1500, 970, 0.45)
            click(1500, 970)
            time.sleep(15)
            print('WINS:', wins)
            print('LOSSES:', losses)


    ###### TANK HAS FINISHED ALL 5 BATTLES ###########
    #get next tank from garage
    print('SWITCHING TANKS...')
    next_tank()
    time.sleep(4)

print('\n\nTHE WAR IS OVER!!!!!!!')
print('BATTLES WON: ', wins)
print('BATTLES LOST:', losses)

#end time
end_time = time.time()
elapsed_time = end_time - start_time

#total battle time
print('TOTAL BATTLE TIME:', elapsed_time)
print('TIME PER TANK:', elapsed_time / NUM_TANKS)


















#capture.save('cropped_board.bmp')

#img = cv2.imread('captured_board1.bmp')
#img = cv2.imread(img)
#rows, cols, _ = img.shape
#print("Rows", rows)
#print("Cols", cols)

#crop the image
#cut_image = img[436:880, 728:1172]
#img = img.crop((728, 436, 1172, 880))
#img.show()

#cv2.imshow("Cut image", cut_image)
#cv2.imshow("image", img)
#cv2.waitKey(0)
