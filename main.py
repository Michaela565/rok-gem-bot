import pyautogui
import cv2
import numpy as np
import time
import pygetwindow as gw

pyautogui.FAILSAFE = True

GAME_TITLE = 'Rise of Kingdoms'

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
    pass

if __name__ == "__main__":
    start_bot()