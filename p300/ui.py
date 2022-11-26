import string
import tkinter as tk

from p300.config import *


class UI:
    def __init__(self, callbacks):
        self.typing_label = None
        self.labels = None
        self.window = None
        self.configure_window(callbacks)
        self.configure_labels()

    def configure_window(self, callbacks):
        callback_train, callback_predict, callback_stop = callbacks

        self.window = tk.Tk()
        self.window.configure(bg='black')
        self.window.rowconfigure(list(range(1, GRID_SIZE + 1)), minsize=GRID_ROW_SIZE)
        self.window.columnconfigure(list(range(GRID_SIZE + 1)), minsize=GRID_COL_SIZE)

        def key(k):
            if k.char == 'p':
                callback_predict()
            elif k.char == 't':
                callback_train()
            elif k.char == 's':
                self.clear_typing()
                callback_stop()

        self.window.bind('<KeyPress>', key)

    def configure_labels(self):
        self.typing_label = tk.Label(text="", bg="black", fg="white", font=('Times', 25))
        self.typing_label.grid(row=0, column=2, sticky="nsew", padx=0, pady=5)

        self.labels = [[tk.Label() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        arr = list(string.ascii_uppercase) + ['_'] + list(range(1, 10))
        k = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.labels[i][j].configure(text=str(arr[k]), bg="black", fg="grey", font=('Times', 50))
                self.labels[i][j].grid(row=i + 1, column=j, sticky="nsew", padx=0, pady=0)
                k += 1

    def start(self):
        self.window.mainloop()

    def clear_typing(self):
        self.typing_label.configure(text="")

    def sleep(self, t):
        ms = int(t)
        root = tk._get_default_root()
        var = tk.IntVar(root)
        root.after(ms, lambda: var.set(1))
        root.wait_variable(var)

    def highlight_row(self, row):
        for i in range(len(self.labels)):
            self.labels[row][i].configure(bg="#080808", fg="white", font=('Times', 80))

        self.labels[row][0].after(DURATION1, self.clear_row, row)
        self.sleep(DURATION2)

    def highlight_col(self, col):
        for i in range(len(self.labels)):
            self.labels[i][col].configure(bg="#080808", fg="white", font=('Times', 80))

        self.labels[0][col].after(DURATION1, self.clear_col, col)
        self.sleep(DURATION2)

    def highlight_target(self, row, col):
        self.labels[row][col].configure(bg="blue", fg="white", font=('Times', 80))

        self.labels[row][col].after(2000, self.clear_cell, row, col)
        self.sleep(3000)

    def highlight_prediction(self, row, col):
        self.labels[row][col].configure(bg="green", fg="white", font=('Times', 80))
        self.typing_label.configure(text=self.typing_label['text'] + str(self.labels[row][col]['text']))
        self.labels[row][col].after(2000, self.clear_cell, row, col)
        self.sleep(3000)

    def countdown(self):
        for i in range(len(self.labels)):
            for j in range(len(self.labels)):
                self.labels[i][j].configure(fg="white", font=('Times', 80))
        self.sleep(2000)
        for i in range(len(self.labels)):
            for j in range(len(self.labels)):
                self.labels[i][j].configure(fg="grey", font=('Times', 50))

    def clear_row(self, row):
        for i in range(len(self.labels)):
            self.labels[row][i].configure(bg="black", fg="grey", font=('Times', 50))

    def clear_col(self, col):
        for i in range(len(self.labels)):
            self.labels[i][col].configure(bg="black", fg="grey", font=('Times', 50))

    def clear_cell(self, row, col):
        self.labels[row][col].configure(bg="black", fg="grey", font=('Times', 50))
