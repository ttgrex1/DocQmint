# gui/api_keys_window.py

import tkinter as tk
from tkinter import messagebox
from utils.env_manager import save_api_key
from dotenv import set_key, unset_key

class APIKeysWindow:
    def __init__(self, master, groq_api_key_var, openai_api_key_var, admin_password, on_save_callback):
        self.master = master
        self.groq_api_key_var = groq_api_key_var
        self.openai_api_key_var = openai_api_key_var
        self.admin_password = admin_password
        self.on_save_callback = on_save_callback  # Callback to update API keys in main app

        self.create_widgets()

    def create_widgets(self):
        self.master.title("API Keys")
        self.master.configure(bg='black')
        self.master.geometry('620x200')  # Adjust window size as needed

        # Groq Section
        groq_label = tk.Label(self.master, text="Groq API Key:", bg='black', fg='white')
        groq_label.grid(row=0, column=0, padx=10, pady=10)

        self.groq_key_var_display = tk.StringVar(value='********')  # Hide the key
        self.groq_entry = tk.Entry(self.master, textvariable=self.groq_key_var_display, show='*', width=40, bg='grey', fg='white', state='disabled')
        self.groq_entry.grid(row=0, column=1, padx=10, pady=10)

        groq_toggle_button = tk.Button(self.master, text="Show/Hide", command=lambda: self.toggle_password(self.groq_entry), state='disabled')
        groq_toggle_button.grid(row=0, column=2, padx=10)

        groq_save_button = tk.Button(self.master, text="Save", command=lambda: self.save_api_key("GROQ_API_KEY", self.groq_key_var_display.get()), bg='darkgrey', fg='green', state='disabled')
        groq_save_button.grid(row=0, column=3, padx=10)

        groq_delete_button = tk.Button(self.master, text="Delete", command=lambda: self.delete_api_key("GROQ_API_KEY"), bg='darkgrey', fg='red', state='disabled')
        groq_delete_button.grid(row=0, column=4, padx=10)

        # OpenAI Section
        openai_label = tk.Label(self.master, text="OpenAI API Key:", bg='black', fg='white')
        openai_label.grid(row=1, column=0, padx=10, pady=10)

        self.openai_key_var_display = tk.StringVar(value='********')  # Hide the key
        self.openai_entry = tk.Entry(self.master, textvariable=self.openai_key_var_display, show='*', width=40, bg='grey', fg='white', state='disabled')
        self.openai_entry.grid(row=1, column=1, padx=10, pady=10)

        openai_toggle_button = tk.Button(self.master, text="Show/Hide", command=lambda: self.toggle_password(self.openai_entry), state='disabled')
        openai_toggle_button.grid(row=1, column=2, padx=10)

        openai_save_button = tk.Button(self.master, text="Save", command=lambda: self.save_api_key("OPENAI_API_KEY", self.openai_key_var_display.get()), bg='darkgrey', fg='green', state='disabled')
        openai_save_button.grid(row=1, column=3, padx=10)

        openai_delete_button = tk.Button(self.master, text="Delete", command=lambda: self.delete_api_key("OPENAI_API_KEY"), bg='darkgrey', fg='red', state='disabled')
        openai_delete_button.grid(row=1, column=4, padx=10)

        # Admin button
        admin_button = tk.Button(self.master, text="Admin", command=self.admin_login)
        admin_button.grid(row=2, column=0, padx=10, pady=20)

        self.change_password_button = tk.Button(self.master, text="Change Password", command=self.change_admin_password, state='disabled')
        self.change_password_button.grid(row=2, column=1, padx=10, pady=20)

        # Store the widgets to enable/disable
        self.api_key_widgets = [
            self.groq_entry, groq_toggle_button, groq_save_button, groq_delete_button,
            self.openai_entry, openai_toggle_button, openai_save_button, openai_delete_button,
            self.change_password_button
        ]

    def toggle_password(self, entry_widget):
        if entry_widget.cget('show') == '*':
            entry_widget.config(show='')
        else:
            entry_widget.config(show='*')

    def save_api_key(self, key_name, key_value):
        if key_value and key_value != '********':
            save_api_key(key_name, key_value)
            messagebox.showinfo("Success", f"{key_name} saved successfully.")
            self.on_save_callback()
        else:
            messagebox.showwarning("Warning", "API key cannot be empty or hidden.")

    def delete_api_key(self, key_name):
        save_api_key(key_name, '')
        messagebox.showinfo("Success", f"{key_name} deleted successfully.")
        if key_name == "GROQ_API_KEY":
            self.groq_key_var_display.set('')
        elif key_name == "OPENAI_API_KEY":
            self.openai_key_var_display.set('')
        self.on_save_callback()

    def admin_login(self):
        from gui.auth import AdminLoginWindow
        AdminLoginWindow(self.master, self.enable_api_key_widgets)

    def enable_api_key_widgets(self):
        for widget in self.api_key_widgets:
            widget.config(state='normal')

        # Update API key displays
        from utils.env_manager import get_env_variable
        groq_api_key = get_env_variable('GROQ_API_KEY', '')
        openai_api_key = get_env_variable('OPENAI_API_KEY', '')
        self.groq_key_var_display.set(groq_api_key if groq_api_key else '')
        self.openai_key_var_display.set(openai_api_key if openai_api_key else '')

    def change_admin_password(self):
        from gui.auth import ChangePasswordWindow
        ChangePasswordWindow(self.master)
