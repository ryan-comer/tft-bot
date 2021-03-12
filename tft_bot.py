import pyautogui
import pygetwindow
import datetime

import time
class TftBot:
    def __init__(self):
        self.league_client_name = 'League of Legends'

    # Start the bot
    def start(self):
        windows = pygetwindow.getWindowsWithTitle(self.league_client_name)
        if len(windows) == 0:
            print('No Leauge client found')
        self.league_client_window = windows[0]

        self.league_client_window.activate()
        time.sleep(1)

        self.surrender()

    # Get the position of the mouse in the particular window
    def get_mouse_in_window(self, window):
        window_position = window.topleft
        mouse_position = pyautogui.position()
        x_in_window = mouse_position.x - window_position[0]
        y_in_window = mouse_position.y - window_position[1]
        return (x_in_window, y_in_window)

    # Start a game from the play again screen
    def start_game(self):
        print('Start Game')
        # Look for the start game button
        result = None
        while result == None:
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
        print('Accept Game')
        # Find the image
        result = None
        while result == None:
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
            result = pyautogui.locateCenterOnScreen('./res/in_queue.png', confidence=0.90)

            # Move and click the accept button again
            pyautogui.moveTo(image_x, image_y, 1)
            time.sleep(1)
            pyautogui.leftClick()
            time.sleep(1)

        self.wait_for_surrender()

    # Wait until 3_2
    def wait_for_surrender(self):
        print('Wait for surrender')
        # Find the 3_2 image
        result = None
        while result == None:
            result = pyautogui.locateCenterOnScreen('./res/3_2.png', confidence=0.9)

        self.surrender()

    # Open the surrender menu and surrender
    def surrender(self):
        print('Surrender')

        # Open surrender menu
        # Find and click on options menu
        result = None
        while result == None:
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
        print('Play again')

        # Find and click on surrender
        result = None
        while result == None:
            result = pyautogui.locateCenterOnScreen('./res/play_again.png', confidence=0.9)

        # Move and click
        (image_x, image_y) = result
        pyautogui.moveTo(image_x, image_y, 1)
        pyautogui.leftClick()
        time.sleep(1)

        self.start_game()