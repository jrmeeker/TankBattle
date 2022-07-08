import numpy as np
#import cv2
#import pyautogui
from PIL import Image
from PIL import ImageGrab
from sklearn_decoder import ImgRecognizer
#import win32api, win32con
#import time
#import debug_utils as dbg
#import simple_solver
#import cProfile
#import pstats

debug = True

def grab_board():
    global game_board
    if debug:
        img = Image.open('board.bmp')
    else:
        img = ImageGrab.grab()
        img = img.crop(board_box)
        img.save('board.bmp')


    for y in range(0, 6):
        for x in range(0, 6):
            cell_box = (x*cell_size[0], y*cell_size[1], (x+1)*cell_size[0], (y+1)*cell_size[1])
            cell = img.crop(cell_box)
            cells.append(cell)
            #cell.show()
            pred = recognizer.predict(cell)
            game_board[y][x] = pred
            print(pred, ' ', end='')
        print('\n')


    return img

def save_cells():
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
            print('MATCH')
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
            print('MATCH')
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
                    return True, [(check_x, check_y), (x, check_y)]

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
    for i in range(board_size):
        for j in range(board_size):
            for function in functions_list:
                move_found, move = function(i, j)
                if move_found:
                    return move

board_size = 6
board_box = (728, 436, 1172, 880)
img_size = (board_box[2]-board_box[0], board_box[3]-board_box[1])
cell_size = (img_size[0]/6, img_size[1]/6)
game_board = np.zeros((board_size, board_size), dtype=np.int32)
recognizer = ImgRecognizer()
cells = []


#main code
#train learner then wait for input
recognizer.train()

#pause and prompt user
input('Press Enter when game board is ready:')

#capture game board
capture = grab_board()
#capture.show()
print(solver(functions_list))
























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
