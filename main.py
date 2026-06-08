import pyautogui
import cv2
import numpy as np
import time
import pygetwindow as gw
import pytesseract

pyautogui.FAILSAFE = True

pytesseract.pytesseract.tesseract_cmd = r'C:\programy\Tesseract\tesseract.exe'

GAME_TITLE = 'Rise of Kingdoms'

def get_scaled_roi(cur_width, cur_height, BASE_X, BASE_Y, BASE_W, BASE_H):
    BASE_WIDTH = 1366
    BASE_HEIGHT = 768

    scale_x = cur_width / BASE_WIDTH
    scale_y = cur_height / BASE_HEIGHT

    new_x = int(BASE_X * scale_x)
    new_y = int(BASE_Y * scale_y)
    new_w = int(BASE_W * scale_x)
    new_h = int(BASE_H * scale_y)

    return (new_x, new_y, new_w, new_h)

def get_game_screenshot():
    try:
        windows = gw.getWindowsWithTitle(GAME_TITLE)
        if not windows:
            print(f"Game window '{GAME_TITLE}' not found.")
            return None
        
        game_window = windows[0]

        if game_window.isMinimized:
            print(f"Game window '{GAME_TITLE}' is minimized. Please restore it.")
            return None
        
        bounds = (game_window.left, game_window.top, game_window.width, game_window.height)
        screenshot = pyautogui.screenshot(region=bounds)

        return screenshot
    
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None

def check_kingdom_code(screenshot, target_code="", window_width=1366, window_height=768):
    if screenshot is None:
        print("No screenshot available for OCR.")
        return False
    
    try:
        img_np = np.array(screenshot)

        roi_x, roi_y, roi_w, roi_h = get_scaled_roi(window_width, window_height, 23, 30, 125, 70)
        cropped_img = img_np[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        gray = cv2.cvtColor(cropped_img, cv2.COLOR_RGB2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        _, thresh = cv2.threshold(gray, 187, 255, cv2.THRESH_BINARY_INV)

        text = pytesseract.image_to_string(thresh, config='--psm 7').strip()

        print(f"OCR Result: '{text}'")

        if target_code in text:
            print("Kingdom code matches target.")
            return True
        else:
            print("Kingdom code does not match target.")
            return False
        
    except Exception as e:
        print(f"Error during OCR: {e}")
        return False

# def is_snowy_mountain():
#     screenshot = get_game_screenshot()
#     if screenshot is None:
#         return False
#     img_np = np.array(screenshot)

#     gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

#     _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

#     white_pixel_count = cv2.countNonZero(thresh)
#     total_pixel_count = thresh.size
#     white_pixel_percentage = (white_pixel_count / total_pixel_count) * 100

#     print(f"White Pixel Percentage: {white_pixel_percentage:.2f}%")

#     if white_pixel_percentage > 30.0:
#         return True
#     else:
#         return False

def search_for_gems():
    pass

def send_gather_march(x, y):
    pass

def move_map():
    pass

def start_bot():
    time.sleep(5)
    curr_frame = get_game_screenshot()

    is_correct_kingdom = check_kingdom_code(curr_frame, target_code="S11448")

    if is_correct_kingdom:
        print("We are in the correct territory. Safe to move!")
    else:
        print("Warning: Coordinates matching failed or out of bounds!")

if __name__ == "__main__":
    start_bot()