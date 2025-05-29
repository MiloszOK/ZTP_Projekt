import customtkinter as ctk
import tkinter as tk
import json
import os
import sys

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

try:
    with open("./Assets/passwords.json", "r") as f:
        password_data = json.load(f)
        valid_passwords = password_data.get("passwords", [])
except Exception as e:
    print(f"Błąd przy wczytywaniu pliku z hasłami: {e}")
    sys.exit(1)

root = ctk.CTk()
root.geometry("320x180")
root.title("Logowanie")

font = ctk.CTkFont(family="Arial", size=16)

label = ctk.CTkLabel(root, text="Wprowadź hasło", font=font)
label.pack(pady=20)

entry = ctk.CTkEntry(root, show="*", width=200, font=font)
entry.pack(pady=0)

status_label = ctk.CTkLabel(root, text="", text_color="red")
status_label.pack(pady=0)

def check_password():
    password = entry.get()
    if password in valid_passwords:
        root.destroy()
        import Imports.logic
    else:
        status_label.configure(text="Nieprawidłowe hasło")

login_button = ctk.CTkButton(root, text="Zaloguj", command=check_password, font=font)
login_button.pack(pady=(0, 0))

root.mainloop()
