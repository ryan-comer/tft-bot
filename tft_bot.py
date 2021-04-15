import pyautogui
import pygetwindow
import datetime
from ctypes import windll

from scipy import interpolate
import numpy as np
import random
import math
import time
from datetime import datetime

from pyclick import HumanClicker

class TftBot:
    def __init__(self, logging_function=None):
        self.league_client_name = 'League of Legends'
        self.logging_function=logging_function

        self.start_time = datetime.now()
        self.end_time = datetime.now()

        self.image_confidence = 0.8

        self.should_buy_and_move = True

        self.champion_positions = [
            (0.2995, 0.9148),
            (0.4094, 0.9148),
            (0.5104, 0.9148),
            (0.6146, 0.9148),
            (0.7172, 0.9148),
        ]

        self.hc = HumanClicker()

        # Account for UI scaling on Windows
        user32 = windll.user32

        # Set Pyautogui defaults
        # Any duration less than this is rounded to 0.0 to instantly move the mouse.
        pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
        # Minimal number of seconds to sleep between mouse moves.
        pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
        # The number of seconds to pause after EVERY public function call.
        pyautogui.PAUSE = 0  # Default: 0.1       user32.SetProcessDPIAware()

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

        self.start_time = datetime.now()

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
            result = pyautogui.locateCenterOnScreen('./res/test.png', confidence=self.image_confidence)
            log_statement = ""

            mouse_position = pyautogui.position()
            if result == None:
                log_statement = "Mouse: (%d, %d)" % (mouse_position.x, mouse_position.y)
            else:
                log_statement = "Test Image: (%d, %d)\tMouse: (%d, %d)" % (result.x, result.y, mouse_position.x, mouse_position.y)

            if self.running:
                self.log(log_statement)
            else:
                return

    # Start a game from the play again screen
    def start_game(self):
        self.log('Queuing for TFT game')

        self.start_time = datetime.now()

        # Look for the start game button
        result = None
        while result == None:
            if not self.running:
                return

            result = pyautogui.locateCenterOnScreen('./res/start_game.png', confidence=self.image_confidence)

        # Move and click the button
        (image_x, image_y) = result
        self.move_mouse(image_x, image_y)
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

            result = pyautogui.locateCenterOnScreen('./res/accept.png', confidence=self.image_confidence)
        
        # Move and click
        (image_x, image_y) = result
        self.move_mouse(image_x, image_y)
        time.sleep(1)
        pyautogui.leftClick()
        time.sleep(1)

        # Keep checking until the in_queue button goes away
        result = pyautogui.locateCenterOnScreen('./res/in_queue.png', confidence=self.image_confidence)
        while result != None:
            if not self.running:
                return
            result = pyautogui.locateCenterOnScreen('./res/in_queue.png', confidence=self.image_confidence)

            # Move and click the accept button again
            self.move_mouse(image_x, image_y)
            time.sleep(random.random() * 2)
            pyautogui.leftClick()

        self.wait_for_surrender()

    # Wait until 3_2
    def wait_for_surrender(self):
        self.log('Waiting for round 3-2')

        buy_champion_time = datetime.now()
        walk_time = datetime.now()

        # Find the 3_2 image
        result = None
        while result == None:
            if not self.running:
                return

            # Bot actions during a game
            if self.should_buy_and_move:
                # Check for buy champion
                test_time = datetime.now()
                buy_champion_threshold = random.randrange(25, 50)
                if (test_time - buy_champion_time).total_seconds() >  buy_champion_threshold:
                    self.buy_random_champion()
                    buy_champion_time = datetime.now()

                # Check for walk
                test_time = datetime.now()
                walk_threshold = random.randrange(10, 20)
                if (test_time - walk_time).total_seconds() > walk_threshold:
                    self.move_character()
                    walk_time = datetime.now()

            result = pyautogui.locateCenterOnScreen('./res/3_2.png', confidence=self.image_confidence)

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
            result = pyautogui.locateCenterOnScreen('./res/menu.png', confidence=self.image_confidence)

        # Move and click
        (image_x, image_y) = result
        self.move_mouse(image_x, image_y)
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
            result = pyautogui.locateCenterOnScreen('./res/surrender_1.png', confidence=self.image_confidence)

        # Move and click
        (image_x, image_y) = result
        self.move_mouse(image_x, image_y)
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.mouseUp()
        time.sleep(1)

        # Find and click on surrender_2
        result = None
        while result == None:
            if not self.running:
                return
            result = pyautogui.locateCenterOnScreen('./res/surrender_2.png', confidence=self.image_confidence)

            pyautogui.mouseDown()
            time.sleep(random.random() * 2)
            pyautogui.mouseUp()

        # Move and click
        (image_x, image_y) = result
        self.move_mouse(image_x, image_y)
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
            result = pyautogui.locateCenterOnScreen('./res/play_again.png', confidence=self.image_confidence)

        # Move and click
        (image_x, image_y) = result
        self.move_mouse(image_x, image_y)
        pyautogui.leftClick()
        time.sleep(1)

        self.end_time = datetime.now()
        self.calculate_loop_time()

        self.start_game()

    # Move the character to a random location
    def move_character(self):
        min_val = 0.4
        max_val = 0.6

        x = random.random()
        y = random.random()

        x = max(min_val, min(x, max_val))
        y = max(min_val, min(x, max_val))

        self.move_mouse_screen_percentage(x, y)
        pyautogui.mouseDown(button='right')
        time.sleep(0.5)
        pyautogui.mouseUp(button='right')
        time.sleep(0.5)

    # Buy a random champion
    def buy_random_champion(self):
        champion_position = random.choice(self.champion_positions)
        self.move_mouse_screen_percentage(champion_position[0], champion_position[1])

        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.mouseUp()
        time.sleep(1)

    # Get how long the loop was
    def calculate_loop_time(self):
        loop_time = self.end_time - self.start_time

        with open('./results.txt', 'a+') as f:
            f.write("Loop Time: %s\n" % loop_time)

    def move_mouse_screen_percentage(self, percent_x, percent_y):
        size = pyautogui.size()
        x = size.width * percent_x
        y = size.height * percent_y

        x = int(x)
        y = int(y)

        self.move_mouse(x, y)

    def move_mouse(self, x, y):
        duration = int((random.random() + 1) * 1.5)
        self.hc.move((x, y), duration)