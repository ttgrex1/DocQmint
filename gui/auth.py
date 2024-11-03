# gui/auth.py

import tkinter as tk
from tkinter import messagebox
from utils.env_manager import save_api_key, get_env_variable
from dotenv import set_key

class AdminLoginWindow:
    def __init__(self, master, on_success_callback):
        self.master = master
        self.on_success_callback = on_success_callback
        self.admin_password = get_env_variable('ADMIN_PASSWORD', 'admin')
        self.create_widgets()

    def create_widgets(self):
        self.password_window = tk.Toplevel(self.master)
        self.password_window.title("Admin Login")
        self.password_window.configure(bg='black')
        self.password_window.geometry('300x150')

        password_label = tk.Label(self.password_window, text="Enter Admin Password:", bg='black', fg='white')
        password_label.pack(pady=10)

        self.password_var = tk.StringVar()
        password_entry = tk.Entry(self.password_window, textvariable=self.password_var, show='*', width=30, bg='grey', fg='white')
        password_entry.pack(pady=10)

        login_button = tk.Button(self.password_window, text="Login", command=self.check_admin_password, bg='darkgrey', fg='green')
        login_button.pack(pady=10)

        password_entry.bind("<Return>", self.check_admin_password)
        password_entry.focus_set()

    def check_admin_password(self, event=None):
        entered_password = self.password_var.get()
        self.admin_password = get_env_variable('ADMIN_PASSWORD', 'admin')

        if entered_password == self.admin_password:
            self.on_success_callback()
            self.password_window.destroy()
        else:
            messagebox.showerror("Error", "Incorrect password.")
            self.password_window.destroy()

class ChangePasswordWindow:
    def __init__(self, master):
        self.master = master
        self.current_password = get_env_variable('ADMIN_PASSWORD', 'admin')
        self.create_widgets()

    def create_widgets(self):
        self.change_password_window = tk.Toplevel(self.master)
        self.change_password_window.title("Change Admin Password")
        self.change_password_window.configure(bg='black')
        self.change_password_window.geometry('300x200')

        current_password_label = tk.Label(self.change_password_window, text="Current Password:", bg='black', fg='white')
        current_password_label.pack(pady=5)

        self.current_password_var = tk.StringVar()
        current_password_entry = tk.Entry(self.change_password_window, textvariable=self.current_password_var, show='*', width=30, bg='grey', fg='white')
        current_password_entry.pack(pady=5)

        new_password_label = tk.Label(self.change_password_window, text="New Password:", bg='black', fg='white')
        new_password_label.pack(pady=5)

        self.new_password_var = tk.StringVar()
        new_password_entry = tk.Entry(self.change_password_window, textvariable=self.new_password_var, show='*', width=30, bg='grey', fg='white')
        new_password_entry.pack(pady=5)

        confirm_password_label = tk.Label(self.change_password_window, text="Confirm New Password:", bg='black', fg='white')
        confirm_password_label.pack(pady=5)

        self.confirm_password_var = tk.StringVar()
        confirm_password_entry = tk.Entry(self.change_password_window, textvariable=self.confirm_password_var, show='*', width=30, bg='grey', fg='white')
        confirm_password_entry.pack(pady=5)

        change_button = tk.Button(self.change_password_window, text="Change Password", command=self.save_new_password, bg='darkgrey', fg='green')
        change_button.pack(pady=10)

        confirm_password_entry.bind("<Return>", self.save_new_password)
        confirm_password_entry.focus_set()

    def save_new_password(self, event=None):
        current_password = self.current_password_var.get()
        new_password = self.new_password_var.get()
        confirm_password = self.confirm_password_var.get()

        if current_password != self.current_password:
            messagebox.showerror("Error", "Current password is incorrect.")
            return
        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match.")
            return
        if not new_password:
            messagebox.showerror("Error", "New password cannot be empty.")
            return

        # Save new password to .env file
        set_key('.env', 'ADMIN_PASSWORD', new_password)
        messagebox.showinfo("Success", "Admin password changed successfully.")
        self.change_password_window.destroy()
