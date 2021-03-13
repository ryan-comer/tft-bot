import tkinter as tk
from tft_bot import TftBot

import threading

class BotUI:
    def __init__(self):
        self.main_window = tk.Tk()

        self.tft_bot = TftBot(logging_function=self.write_log) # Set up the bot object

        # Init the components
        self.title = tk.Label(text='TFT Bot')
        self.log = tk.Text(state='disabled')
        self.start_button = tk.Button(text='Start Bot', width=50, command=self.start_bot)
        self.stop_button = tk.Button(text='Stop Bot', width=50, command=self.stop_bot)

        self.title.pack()
        self.log.pack()
        self.start_button.pack()
        self.stop_button.pack()

    def start(self):
        self.main_window.mainloop()

    def start_bot(self):
        self.bot_thread = threading.Thread(target=self.tft_bot.start)
        self.bot_thread.start()

    def stop_bot(self):
        self.tft_bot.stop()
        self.bot_thread.join()
        self.bot_thread = None

    # Write
    def write_log(self, log_message):
        self.log.configure(state='normal')
        self.log.delete('1.0', tk.END)
        self.log.insert('end', log_message)
        self.log.configure(state='disabled')