import tkinter as tk


class UI:
    def __init__(self, callbacks):
        self.typing_label = None
        self.labels = None
        self.window = None
        self.configure_window(callbacks)

    def configure_window(self, callbacks):
        callback_play = callbacks[0]

        self.window = tk.Tk()

        def key(k):
            if k.char == 'p':
                callback_play()

        self.window.bind('<KeyPress>', key)

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
