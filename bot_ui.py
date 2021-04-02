import tkinter as tk
from tft_bot import TftBot
import pyautogui

import threading
import time

class BotUI:
    def __init__(self):
        self.main_window = tk.Tk()

        self.tft_bot = TftBot(logging_function=self.write_log) # Set up the bot object
        self.bot_thread = None  # Thread used by the bot to perform functions

        # Init the components
        self.title = tk.Label(text='TFT Bot')
        self.instructions = tk.Text(height=3)
        self.log = tk.Text(state='disabled')
        self.start_button = tk.Button(text='Start Bot', width=50, command=self.start_bot)
        self.stop_button = tk.Button(text='Stop Bot', width=50, command=self.stop_bot)
        
        # Buttons for checking images
        self.images_check = tk.Button(text='Check Images', width=40, command=self.check_images)
        self.stop_images_check = tk.Button(text='Stop image check', width=40, command=self.stop_check_images)

        # Button for test image
        self.test_button = tk.Button(text='Test Mouse', width=40, command=self.test_mouse)

        self.instructions.insert('end', 'Out of game settings: Window Size - 1280x720, Interface - all scales at 100\n')
        self.instructions.insert('end', 'In game settings: Fullscreen, 1920x1080 resolution\n')
        self.instructions.insert('end', 'Windows Resolution: 1920x1080, Windows UI scaling: 100%\n')
        self.instructions.configure(state='disabled')

        self.title.pack()
        self.instructions.pack()
        self.log.pack()
        self.start_button.pack()
        self.stop_button.pack()
        self.test_button.pack()
        self.images_check.pack()
        self.stop_images_check.pack()

    def start(self):
        self.main_window.mainloop()

    def start_bot(self):
        if self.bot_thread != None:
            self.stop_bot()

        self.bot_thread = threading.Thread(target=self.tft_bot.start)
        self.bot_thread.start()

    def stop_bot(self):
        self.tft_bot.stop()

        if self.bot_thread != None:
            self.bot_thread.join()
            self.bot_thread = None

        self.write_log('Bot is stopped')

    # Start a thread to check images
    def check_images(self):
        self.found_images = []
        self.checking_images = True

        # Start the thread to check
        self.image_check_thread = threading.Thread(target=self.image_check_worker)
        self.image_check_thread.start()

    def stop_check_images(self):
        self.checking_images = False
        self.write_log('')

    # Start bot testing mouse
    def test_mouse(self):
        if self.bot_thread != None:
            self.stop_bot()

        self.bot_thread = threading.Thread(target=self.tft_bot.test_coords)
        self.bot_thread.start()

    # Worker function to check for images
    def image_check_worker(self):
        image_names = [
            'start_game',
            'accept',
            'in_queue',
            '3_2',
            'menu',
            'surrender_1',
            'surrender_2',
            'play_again'
        ]

        # Check for each image
        while self.checking_images:
            subset = [image_name for image_name in image_names if image_name not in self.found_images]
            for image_name in subset:
                image_file = './res/' + image_name + '.png'
                if pyautogui.locateCenterOnScreen(image_file, confidence=0.90):
                    self.found_images.append(image_name)

            if self.check_images:
                self.write_image_results()

    # Write
    def write_log(self, log_message):
        self.log.configure(state='normal')
        self.log.delete('1.0', tk.END)
        self.log.insert('end', log_message)
        self.log.configure(state='disabled')

    def write_image_results(self):
        join_str = '\n'.join(self.found_images)
        result_str = 'Checking Images:\n' + join_str

        self.write_log(result_str)