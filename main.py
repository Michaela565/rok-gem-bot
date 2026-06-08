import pyautogui
import cv2
import numpy as np
import time
import pygetwindow as gw
import pytesseract
from random import random, randint

pyautogui.FAILSAFE = True

pytesseract.pytesseract.tesseract_cmd = r'C:\programy\Tesseract\tesseract.exe'

GAME_TITLE = 'Rise of Kingdoms'

TARGET_KINGDOM_CODE = "11448"

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

def activate_game_window():
    try:
        windows = gw.getWindowsWithTitle(GAME_TITLE)
        if not windows:
            print(f"Game window '{GAME_TITLE}' not found.")
            return False
        
        game_window = windows[0]
        game_window.activate()
        return True
    
    except Exception as e:
        print(f"Error activating game window: {e}")
        return False

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

        roi_x, roi_y, roi_w, roi_h = get_scaled_roi(window_width, window_height, 40, 30, 110, 70)
        cropped_img = img_np[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        gray = cv2.cvtColor(cropped_img, cv2.COLOR_RGB2GRAY)
        gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv2.threshold(blurred, 185, 255, cv2.THRESH_BINARY)

        kernel = np.ones((2, 2), np.uint8) 
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)


        text = pytesseract.image_to_string(closed, config='--psm 7 -c tessedit_char_whitelist=0123456789').strip()

        print(f"OCR Result: '{text}'")

        if target_code in text:
            print("Kingdom code matches target.")
            return True
        else:
            cv2.imshow("OCR Region", closed)
            cv2.waitKey(0)
            print("Kingdom code does not match target.")
            return False
        
    except Exception as e:
        print(f"Error during OCR: {e}")
        return False


def search_for_gems(screenshot, confidence=0.8):

    if screenshot is None:
        print("No screenshot available for gem search.")
        return None
    
    try:
        game_img = np.array(screenshot)
        game_image_cv = cv2.cvtColor(game_img, cv2.COLOR_RGB2BGR)

        template = cv2.imread(r'C:\muskine_kody\rok-gem-bot\media\gem.png', cv2.IMREAD_COLOR_BGR)

        if template is None:
            print("Gem template image not found.")
            return None
        
        best_score = -1
        best_loc = None
        best_size = None

        for scale in np.linspace(0.5, 1.5, num=20)[::-1]:

            width = int(template.shape[1] * scale)
            height = int(template.shape[0] * scale)
            resized_template = cv2.resize(template, (width, height))

            if resized_template.shape[0] > game_image_cv.shape[0] or resized_template.shape[1] > game_image_cv.shape[1]:
                continue

            result = cv2.matchTemplate(game_image_cv, resized_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > best_score:
                best_score = max_val
                best_loc = max_loc
                best_size = (width, height)

        print(f"Best match score: {best_score:.2f}")

        if best_score >= confidence:
            center_x = best_loc[0] + best_size[0] // 2
            center_y = best_loc[1] + best_size[1] // 2
            print(f"Gem found at: ({center_x}, {center_y}) with confidence {best_score:.2f}")
            return (center_x, center_y)
        
        else:
            print("No gem found with sufficient confidence.")
            return None

    except Exception as e:
        print(f"Error during gem search: {e}")
        return None


def send_gather_march(x, y):
    """The sequence of clicks required to send troops once a gem is found."""
    print(f"Gems spotted at {x}, {y}! Initiating gather sequence...")
    
    # 1. Click the gem on the map
    pyautogui.click(x, y)
    time.sleep(1) # Wait for the game UI menu to pop up
    
    # 2. Click the 'Gather' button (You would use another image search to find this button!)
    # ... code to find and click 'Gather' ...
    time.sleep(1)
    
    # 3. Click the 'New Troop March' button
    # ... code to find and click 'March' ...
    time.sleep(2) # Give the troops time to leave the city

def move_map():
    sleeptime = random()
    keys = ["up", "down", "left", "right"]
    key = randint(0, 3)
    activate_game_window()
    if check_kingdom_code(get_game_screenshot(), target_code=TARGET_KINGDOM_CODE):
        pyautogui.keyDown(keys[key])
        time.sleep(sleeptime)
        pyautogui.keyUp(keys[key])
    else:
        pyautogui.press("space")
        time.sleep(1)
        pyautogui.moveTo(500, 350)
        for i in range(11):
            pyautogui.scroll(-600)
            time.sleep(1)
        

def start_bot():
    time.sleep(5)
    print("Running...")
    while True:
        res = search_for_gems(get_game_screenshot(), confidence=0.8)
        if res is not None:
            x, y = res
            pyautogui.moveTo(x, y)
        time.sleep(4)
        move_map()
        time.sleep(randint(3,6))


if __name__ == "__main__":
    start_bot()