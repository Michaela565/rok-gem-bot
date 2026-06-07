import pyautogui
import cv2
import numpy as np
import time

pyautogui.FAILSAFE = True

def is_snowy_mountain():
    screenshot = pyautogui.screenshot()
    img_np = np.array(screenshot)

    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    white_pixel_count = cv2.countNonZero(thresh)
    total_pixel_count = thresh.size
    white_pixel_percentage = (white_pixel_count / total_pixel_count) * 100

    print(f"White Pixel Percentage: {white_pixel_percentage:.2f}%")

    if white_pixel_percentage > 30.0:
        return True
    else:
        return False

def search_for_gems():
    pass

def send_gather_march(x, y):
    pass

def move_map():
    pass

def start_bot():
    pass

if __name__ == "__main__":
    start_bot()