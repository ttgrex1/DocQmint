# main.py

import tkinter as tk
from gui.app import LLMChatApp

if __name__ == "__main__":
    root = tk.Tk()
    app = LLMChatApp(root)
    root.mainloop()
