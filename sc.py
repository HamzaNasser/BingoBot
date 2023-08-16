import pyautogui as py
import numpy as np
import time
import keyboard
from paddleocr import PaddleOCR
import re

def find_best_bingo_move(grid):
    winning_patterns = [
        [0, 1, 2, 3, 4],   # Top row
        [5, 6, 7, 8, 9],   # Second row
        [10, 11, 12, 13, 14],  # Third row
        [15, 16, 17, 18, 19],  # Fourth row
        [20, 21, 22, 23, 24],  # Fifth row
        [0, 5, 10, 15, 20],  # First column
        [1, 6, 11, 16, 21],  # Second column
        [2, 7, 12, 17, 22],  # Third column
        [3, 8, 13, 18, 23],  # Fourth column
        [4, 9, 14, 19, 24],  # Fifth column
        [0, 6, 12, 18, 24],  # Diagonal from top-left to bottom-right
        [4, 8, 12, 16, 20]   # Diagonal from top-right to bottom-left
    ]
    
    potential_best_moves = []  # Maintain a list of potential best moves
    max_matches = 0
    
    for move in range(25):
        if grid[move] == 'X':
            continue
        
        num_matches = 0
        for pattern in winning_patterns:
            if move in pattern:
                matches = sum(1 for index in pattern if grid[index] == 'X')
                if matches > num_matches:
                    num_matches = matches
        
        if num_matches >= max_matches:  # Use >= to account for cases with multiple potential best moves
            max_matches = num_matches
            potential_best_moves.append(move)
    
    # Sort the potential best moves by the number of matches
    potential_best_moves.sort(key=lambda move: -max_matches)
    
    return potential_best_moves[:4]  # Return the top 4 potential best moves

# ANSI escape codes for text colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"

a = time.time()
ocr = PaddleOCR(show_log = False, max_text_length=3, det_db_score_mode='fast', det=True, rec=True, cls=True, det_db_thresh=0.5, use_gpu=True, ocr=True, lang='en', use_angle_cls=True ) # need to run only once to load model into memory

print("Starting ... ")

cords = [(755, 375), (855, 375), (955, 375), (1055, 375), (1155, 375), (755, 475), (855, 475), (955, 475), (1055, 475), (1155, 475), (755, 575), (855, 575), (0,0),(1055, 575), (1155, 575), (755, 675), (855, 675), (955, 675), (1055, 675), (1155, 675), (755, 775), (855, 775), (955, 775), (1055, 775), (1155, 775)]


def currentValue(image):
    result = ocr.ocr(np.array(image), cls=True)
    # Extract and print the detected digits
    if result:
        for idx in range(len(result)):
                res = result[idx]
                for line in res:
                    res = ''.join(re.findall(r'[BIiNGOo0-9]', line[-1][0]))
                    return res
    return "-"

def read_value_from_image(image1):
    # Load the image using OpenCV
    result = ocr.ocr(np.array(image1))
    listOfNumebrs = []
    # Extract and print the detected digits
    for idx in range(len(result)):
            res = result[idx]
            for line in res:
                listOfNumebrs.append(line[-1][0])
    
    return listOfNumebrs

def check(grid, newgrid):
    for i in grid:
        if i not in newgrid:
            index = grid.index(i)
            grid[index] = "X"
    return grid


input("Press Entre... ")

detected_digits = read_value_from_image(py.screenshot(region=(733, 340 , 470, 470)))

print("Start to detect ", time.time() - a, " time taken!")

#print(detected_digits)

grid = detected_digits
grid.insert(12, "X")
print(grid)

while keyboard.is_pressed('ctrl') != True:
    s = time.time()

    now_value = currentValue(py.screenshot(region=((1108, 214, 57, 35))))
    if now_value in grid:
        py.click(cords[grid.index(now_value)])
        print("Found a Value in:", GREEN + now_value + RESET, "in:", "{:.2f}".format(time.time() - s))
        grid.insert(grid.index(now_value), ('X'))
        grid.pop(grid.index(now_value))
        #print(grid)
        grid = check(grid, read_value_from_image(py.screenshot(region=(733, 340 , 470, 470))))
        best = find_best_bingo_move(grid)
        if best is not None:
            for i, k in enumerate(best):
                print("\033[93m" + grid[k] + "\033[0m", end=" ")
            print()
        time.sleep(0.10)
    time.sleep(0.30)
