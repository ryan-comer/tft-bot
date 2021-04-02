import pyautogui
import pygetwindow
import datetime
from ctypes import windll

import time
class TftBot:
    def __init__(self, logging_function=None):
        self.league_client_name = 'League of Legends'
        self.logging_function=logging_function

        # Account for UI scaling on Windows
        user32 = windll.user32
        user32.SetProcessDPIAware()

    def log(self, log_message):
        if self.logging_function != None:
            self.logging_function(log_message)

    # Start the bot
    def start(self):
        windows = pygetwindow.getWindowsWithTitle(self.league_client_name)
        if len(windows) == 0:
            self.log("No League client found")
        self.league_client_window = windows[0]
        self.league_client_window.activate()

        time.sleep(1)

        self.running = True
        self.start_game()

    def stop(self):
        self.running = False

    # Get the position of the mouse in the particular window
    def get_mouse_in_window(self, window):
        window_position = window.topleft
        mouse_position = pyautogui.position()
        x_in_window = mouse_position.x - window_position[0]
        y_in_window = mouse_position.y - window_position[1]
        return (x_in_window, y_in_window)

    # Use the test image to test the screen coordinates of the mouse
    def test_coords(self):
        self.running = True

        while True:
            result = pyautogui.locateCenterOnScreen('./res/test.png', confidence=0.9)
            log_statement = ""

            if result == None:
                log_statement = "No test image found"
            else:
                mouse_position = pyautogui.position()
                log_statement = "Test Image: (%d, %d)\tMouse: (%d, %d)" % (result.x, result.y, mouse_position.x, mouse_position.y)

            if self.running:
                self.log(log_statement)
            else:
                return

    # Start a game from the play again screen
    def start_game(self):
        self.log('Queuing for TFT game')

        # Look for the start game button
        result = None
        while result == None:
            if not self.running:
                return

            result = pyautogui.locateCenterOnScreen('./res/start_game.png', confidence=0.9)

        # Move and click the button
        (image_x, image_y) = result
        pyautogui.moveTo(image_x, image_y, 1)
        time.sleep(1)
        pyautogui.leftClick()
        time.sleep(1)

        self.accept_game()

    # Accept the game
    def accept_game(self):
        self.log('Accepting TFT game')

        # Find the image
        result = None
        while result == None:
            if not self.running:
                return

            result = pyautogui.locateCenterOnScreen('./res/accept.png', confidence=0.9)
        
        # Move and click
        (image_x, image_y) = result
        pyautogui.moveTo(image_x, image_y, 1)
        time.sleep(1)
        pyautogui.leftClick()
        time.sleep(1)

        # Keep checking until the in_queue button goes away
        result = pyautogui.locateCenterOnScreen('./res/in_queue.png', confidence=0.90)
        while result != None:
            if not self.running:
                return
            result = pyautogui.locateCenterOnScreen('./res/in_queue.png', confidence=0.90)

            # Move and click the accept button again
            pyautogui.moveTo(image_x, image_y, 1)
            time.sleep(1)
            pyautogui.leftClick()
            time.sleep(1)

        self.wait_for_surrender()

    # Wait until 3_2
    def wait_for_surrender(self):
        self.log('Waiting for round 3-2')

        # Find the 3_2 image
        result = None
        while result == None:
            if not self.running:
                return
            result = pyautogui.locateCenterOnScreen('./res/3_2.png', confidence=0.9)

        self.surrender()

    # Open the surrender menu and surrender
    def surrender(self):
        self.log('Surrendering')

        # Open surrender menu
        # Find and click on options menu
        result = None
        while result == None:
            if not self.running:
                return
            result = pyautogui.locateCenterOnScreen('./res/menu.png', confidence=0.9)

        # Move and click
        (image_x, image_y) = result
        pyautogui.moveTo(image_x, image_y, 1)
        time.sleep(1)
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.mouseUp()
        time.sleep(1)

        # Find and click on surrender
        result = None
        while result == None:
            if not self.running:
                return
            result = pyautogui.locateCenterOnScreen('./res/surrender_1.png', confidence=0.9)

        # Move and click
        (image_x, image_y) = result
        pyautogui.moveTo(image_x, image_y, 1)
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.mouseUp()
        time.sleep(1)

        # Find and click on surrender_2
        result = None
        while result == None:
            if not self.running:
                return
            result = pyautogui.locateCenterOnScreen('./res/surrender_2.png', confidence=0.9)

        # Move and click
        (image_x, image_y) = result
        pyautogui.moveTo(image_x, image_y, 1)
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.mouseUp()
        time.sleep(1)

        self.play_again()

    # Click the button to play again
    def play_again(self):
        self.log('Playing Again')

        # Find and click on surrender
        result = None
        while result == None:
            if not self.running:
                return
            result = pyautogui.locateCenterOnScreen('./res/play_again.png', confidence=0.9)

        # Move and click
        (image_x, image_y) = result
        pyautogui.moveTo(image_x, image_y, 1)
        pyautogui.leftClick()
        time.sleep(1)

        self.start_game()