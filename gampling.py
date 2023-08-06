import pyautogui as py
import pytesseract
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


 # x, y coords of each square on the board
b_coordinates = [(770, 401), (770, 501), (770, 601), (770, 701), (770, 801)]
i_coordinates = [(870, 401), (870, 501), (870, 601), (870, 701), (870, 801)]
n_coordinates = [(970, 401), (970, 501), (970, 601), (970, 701), (970, 801)]
g_coordinates = [(1070, 401), (1070, 501), (1070, 601), (1070, 701), (1070, 801)]
o_coordinates = [(1170, 401), (1170, 501), (1170, 601), (1170, 701), (1170, 801)]


# Path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Perform OCR to extract text from the image
def read_value_from_image(image):
    # Read the image using pytesseract
    extracted_text = pytesseract.image_to_string(image, config='--oem 3 --psm 6 outputbase alphanumeric')

    # Return the extracted text as the result and add it to the proper list B I N G O
    return ''.join(re.findall(r'[BINGO0-9]', extracted_text))

def save_character_screenshots(character, x, y, width, height):
    extracted_values = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(read_value_from_image, py.screenshot(region=(x, y + (i - 1) * 95, width, height))) for i in range(1, 6)]
        for future in as_completed(futures):
            value = future.result()
            extracted_values.append(value)
    return extracted_values

# Measure the start time
start_time = time.time()

# B
b_list = save_character_screenshots("B", 740, 375, 70, 66)

# I
i_list = save_character_screenshots("I", 830, 370, 70, 70)

# N
n_list = save_character_screenshots("N", 924, 370, 70, 70)

# O
o_list = save_character_screenshots("O", 1120, 370, 70, 70)

# G
g_list = save_character_screenshots("G", 1020, 370, 70, 70)

def click_curr_value():
    now_value = read_value_from_image(py.screenshot(region=(1100, 200, 75, 75)))
    letter = now_value[0]
    now_value = now_value[1:]
    if letter == "B":
        if now_value in b_list:
            py.click(b_coordinates[b_list.index(now_value)])
    if letter == "I":
        if now_value in i_list:
            py.click(i_coordinates[i_list.index(now_value)])
    if letter == "N":
        if now_value in n_list:
            py.click(n_coordinates[n_list.index(now_value)])
    if letter == "G":
        if now_value in g_list:
            py.click(g_coordinates[g_list.index(now_value)])
    if letter == "O":
        if now_value in o_list:
            py.click(o_coordinates[o_list.index(now_value)])  
    return letter, now_value




click_curr_value()

# Calculate the time taken
print("Total Execution Time:", (time.time() - start_time), "seconds")