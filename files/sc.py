import easyocr
import numpy as np
import pyautogui as py

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Constants
B_PIXEL_VALUE = 220
I_PIXEL_VALUE = 39
N_PIXEL_VALUES = 100
G_PIXEL_VALUE = 223
O_PIXEL_VALUE = 80

# Coordinates of each square on the board
b_coordinates = [(770, 401), (770, 501), (770, 601), (770, 701), (770, 801)]
i_coordinates = [(870, 401), (870, 501), (870, 601), (870, 701), (870, 801)]
n_coordinates = [(970, 401), (970, 501), (970, 601), (970, 701), (970, 801)]
g_coordinates = [(1070, 401), (1070, 501), (1070, 601), (1070, 701), (1070, 801)]
o_coordinates = [(1170, 401), (1170, 501), (1170, 601), (1170, 701), (1170, 801)]

def checkBingo():
    if py.pixel(1110, 930)[0] == 251:
        py.click(1110, 930)

def update_list(value, value_list):
    if value in value_list:
        curr_index = value_list.index(value)
        value_list.pop(curr_index)
        value_list.insert(curr_index, "X")
        print(f"{value} value found, Value list: {value_list}")


def read_value_from_image(image):
    results = reader.readtext(np.array(image))
    print(results)
    if results:
        extracted_text = results[0][1]
    else:
        extracted_text = 'X'
    return extracted_text


def save_character_screenshots(character, x, y, width, height):
    extracted_values = []
    for i in range(1, 6):
        value = read_value_from_image(py.screenshot(region=(x, y + (i - 1) * 95, width, height)))
        extracted_values.append(value)
    return extracted_values


# Initialize value lists
b_list = save_character_screenshots("B", 735, 340, 55, 60)
i_list = save_character_screenshots("I", 830, 370, 70, 70)
n_list = save_character_screenshots("N", 924, 370, 70, 70)
o_list = save_character_screenshots("O", 1120, 370, 70, 70)
g_list = save_character_screenshots("G", 1020, 370, 70, 70)


def click_and_update(pixel_value, value_list, coord_list, now_value):
    if py.pixel(1129, 285)[0] == pixel_value and now_value in value_list and now_value != "X":
        py.click(coord_list[value_list.index(now_value)])
        update_list(now_value, value_list)


def click_curr_value():
    now_value = read_value_from_image((py.screenshot(region=(1110, 212, 50, 35))))
    print(b_list)
    click_and_update(B_PIXEL_VALUE, b_list, b_coordinates, now_value)
    click_and_update(I_PIXEL_VALUE, i_list, i_coordinates, now_value)
    click_and_update(G_PIXEL_VALUE, g_list, g_coordinates, now_value)
    click_and_update(O_PIXEL_VALUE, o_list, o_coordinates, now_value)
    click_and_update(N_PIXEL_VALUES, n_list, n_coordinates, now_value)
    return now_value

print("Detecting now .. ")
while 1:
    click_curr_value()
    checkBingo()
