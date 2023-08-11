import cv2
import easyocr
import pyautogui as py
import numpy as np
import threading


cords = [(755, 375), (855, 375), (955, 375), (1055, 375), (1155, 375),
         (755, 475), (855, 475), (955, 475), (1055, 475), (1155, 475),
         (755, 575), (955, 575), (1055, 575), (1155, 575),
         (755, 675), (855, 675), (955, 675), (1055, 675), (1155, 675),
         (755, 775), (855, 775), (955, 775), (1055, 775), (1155, 775)]

# Load the EasyOCR reader
reader = easyocr.Reader(lang_list=['en'])

# Load images
bingo_image = cv2.cvtColor(cv2.imread("C:\\Users\\shbat\\Desktop\\project\\bingo.png"), cv2.COLOR_BGR2GRAY)
extra_image = cv2.imread("C:\\Users\\shbat\\Desktop\\project\\extra.png", cv2.IMREAD_GRAYSCALE)
choose_image = cv2.imread("C:\\Users\\shbat\\Desktop\\project\\choose.png", cv2.IMREAD_GRAYSCALE)
time_image = cv2.imread("C:\\Users\\shbat\\Desktop\\project\\time.png", cv2.IMREAD_GRAYSCALE)
print("About to Start ... ")
def compare_images():
    region = np.array(py.screenshot(region=(905, 840, 80, 100)))
    region_gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    
    templates = [(extra_image, (940, 894)), (choose_image, (940, 894)), (time_image, (940, 894))]
    
    found_templates = []
    
    for template, coords in templates:
        result = cv2.matchTemplate(region_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        
        if max_val >= 0.8:
            found_templates.append((coords[0], coords[1]))  # Save the coordinates
    
    if len(found_templates) > 0:
        check_bingo_thread = threading.Thread(target=check_bingo)
        check_bingo_thread.start()
    
        for coords in found_templates:
            click_thread = threading.Thread(target=py.click, args=coords)
            click_thread.start()

def check_bingo():
    result = cv2.matchTemplate(cv2.cvtColor(np.array(py.screenshot(region=(1010, 840, 80, 100))), cv2.COLOR_BGR2GRAY), bingo_image, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    if max_val > 0.8:
        py.click(1024, 890)

def currentValue(image):
    results = reader.readtext(np.array(image))
    if results:
        extracted_text = results[0][1]
    else:
        extracted_text = 'X'
    return extracted_text

def read_value_from_image(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform thresholding to convert the image to black and white
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV)

    # Perform text detection using EasyOCR
    results = reader.readtext(binary_image)

    # Extract and print the detected digits
    detected_digits = []
    now_value = currentValue(py.screenshot(region=(1110, 212, 50, 35)))
    
    for (bbox, text, prob) in results:
        x_min, y_min = map(int, bbox[0])
        x_max, y_max = map(int, bbox[2])
        detected_digits.append((text, (x_min, y_min, x_max, y_max)))
    
    for i, (text, _) in enumerate(detected_digits):
        if text is not None and now_value == text:
            print("Found a Value:", text)
            py.click(cords[i][0], cords[i][1])
            break

print("Start to detect")
screenshot_region = py.screenshot(region=(733, 340, 470, 470))
screenshot_region.save("C:\\Users\\shbat\\Desktop\\project\\1.png")

while True:
    read_value_from_image(cv2.imread("C:\\Users\\shbat\\Desktop\\project\\1.png"))