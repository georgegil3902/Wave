from tkinter import TK, ttk

class App:
    def __init__(self) -> None:
        self.root = TK()    # Main tkinter window

    # Start tkinter window mainloop
    def start(self):
        """Start function that starts the GUI App"""
        self.root.mainloop()