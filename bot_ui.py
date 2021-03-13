import tkinter as tk
from tft_bot import TftBot
import pyautogui

import threading

class BotUI:
    def __init__(self):
        self.main_window = tk.Tk()

        self.tft_bot = TftBot(logging_function=self.write_log) # Set up the bot object

        # Init the components
        self.title = tk.Label(text='TFT Bot')
        self.instructions = tk.Text(height=2)
        self.log = tk.Text(state='disabled')
        self.start_button = tk.Button(text='Start Bot', width=50, command=self.start_bot)
        self.stop_button = tk.Button(text='Stop Bot', width=50, command=self.stop_bot)

        self.instructions.insert('end', 'Out of game settings: Window Size - 1280x720, Interface - all scales at 100\n')
        self.instructions.insert('end', 'In game settings: Fullscreen, 1920x1080 resolution')
        self.instructions.configure(state='disabled')

        self.title.pack()
        self.instructions.pack()
        self.log.pack()
        self.start_button.pack()
        self.stop_button.pack()

        self.screenshot_name = ''   # Used for taking a screenshot of an image

    def start(self):
        self.main_window.mainloop()

    def start_bot(self):
        self.bot_thread = threading.Thread(target=self.tft_bot.start)
        self.bot_thread.start()

    def stop_bot(self):
        self.tft_bot.stop()
        self.bot_thread.join()
        self.bot_thread = None
        self.write_log('Bot is stopped')

    # Write
    def write_log(self, log_message):
        self.log.configure(state='normal')
        self.log.delete('1.0', tk.END)
        self.log.insert('end', log_message)
        self.log.configure(state='disabled')

    # Start dragging the box
    def start_drag(self):
        self.image_starting_position = pyautogui.position

    def end_drag(self):
        self.image_ending_position = pyautogui.position