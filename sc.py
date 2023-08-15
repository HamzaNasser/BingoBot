import pyautogui as py
import numpy as np
import time
import keyboard
from paddleocr import PaddleOCR
import re


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

cords = [(755, 375), (855, 375), (955, 375), (1055, 375), (1155, 375), (755, 475), (855, 475), (955, 475), (1055, 475), (1155, 475), (755, 575), (855, 575), (1055, 575), (1155, 575), (755, 675), (855, 675), (955, 675), (1055, 675), (1155, 675), (755, 775), (855, 775), (955, 775), (1055, 775), (1155, 775)]


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

input("Press Entre... ")

detected_digits = read_value_from_image(py.screenshot(region=(733, 340 , 470, 470)))

print("Start to detect ", time.time() - a, " time taken!")

print(detected_digits)



while keyboard.is_pressed('ctrl') != True:
    s = time.time()

    now_value = currentValue(py.screenshot(region=((1108, 214, 57, 35))))
    if now_value in detected_digits:
        py.click(cords[detected_digits.index(now_value)])
        print("Found a Value in:", GREEN + now_value + RESET, "in:", "{:.2f}".format(time.time() - s))
        detected_digits.insert(detected_digits.index(now_value), ('X'))
        detected_digits.pop(detected_digits.index(now_value))
        print(detected_digits)
        time.sleep(1.25)
    time.sleep(0.25)


listOfNumebrs = []


while keyboard.is_pressed("ctrl") == True:
    s = time.time()
    
    # Capture the current value every 0.5 seconds the other game currentValue(py.screenshot(region=(1105, 224, 60, 40)))
    now_value = currentValue(py.screenshot(region=(1110, 212, 50, 35)))
    if now_value in listOfNumebrs:
            py.click(cords[listOfNumebrs.index(now_value)])
            print("Found a Value in:", GREEN + now_value + RESET, "in:", "{:.2f}".format(time.time() - s))
            listOfNumebrs.insert(listOfNumebrs.index(now_value), ('X'))
            listOfNumebrs.pop(listOfNumebrs.index(now_value))
            print(listOfNumebrs)

