import tkinter as tk
from tft_bot import TftBot
import pyautogui

import threading
import time

class BotUI:
    def __init__(self):
        self.main_window = tk.Tk()
        start_stop_frame = tk.Frame(self.main_window, borderwidth=1)
        debug_buttons_frame = tk.Frame(self.main_window)
        config_frame = tk.Frame(self.main_window)

        self.tft_bot = TftBot(logging_function=self.logging_function) # Set up the bot object
        self.bot_thread = None  # Thread used by the bot to perform functions

        self.log_message = None

        # Init the components
        self.title = tk.Label(text='TFT Bot')
        self.instructions = tk.Text(height=3)
        self.log = tk.Text(state='disabled')
        self.start_button = tk.Button(start_stop_frame, text='Start Bot', command=self.start_bot, padx=5, pady=5)
        self.stop_button = tk.Button(start_stop_frame, text='Stop Bot', command=self.stop_bot, padx=5, pady=5)

        self.checkbox_var = tk.IntVar()
        self.checkbox = tk.Checkbutton(config_frame, text='Buy champions/Move character', variable=self.checkbox_var, onvalue=1, offvalue=0, command=self.checkbox_checked)
        self.checkbox.select()
        
        # Buttons for checking images
        self.images_check = tk.Button(debug_buttons_frame, text='Check Images', command=self.check_images, padx=5, pady=5)
        self.stop_images_check = tk.Button(debug_buttons_frame, text='Stop image check', command=self.stop_check_images, padx=5, pady=5)

        # Button for testing the mouse
        self.test_button = tk.Button(debug_buttons_frame, text='Test Mouse', command=self.test_mouse, padx=5, pady=5)

        self.instructions.insert('end', 'Out of game settings: Window Size - 1280x720, Interface - all scales at 100\n')
        self.instructions.insert('end', 'In game settings: Fullscreen, 1920x1080 resolution\n')
        self.instructions.insert('end', 'Windows Resolution: 1920x1080, Windows UI scaling: 100%\n')
        self.instructions.configure(state='disabled')

        self.title.pack()
        self.instructions.pack()
        self.log.pack()

        self.checkbox.pack(side=tk.LEFT)
        config_frame.pack()
        
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        start_stop_frame.pack()

        self.test_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.images_check.pack(side=tk.LEFT, padx=5, pady=5)
        self.stop_images_check.pack(side=tk.LEFT, padx=5, pady=5)
        debug_buttons_frame.pack()

        self.logging = True
        self.checking_images = False

    def start(self):
        self.logging_thread = threading.Thread(target=self.logging_worker)
        self.logging_thread.start()

        self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main_window.mainloop()

    def on_closing(self):
        self.logging = False
        self.checking_images = False

        if self.bot_thread != None:
            self.stop_bot(join=False)

        self.main_window.destroy()

    # Worker function to read what to log and put it in the UI
    def logging_worker(self):
        while self.logging:
            if self.log_message != None:
                self.write_log(self.log_message)
                self.log_message = None

            time.sleep(0.5)

    def start_bot(self):
        if self.bot_thread != None:
            self.stop_bot()

        self.bot_thread = threading.Thread(target=self.tft_bot.start)
        self.bot_thread.start()

    def stop_bot(self, join=True):
        self.tft_bot.stop()

        if self.bot_thread != None:
            if join:
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

    # Function executed when the checkbox is checked
    def checkbox_checked(self):
        print(self.checkbox_var.get())
        if(self.checkbox_var.get() == 0):
            self.tft_bot.should_buy_and_move = False
        elif(self.checkbox_var.get() == 1):
            self.tft_bot.should_buy_and_move = True

    # Log function for the bot to use
    def logging_function(self, message):
        self.log_message = message

    def write_log(self, log_message):
        self.log.configure(state='normal')
        self.log.delete('1.0', tk.END)
        self.log.insert('end', log_message)
        self.log.configure(state='disabled')

    def write_image_results(self):
        join_str = '\n'.join(self.found_images)
        result_str = 'Checking Images:\n' + join_str

        self.write_log(result_str)