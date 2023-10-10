import string
import tkinter as tk

from p300.config import *


class UI:
    def __init__(self, callback):
        self.typing_label = None
        self.labels = None
        self.window = None
        self.configure_window(callback)

    def configure_window(self, callback):
        self.window = tk.Tk()
        self.window.configure(bg='black')
        self.window.rowconfigure([1], minsize=GRID_ROW_SIZE)
        self.window.columnconfigure([1], minsize=GRID_COL_SIZE)

        def key(k):
            if k.char == 's':
                callback()

        self.window.bind('<KeyPress>', key)

        self.label = tk.Label()
        self.label.grid(column=1, row=1)

        self.label.configure(text=str("BUTTON"), bg="black", fg="grey", font=('Times', 50))
        #self.label.configure(bg="black", fg="grey", font=('Times', 50))
        #self.label.grid(row=i + 1, column=j, sticky="nsew", padx=0, pady=0)

    def start(self):
        self.window.mainloop()

    def sleep(self, t):
        ms = int(t)
        root = tk._get_default_root()
        var = tk.IntVar(root)
        root.after(ms, lambda: var.set(1))
        root.wait_variable(var)


    def clear(self):
        self.label.configure(bg="black", fg="grey", font=('Times', 50))

    def highlight(self):
        self.label.configure(bg="blue", fg="white", font=('Times', 50))

        self.label.after(500, self.clear)
        self.sleep(3000)
