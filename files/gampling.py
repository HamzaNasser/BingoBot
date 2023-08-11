import cv2
import easyocr
import pyautogui as py
import numpy as np
import time



cords = [(755, 375), (855, 375), (955, 375), (1055, 375), (1155, 375), (755, 475), (855, 475), (955, 475), (1055, 475), (1155, 475), (755, 575), (955, 575), (1055, 575), (1155, 575), (755, 675), (855, 675), (955, 675), (1055, 675), (1155, 675), (755, 775), (855, 775), (955, 775), (1055, 775), (1155, 775)]



def bingo(): 
    result = cv2.matchTemplate(cv2.cvtColor(np.array(py.screenshot(region=(1010, 840, 80, 100))), cv2.COLOR_BGR2GRAY), cv2.cvtColor(cv2.imread("C:\\Users\\shbat\\Desktop\\project\\bingo.png"), cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    if max_val > 0.9:
        py.click(1024,890)

def compare_images():
    region = np.array(py.screenshot(region=(905, 840, 80, 100)))
    region_gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    
    template_names = ["extra.png", "choose.png", "time.png"]
    
    for template_name in template_names:
        template_path = "C:\\Users\\shbat\\Desktop\\project\\" + template_name
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(region_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        
        if max_val >= 0.8:
            py.click(940, 894)
            break  # Click once and break out of the loop

# Load the EasyOCR reader
reader = easyocr.Reader(lang_list=['en'])

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
        x_min, y_min = map(int, bbox[0])
        x_max, y_max = map(int, bbox[2])
        detected_digits.append((text, (x_min, y_min, x_max, y_max)))
    
    return detected_digits
    



print("Start to detect")

now_value = currentValue((py.screenshot(region=(1110, 212, 50, 35))))

py.screenshot(region=(733, 340 , 470, 470)).save("C:\\Users\\shbat\\Desktop\\project\\1.png")

detected_digits = read_value_from_image("C:\\Users\\shbat\\Desktop\\project\\1.png")


lis = []
for i, k in detected_digits:
    lis.append(i)

print(lis)
while True:
    for i in (lis):
        if (now_value == i):
            py.click(cords[lis.index(i)])
            print("Found a Value: ", i)
            lis.insert(lis.index(i),('Fuck'))
            lis.pop(lis.index(i))
            print(lis)
    now_value = currentValue((py.screenshot(region=(1110, 212, 50, 35))))