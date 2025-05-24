import tkinter as tk

class OnScreenKeyboard(tk.Toplevel):
    def __init__(self, master, entry_widget, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Keyboard")
        self.entry = entry_widget
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.configure(bg="black")
        self.create_keys()

    def create_keys(self):
        keys = [
            ['1','2','3'],
            ['4','5','6'],
            ['7','8','9'],
            ['0','Del','Clear'],
            ['OK']
        ]
        for y, row in enumerate(keys):
            for x, key in enumerate(row):
                btn = tk.Button(
                    self, text=key, width=6, height=3, font=("Arial", 16),
                    command=lambda k=key: self.key_press(k)
                )
                btn.grid(row=y, column=x, padx=2, pady=2)
        self.protocol("WM_DELETE_WINDOW", self.close_keyboard)

    def key_press(self, key):
        if key == "OK":
            self.close_keyboard()
        elif key == "Del":
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current[:-1])
        elif key == "Clear":
            self.entry.delete(0, tk.END)
        else:
            self.entry.insert(tk.END, key)

    def close_keyboard(self):
        self.destroy()