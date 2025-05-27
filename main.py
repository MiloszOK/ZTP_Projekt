import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import json
import os

PASSWORD_FILE = "Assets/passwords.json"

def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        CTkMessagebox(title="Błąd", message="Plik hasla.json nie istnieje", icon="cancel")
        exit(1)
    try:
        with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("passwords", [])
    except Exception as e:
        CTkMessagebox(title="Błąd", message=f"Nie można odczytać pliku: {e}", icon="cancel")
        exit(1)

PASSWORDS = load_passwords()


PASSWORD = load_passwords()

auth_window = ctk.CTk()
auth_window.geometry("300x150")
auth_window.title("Logowanie")
auth_window.resizable(False, False)

font = ctk.CTkFont(family="Arial", size=14, weight="normal")

def check_password():
    entered_password = password_entry.get()
    if entered_password in PASSWORDS:
        auth_window.destroy()
        import subprocess
        subprocess.Popen(["python", "content.py"])
    else:
        CTkMessagebox(title="Błąd", message="Nieprawidłowe hasło", icon="cancel",
                      button_color="grey", button_hover_color="grey")


label = ctk.CTkLabel(master=auth_window, text="Podaj hasło:", font=font)
label.pack(pady=(20, 5))

password_entry = ctk.CTkEntry(master=auth_window, show="*", width=200)
password_entry.pack(pady=5)

login_button = ctk.CTkButton(master=auth_window, text="Zaloguj", command=check_password, width=100)
login_button.pack(pady=15)

if __name__ == "__main__":
    auth_window.mainloop()
