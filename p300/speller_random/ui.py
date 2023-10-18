import string
import tkinter as tk

from p300.config import *


class UI:
    def __init__(self, callbacks):
        self.typing_label = None
        self.labels = None
        self.window = None
        self.size_normal = 50
        self.size_big = 70

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
                self.labels[i][j].configure(text=str(arr[k]), bg="black", fg="grey", font=('Times', self.size_normal))
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

    def highlight(self, nums):
        for num in nums:
            col = num // GRID_SIZE
            row = num % GRID_SIZE

            self.labels[row][col].configure(bg="#080818", fg="white", font=('Times', self.size_big))

        self.labels[row][col].after(DURATION1, self.clear_nums, nums)
        self.sleep(DURATION2)

    def highlight_target(self, row, col):
        self.labels[row][col].configure(bg="blue", fg="white", font=('Times', self.size_big))

        self.labels[row][col].after(2000, self.clear_cell, row, col)
        self.sleep(3000)

    def highlight_prediction(self, row, col):
        self.labels[row][col].configure(bg="green", fg="white", font=('Times', self.size_big))
        self.typing_label.configure(text=self.typing_label['text'] + str(self.labels[row][col]['text']))
        self.labels[row][col].after(2000, self.clear_cell, row, col)
        self.sleep(3000)

    def countdown(self):
        for i in range(len(self.labels)):
            for j in range(len(self.labels)):
                self.labels[i][j].configure(fg="white", font=('Times', self.size_big))
        self.sleep(2000)
        for i in range(len(self.labels)):
            for j in range(len(self.labels)):
                self.labels[i][j].configure(fg="grey", font=('Times', self.size_normal))

    def clear_cell(self, row, col):
        self.labels[row][col].configure(bg="black", fg="grey", font=('Times', self.size_normal))
    
    def clear_nums(self, nums):
        for num in nums:
            col = num // GRID_SIZE
            row = num % GRID_SIZE

            self.labels[row][col].configure(bg="black", fg="grey", font=('Times', self.size_normal))
