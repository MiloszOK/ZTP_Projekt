import tkinter as tk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import customtkinter as ctk

def toggle_options_menu(options_frame, x ,y):
    if options_frame.winfo_ismapped():
        options_frame.place_forget()
    else:
        options_frame.place(x=x, y=y + 40, anchor=tk.NW)


def toggle_help_text(help_frame):
    if help_frame.winfo_ismapped():
        help_frame.grab_release()
        help_frame.place_forget()
    else:
        help_frame.grab_set()
        help_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def toggle_settings_option(settings_frame):
    if settings_frame.winfo_ismapped():
        settings_frame.grab_release()
        settings_frame.place_forget()
    else:
        settings_frame.grab_set()
        settings_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def toggle_test_settings(test_settings_frame):
    if test_settings_frame.winfo_ismapped():
        test_settings_frame.grab_release()
        test_settings_frame.place_forget()
    else:
        test_settings_frame.grab_set()
        test_settings_frame.place(relx=0.5,rely=0.5,anchor=tk.CENTER)



def exit_program(root):
    root.destroy()


def show_page1(page1, separator, page2):
    page1.place(x=0, y=40, relwidth=1, relheight=1)
    if not separator.winfo_ismapped():
        separator.place(relx=0.5, rely=0.05, anchor=tk.N, relheight=0.85)
    page2.place_forget()


def show_page2(page1, separator, page2):
    page1.place_forget()
    separator.place_forget()
    page2.place(x=0, y=40, relwidth=1, relheight=1)


def approve_color_template(left_frame):
    left_frame.configure(border_color="lightgreen")


def change_template(filedialog, template_image_label, left_frame):
    global template_loaded_image
    file_path = filedialog.askopenfilename(
        defaultextension=".png",
        filetypes=[("Pliki PNG", "*.png"), ("Wszystkie pliki", "*.*")]
    )
    if not file_path:
        return

    try:
        template_loaded_image = Image.open(file_path)
        ctk_image = ctk.CTkImage(light_image=template_loaded_image, size=(420, 600))
        template_image_label.configure(image=ctk_image)
        template_image_label.image = ctk_image
        print(f"{type(template_loaded_image.mode)}")
        left_frame.configure(border_color="lightblue", border_width=2)
    except Exception as e:
        CTkMessagebox(title="Błąd", message=f"Nie można wczytać pliku: {e}", text_color="white")