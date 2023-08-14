import cv2
import easyocr
import pyautogui as py
import numpy as np
import time
import keyboard
import threading
from queue import Queue

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
print("Starting ... ")
# Load the EasyOCR reader
reader = easyocr.Reader(lang_list=['en'])
print("Finish loading ... ")
cords = [(755, 375), (855, 375), (955, 375), (1055, 375), (1155, 375), (755, 475), (855, 475), (955, 475), (1055, 475), (1155, 475), (755, 575), (955, 575), (1055, 575), (1155, 575), (755, 675), (855, 675), (955, 675), (1055, 675), (1155, 675), (755, 775), (855, 775), (955, 775), (1055, 775), (1155, 775)]

def compare_images():
    region = np.array(py.screenshot(region=(905, 840, 80, 100)))
    region_gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    
    template_names = ["extra.png","pick.png"]
    
    for template_name in template_names:
        template_path = "C:\\Users\\shbat\\Desktop\\bot\\" + template_name
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(region_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        
        if max_val >= 0.8:
            py.click(940, 894)
            break  # Click once and break out of the loop


import threading

def currentValue(image):
    result_queue = Queue()

    def sleep_and_read(image):
        time.sleep(0.4)  # Sleep for 1 second
        result = reader.readtext(np.array(image))
        result_queue.put(result)

    thread = threading.Thread(target=sleep_and_read, args=(image,))
    thread.start()
    thread.join()  # Wait for the thread to finish

    if not result_queue.empty():
        result = result_queue.get()
        if result:
            extracted_text = result[0][1]
            return extracted_text
    extracted_text = '-'
    return extracted_text

def read_value_from_image(image1):
    
    # Load the image using OpenCV
    image = cv2.imread(image1)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform thresholding to convert the image to black and white
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV)

    # Perform text detection using EasyOCR
    results = reader.readtext(binary_image)

    # Extract and print the detected digits
    detected_digits = []
    for (bbox, text, prob) in results:
        x_min, y_min = map(int, bbox[0])
        x_max, y_max = map(int, bbox[2])
        detected_digits.append((text, (x_min, y_min, x_max, y_max)))
    
    return detected_digits



print("Start to detect ", time.time() - a, " time taken!")
py.screenshot(region=(733, 340 , 470, 470)).save("C:\\Users\\shbat\\Desktop\\bot\\1.png")

detected_digits = read_value_from_image("C:\\Users\\shbat\\Desktop\\bot\\1.png")

listOfNumebrs = []
for i, k in detected_digits:
    listOfNumebrs.append(i)
    

print(listOfNumebrs)

while keyboard.is_pressed("ctrl") != True:
    s = time.time()
    
    # Capture the current value every 0.5 seconds
    now_value = currentValue(py.screenshot(region=(1110, 212, 50, 35)))
    if now_value in listOfNumebrs:
            py.click(cords[listOfNumebrs.index(now_value)])
            print("Found a Value in:", GREEN + now_value + RESET, "in:", "{:.2f}".format(time.time() - s))
            listOfNumebrs.insert(listOfNumebrs.index(now_value), ('X'))
            listOfNumebrs.pop(listOfNumebrs.index(now_value))
            print(listOfNumebrs)

