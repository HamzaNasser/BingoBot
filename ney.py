import cv2
import easyocr
import pyautogui as py
import numpy as np
import time
import keyboard
start_time = time.time()

# Load the EasyOCR reader
reader = easyocr.Reader(lang_list=['en'])

cords = [(755, 375), (855, 375), (955, 375), (1055, 375), (1155, 375), (755, 475), (855, 475), (955, 475), (1055, 475), (1155, 475), (755, 575), (955, 575), (1055, 575), (1155, 575), (755, 675), (855, 675), (955, 675), (1055, 675), (1155, 675), (755, 775), (855, 775), (955, 775), (1055, 775), (1155, 775)]

def currentValue(image):
    results = reader.readtext(np.array(image))
    if results:
        extracted_text = results[0][1]
    else:
        extracted_text = 'X'
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
        detected_digits.append(text)

    return detected_digits

end_time = time.time()
print(end_time - start_time)

print("Start to detect")
py.screenshot(region=(733, 340 , 470, 470)).save("C:\\Users\\shbat\\Desktop\\project\\1.png")
detected_digits = read_value_from_image("C:\\Users\\shbat\\Desktop\\project\\1.png")
print(detected_digits)

while keyboard.is_pressed('ctrl') == False:

    now_value = currentValue((py.screenshot(region=(1110, 212, 50, 35))))
    for i in detected_digits:
        if (now_value == i):
            py.click(cords[detected_digits.index(i)])
            print("Found a Value: ", i)
            detected_digits.insert(detected_digits.index(i),('Fuck'))
            detected_digits.pop(detected_digits.index(i))
            print(detected_digits)
