# gui/about_window.py

import tkinter as tk

class AboutWindow:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        about_window = tk.Toplevel(self.master)
        about_window.title("About")
        about_window.configure(bg='black')
        about_window.geometry('275x200')  # Adjust window size as needed

        # Display app information
        app_name_label = tk.Label(about_window, text="DocQmint", bg='black', fg='blue', font=('Arial', 16))
        app_name_label.pack(pady=(20, 5))

        version_label = tk.Label(about_window, text="Version: 1.2.24", bg='black', fg='white', font=('Arial', 12))
        version_label.pack(pady=5)

        date_label = tk.Label(about_window, text="Date: 11/02/2024", bg='black', fg='white', font=('Arial', 12))
        date_label.pack(pady=5)

        author_label = tk.Label(about_window, text="Author: ttGrex1", bg='black', fg='white', font=('Arial', 12))
        author_label.pack(pady=(5, 20))
