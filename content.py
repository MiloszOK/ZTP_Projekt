import tkinter as tk
from tkinter import filedialog
from skimage.feature import orb
from skimage.metrics import structural_similarity
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
from constants import *
from fpdf import FPDF
import cv2
import numpy as np
from datetime import datetime

root = ctk.CTk()




''' ----------------------------------------  FUNKCJE PROGRAMU -------------------------------------------- '''


def toggle_options_menu():
    if options_frame.winfo_ismapped():
        options_frame.place_forget()
    else:
        options_frame.place(x=x, y=y + 40, anchor=tk.NW)


def toggle_help_text():
    if help_frame.winfo_ismapped():
        help_frame.grab_release()
        help_frame.place_forget()
    else:
        help_frame.grab_set()
        help_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def toggle_settings_option():
    if settings_frame.winfo_ismapped():
        settings_frame.grab_release()
        settings_frame.place_forget()
    else:
        settings_frame.grab_set()
        settings_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def toggle_test_settings():
    if test_settings_frame.winfo_ismapped():
        test_settings_frame.grab_release()
        test_settings_frame.place_forget()
    else:
        test_settings_frame.grab_set()
        test_settings_frame.place(relx=0.5,rely=0.5,anchor=tk.CENTER)



def exit_program():
    root.destroy()


def show_page1():
    page1.place(x=0, y=40, relwidth=1, relheight=1)
    if not separator.winfo_ismapped():
        separator.place(relx=0.5, rely=0.05, anchor=tk.N, relheight=0.85)
    page2.place_forget()  # Ukryj stronę 2


def show_page2():
    page1.place_forget()  # Ukryj stronę 1
    separator.place_forget()
    page2.place(x=0, y=40, relwidth=1, relheight=1)  # Wyświetl stronę 2


def approve_color_template():
    left_frame.configure(border_color="lightgreen")


def change_template():
    global template_loaded_image
    file_path = filedialog.askopenfilename(
        defaultextension=".png",
        filetypes=[("Pliki PNG", "*.png"), ("Wszystkie pliki", "*.*")]
    )
    if not file_path:
        return  # Anulowano wybór pliku

    try:
        template_loaded_image = Image.open(file_path)
        ctk_image = ctk.CTkImage(light_image=template_loaded_image, size=(420, 600))
        template_image_label.configure(image=ctk_image)
        template_image_label.image = ctk_image  # Zachowanie referencji do obrazu
        print(f"{type(template_loaded_image.mode)}")
        left_frame.configure(border_color="lightblue", border_width=2)
    except Exception as e:
        CTkMessagebox(title="Błąd", message=f"Nie można wczytać pliku: {e}", text_color="white")


root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)
root.title("Automatic Test Reviewer")

font = ctk.CTkFont(family=FONT[0], size=FONT[1], weight=FONT[2])

toolbar_frame = ctk.CTkFrame(master=root, height=TOOLBAR_HEIGHT, fg_color=FG_COLOR, corner_radius=0)
toolbar_frame.pack(fill="x")

page1 = ctk.CTkFrame(master=root, height=680, fg_color="transparent")
page1.place(x=0, y=40, relwidth=1, relheight=1)
page2 = ctk.CTkFrame(master=root, fg_color="transparent", height=680)
page2.place_forget()


app_height = 720
toolbar_height = 40
left_frame_height = app_height - toolbar_height - 80

left_frame = ctk.CTkFrame(master=page1, height=LEFT_FRAME_HEIGHT, fg_color="transparent")
left_frame.place(x=110, y=40, relwidth=0.325, relheight=0.75, anchor=tk.NW)
# left_frame.pack(side=tk.LEFT, padx=110)

right_frame = ctk.CTkFrame(master=page1, height=LEFT_FRAME_HEIGHT, fg_color="transparent")
right_frame.place(x=705, y=100, relwidth=0.4, relheight=0.60, anchor=tk.NW)


left_frame_page2 = ctk.CTkFrame(master=page2, height=LEFT_FRAME_HEIGHT, fg_color="transparent")
left_frame_page2.place(x=110, y=60, relwidth=0.6, relheight=0.75, anchor=tk.NW)

right_frame_page2 = ctk.CTkFrame(master=page2, height=LEFT_FRAME_HEIGHT, fg_color="#484545",border_width=1,border_color="black")
right_frame_page2.place(x=950, y=60, relwidth=0.20, relheight=0.35, anchor=tk.NW)

button_template_approve = ctk.CTkButton(master=page1, height=40, fg_color=FG_COLOR, text_color=TEXT_COLOR, text="Zatwierdź", font=font, corner_radius=2, hover_color="gray", command=approve_color_template)
button_template_approve.place_forget()

button_template_change = ctk.CTkButton(master=page1, height=40, fg_color=FG_COLOR, text_color=TEXT_COLOR, text="Zmień", font=font, corner_radius=2, hover_color="gray", command=change_template)
button_template_change.place_forget()

template_image_label = ctk.CTkLabel(master=left_frame, text="")
template_image_label.pack(padx=10, pady=10, expand=True, anchor=tk.CENTER)


score_points=0
question_number=0
pass_threshold=0
grade_table = [0.0 for _ in range(3)]
def save_value():
    global score_points,question_number,pass_threshold,grade_table
    try:
        score_points = int(points_entry.get())
        question_number = int(questions_entry.get())
        pass_threshold = float(pass_entry.get())
        grade_table[0]=float(grade_five_entry.get())
        grade_table[1]=float(grade_four_entry.get())
        grade_table[2]=float(grade_three_entry.get())
        if score_points < question_number:
            messagebox = CTkMessagebox(title="Uwaga", message="Liczba punktów nie może być mniejsza niż liczba pytań",
                                       icon="warning", text_color="white",button_hover_color="grey")
            return
        elif score_points> question_number:
            set_question_points(question_number,score_points)
        else:
            print(f"Zapisano wartości: liczba punktów = {score_points}, liczba pytań = {question_number}, próg zaliczeniowy: {pass_threshold},{grade_table[0]}, {grade_table[1]}, {grade_table[2]}")
            toggle_test_settings()
    except ValueError:
        CTkMessagebox(title="Błąd",message = "Podaj poprawne wartości",icon="cancel", text_color="white", button_hover_color="grey")

points_table = []
def set_question_points(question_numbers,score_points):
    global points_table
    toggle_test_settings()
    set_question_points_frame = ctk.CTkFrame(master=root,width=400,fg_color="#484545",corner_radius=4,
                                             border_color="#D9D9D9",border_width=1)
    set_question_points_frame.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

    def update_remaining_points(event=None):
        remaining_points = score_points
        remaining_points_label.configure(text_color="white")
        for entry in point_entry_table:
            try:
                value = int(entry.get())
                if value < 0:
                    CTkMessagebox(title="Uwaga",message = "Podaj wartość dodatnią",
                                  icon="warning", text_color="white", button_hover_color="grey")
                    entry.delete(0, tk.END)
                    entry.focus_set()
                    return
                remaining_points -= value
                if remaining_points < 0:
                    remaining_points_label.configure(text_color="red")
                elif remaining_points == 0:
                    remaining_points_label.configure(text_color="green")
            except ValueError:
                pass
        remaining_points_label.configure(text=f"Pozostałe punkty: {remaining_points}", text_color="white")
    def toggle_set_question_points_frame():
        set_question_points_frame.place_forget()

    points_table = [0]*question_numbers
    text_labels=[]
    point_entry_table = []
    for i in range(question_numbers):
        column = (i // 10) * 2
        row = i % 10
        text_label= ctk.CTkLabel(master=set_question_points_frame,text=f"Pytanie {i+1} punkty:")
        text_label.grid(row=row, column=column, pady=5, padx=10)
        text_labels.append(text_label)

        point_entry= ctk.CTkEntry(master=set_question_points_frame,width=80)
        point_entry.grid(row=row,column=column+1,pady=5, padx=10)
        point_entry_table.append(point_entry)
        point_entry.bind("<KeyRelease>", update_remaining_points)
    def save_points():
        for i, point in enumerate(point_entry_table):
            try:
                value = int(point.get())
                if 0 <= i < question_number:
                    points_table[i]= value
                else:
                    print(f"Indeks {i} poza zakresem tabeli")
            except ValueError:
                print(f"Nieprawidłowa wartość w polu {i+i}.")



    if question_numbers % 10 == 0 and question_numbers > 10:
        num_columns = (question_numbers // 10) * 2
    else:
        num_columns = (question_numbers // 10) * 2 + 2

    if num_columns == 2:
        columnspan = 1
    elif question_numbers % 10 == 0:
        columnspan = num_columns // 2 - 1
    else:
        columnspan = num_columns // 2

    if question_numbers <= 10:
        cancel_column = 0
        save_column = 1
    else:
        cancel_column = 0
        save_column = num_columns - columnspan  #

    remaining_points_label = ctk.CTkLabel(master=set_question_points_frame,
                                          text=f"Punkty do wydania: {score_points}",font=font, text_color="white")
    remaining_points_label.grid(row=question_numbers, column=save_column,columnspan=columnspan, pady=(10,0))
    button_question_points_cancel = ctk.CTkButton(master=set_question_points_frame, text="Anuluj",height=40,command=lambda:[toggle_test_settings(),toggle_set_question_points_frame()],fg_color="#E1E1E1", hover_color="gray", font=font, text_color=TEXT_COLOR, corner_radius=2)
    button_question_points_cancel.grid(row=question_numbers+1,column=cancel_column,columnspan=columnspan,pady=20,padx=10)

    button_question_points_save = ctk.CTkButton(master=set_question_points_frame, text= "Zapisz punkty",height=40, command=lambda:[save_points(),toggle_set_question_points_frame()],fg_color="#E1E1E1", hover_color="gray", font=font, text_color=TEXT_COLOR, corner_radius=2)
    button_question_points_save.grid(row=question_numbers+1, column=save_column,columnspan=columnspan, pady=20,padx=10)

def define_roi(image):
    """
    Wyświetla obraz i pozwala użytkownikowi zaznaczyć prostokątny obszar ROI.
    Zwraca współrzędne i wymiary wybranego ROI.
    """

    window_name = "Zaznacz obszar pytań"
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)

    roi = cv2.selectROI(window_name, image)

    cv2.destroyAllWindows()

    return roi


template_loaded_image = None
def load_template():
    global template_loaded_image
    if template_loaded_image is not None:
        messagebox = CTkMessagebox(title="Uwaga", message="Już wczytano szablon. "
                                                          "Zmień aktualny, aby wczytać nowy.",
                                   icon="warning", text_color="white", button_hover_color="grey")
        return
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
        left_frame.configure(border_color="lightblue", border_width=2)
        button_template_approve.place(x=170, y=590, anchor=tk.NW)
        button_template_change.place(x=320, y=590, anchor=tk.NW)
    except Exception as e:
        CTkMessagebox(title="Błąd", message=f"Nie można wczytać pliku: {e}", text_color="white")




def find_corners_closest_to_edges(corners, image_shape):
    """Znajduje 4 narożniki najbliżej krawędzi obrazu."""
    height, width = image_shape[:2]
    top_left = min(corners, key=lambda c: c[0] + c[1])
    top_right = min(corners, key=lambda c: width - c[0] + c[1])
    bottom_right = min(corners, key=lambda c: width - c[0] + height - c[1])
    bottom_left = min(corners, key=lambda c: c[0] + height - c[1])
    return [top_left, top_right, bottom_right, bottom_left]

def process_image(input_image):

    opencv_image = cv2.cvtColor(np.array(input_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    dst = cv2.dilate(dst, None)

    ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    corners = centroids[1:]

    width = 1000
    height = 1400

    corners = find_corners_closest_to_edges(corners, gray.shape)
    pts1 = np.float32(corners)
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warped_image = cv2.warpPerspective(opencv_image, matrix, (width, height))

    return warped_image


loaded_tests = []

def load_tests():
    global loaded_tests
    file_paths = filedialog.askopenfilenames(
        defaultextension=".png",
        filetypes=[("Pliki PNG", "*.png"), ("Wszystkie pliki", "*.*")]
    )
    if not file_paths:
        return

    for file_path in file_paths:
        try:
            image = Image.open(file_path)

            loaded_tests.append({
                "file_path": file_path,
                "file_name": file_path.split("/")[-1],
                "image":image
            })

        except Exception as e:
            CTkMessagebox(title="Błąd", message=f"Nie można wczytać pliku: {e}", text_color="white")

    button_tests_approve.place(x=810, y=540, anchor=tk.NW)
    button_tests_add.place(x=970, y=540, anchor=tk.NW)
    update_test_list()


list_frame = ctk.CTkFrame(master=root)
def update_test_list():
    global list_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Canvas do przewijania
    canvas = tk.Canvas(right_frame, bg="#f0f0f0", highlightthickness=0, bd=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ctk.CTkScrollbar(master=right_frame, orientation="vertical", command=canvas.yview,
                                 fg_color="#3C3C3C", button_color="#b0b0b0", button_hover_color="#909090")

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Konfiguracja canvas
    canvas.configure(yscrollcommand=scrollbar.set, background="#3C3C3C")
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Ramka wewnętrzna dla elementów listy
    list_frame = ctk.CTkFrame(master=canvas, fg_color="#333333", border_width=2)
    canvas.create_window((0, 0), window=list_frame, anchor="nw")

    # Dodaj nowe widgety dla każdego wczytanego testu
    for i, test in enumerate(loaded_tests):

        item_frame = ctk.CTkFrame(master=list_frame, border_width=1, border_color="gray", fg_color="transparent")
        item_frame.pack(fill=tk.X, expand=True, padx=10, pady=5)

        label = ctk.CTkLabel(master=item_frame, text=test["file_name"])
        label.pack(side=tk.LEFT, fill=tk.X,padx=(10, 310), pady=5)

        delete_button = ctk.CTkButton(master=item_frame, text="X", width=30,
                                      command=lambda index=i: remove_test(index), fg_color="gray", hover_color="gray")
        delete_button.pack(side=tk.RIGHT, padx=10, pady=5)

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def approve_color_tests():
    list_frame.configure(border_color="lightgreen")


def remove_test(index):
    global loaded_tests

    del loaded_tests[index]
    update_test_list()


def convert_to_opencv(image):
    numpy_array=np.array(image)
    opencv_image=cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)
    return opencv_image

def display_image(image, window_name="Obraz"):

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


test_scores=[]
def evaluate():
    if left_frame.cget("border_color") == "lightgreen" and list_frame.cget("border_color") == "lightgreen":

        template_cv = process_image(template_loaded_image)
        test_cv = [process_image(test['image']) for test in loaded_tests]

        x, y, w, h = 367, 434, 344, 75

        template_question_regions = []
        global test_scores
        test_scores = []

        for i in range(question_number):
            question_region = template_cv[y + i * h: y + (i + 1) * h, x: x + w]
            template_question_regions.append(question_region)


        for i, test_image in enumerate(test_cv):
            total_points = 0

            test_question_regions = []
            for j in range(question_number):

                test_question_region = test_image[y + j * h: y + (j + 1) * h,
                                       x:x + w]
                test_question_regions.append(test_question_region)


            for j, (template_region, test_region) in enumerate(zip(template_question_regions, test_question_regions)):
                result = cv2.matchTemplate(test_region, template_region, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                if max_val >= 0.80:
                    if score_points > question_number:
                        point = points_table[j]
                    else:
                        point = 1
                else:
                    point = 0
                total_points += point

            test_scores.append(total_points)

        try:
            test_results()
        except:
            CTkMessagebox(title="Błąd", message="Nie wpisałeś/aś kryteriów oceniania!", icon="warning",
                      text_color="white", button_hover_color="grey")
        else:
            CTkMessagebox(title="Sukces", message="Ocenianie testów zakończone pomyślnie!", icon="check",
                          text_color="white", button_hover_color="grey")
        button_create_report.pack(side="left")

    else:
        CTkMessagebox(title="Błąd", message = "Potwierdź swój wybór", icon= "warning",
                      button_hover_color="grey", text_color="white")


def generate_report(graded_tests, passed_tests, failed_tests, avg_score, avg_points):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(60,60,60)
    pdf.add_font('DejaVu', '', "DejaVuSans.ttf")

    pdf.set_font('DejaVu', '', 16)
    pdf.cell(200, 10, text="RAPORT", ln=1, align="C")
    pdf.ln(20)

    now = datetime.now()
    timestamp = now.strftime("Data: %Y-%m-%d   Godzina: %H:%M:%S")
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(200, 10, text=timestamp, ln=1, align="R")

    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 10, text="Podsumowanie:", ln=1, align="L")
    pdf.ln(10)
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(200, 10, text=f"Ocenione testy: {graded_tests}", ln=1, align="L")
    pdf.cell(200, 10, text=f"Zaliczone: {passed_tests}", ln=1, align="L")
    pdf.cell(200, 10, text=f"Niezaliczone: {failed_tests}", ln=1, align="L")
    pdf.cell(200, 10, text=f"Średnia ocena: {avg_score}", ln=1, align="L")
    pdf.cell(200, 10, text=f"Średnia ilość punktów: {avg_points}", ln=1, align="L")

    pdf.ln(20)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 10, text="Wyniki:", ln=1, align="L")
    pdf.ln(10)
    pdf.set_font('DejaVu', '', 12)


    for i, test in enumerate(loaded_tests):
        acquired_points = test_scores[i]

        if acquired_points / score_points> pass_threshold:
            status = "Zaliczony"
        else:
            status = "Niezaliczony"


        percentage_points = (acquired_points / score_points)
        if percentage_points >= grade_table[0]:
            degree = 5
        elif percentage_points >= grade_table[1]:
            degree = 4
        elif percentage_points >= grade_table[2]:
            degree = 3
        elif percentage_points >= pass_threshold:
            degree = 2
        else:
            degree = 1

        pdf.cell(200, 10,
                 txt=f"Nazwa: {test['file_name']}  Liczba punktów: {acquired_points}  Ocena: {degree}  Status: {status}",
                 ln=1, align="L")

    pdf.output("raport.pdf")
    CTkMessagebox(title="Sukces", message="Raport wygenerowany pomyślnie!", icon="check", text_color="white",
                button_hover_color="grey")


list_frame_page_2 = ctk.CTkFrame(master=root)
graded_tests,passed_test,failed_tests,summary_score,summary_points=0,0,0,0,0
def test_results():
    global graded_tests, passed_test, failed_tests, summary_score, summary_points
    global list_frame_page_2
    for widget in left_frame_page2.winfo_children():
        widget.destroy()

    for widget in right_frame_page2.winfo_children():
        widget.destroy()


    canvas_2 = tk.Canvas(left_frame_page2)
    canvas_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    scrollbar = tk.Scrollbar(left_frame_page2, orient=tk.VERTICAL, command=canvas_2.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    canvas_2.configure(yscrollcommand=scrollbar.set)
    canvas_2.bind('<Configure>', lambda e: canvas_2.configure(scrollregion=canvas_2.bbox("all")))
    list_frame_page_2 = ctk.CTkFrame(master=canvas_2, fg_color="transparent")
    canvas_2.create_window((0, 0), window=list_frame_page_2, anchor="nw")

    graded_tests, passed_test, failed_tests, summary_score, summary_points=0,0,0,0,0
    for i, test in enumerate(loaded_tests):
        acquired_points = test_scores[i]
        summary_points+=acquired_points

        if acquired_points / score_points >= pass_threshold:
            status = "Zaliczony"
            color_status = "green"
            passed_test+=1
        else:
            status = "Niezaliczony"
            color_status= "red"
            failed_tests+=1
        graded_tests += 1

        percentage_points = (acquired_points / score_points)
        if percentage_points >= grade_table[0]:
            degree = 5
        elif percentage_points >= grade_table[1]:
            degree = 4
        elif percentage_points >= grade_table[2]:
            degree = 3
        elif percentage_points >= pass_threshold:
            degree = 2
        else:
            degree = 1
        summary_score+=degree


        item_frame_2 = ctk.CTkFrame(master=list_frame_page_2, border_width=1, border_color="gray", fg_color="transparent")
        item_frame_2.pack(fill=tk.X, expand=True, padx=10, pady=5)

        if i % 2 == 0:
            bg_color_frame = FG_COLOR
        else:
            bg_color_frame = "white"

        item_frame_2.configure(fg_color=bg_color_frame)

        def show_differences(test):
            template_loaded_image_processed = process_image(template_loaded_image)
            test_image_processed = process_image(test['image'])

            template_loaded_image_np = np.array(template_loaded_image_processed)
            test_image_np = np.array(test_image_processed)
            test_name = test["file_name"]


            template_gray = cv2.cvtColor(template_loaded_image_np, cv2.COLOR_BGR2GRAY)
            test_gray = cv2.cvtColor(test_image_np, cv2.COLOR_BGR2GRAY)


            _, thresh1 = cv2.threshold(test_gray, 128, 255, cv2.THRESH_BINARY)
            _, thresh2 = cv2.threshold(template_gray, 128, 255, cv2.THRESH_BINARY)

            combined_result = cv2.bitwise_and(thresh2, thresh1)

            _, test_gray_binary = cv2.threshold(test_gray, 128, 255, cv2.THRESH_BINARY)

            (score, diff) = structural_similarity(combined_result, test_gray_binary, full=True)

            diff = (diff * 255).astype("uint8")
            diff = cv2.convertScaleAbs(diff)




            thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]


            for c in contours:
                area = cv2.contourArea(c)
                if area > 40:
                    cv2.drawContours(test_image_np, [c], 0, (0, 255, 0), -1)

            cv2.namedWindow(test_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(test_name, 1024, 1024)
            cv2.imshow(test_name, test_image_np)


        label_2_start = tk.Label(master=item_frame_2,bg=bg_color_frame,
                                 text=f"Nazwa:  {test['file_name']}      Liczba punktów:  {acquired_points}      ocena:  {degree}      Status: ", font=FONT_SMALL)
        label_2_start.pack(side=tk.LEFT, fill=tk.X, padx=(10, 0), pady=5)


        label_2_status = tk.Label(master=item_frame_2, text=status, fg=color_status,bg=bg_color_frame,font=FONT_SMALL)
        label_2_status.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 0), pady=5)

        diff_button = ctk.CTkButton(master=item_frame_2,width=100, fg_color="#9A9A9A",text="Włącz podgląd",font=FONT_MEDIUM,corner_radius=2,text_color="black",
                                command=lambda t=test: show_differences(t))
        diff_button.pack(side=tk.LEFT, fill=tk.X)

        if i % 2 == 0:
            diff_button.configure(hover_color="gray")
        else:
            diff_button.configure(hover_color="#D9D9D9")

        if status == "Zaliczony":
            diff_button.pack(padx=(35,0))
        else:
            diff_button.pack(padx=(20, 0))


        label_2_end = tk.Label(master=item_frame_2, text="",bg=bg_color_frame)
        label_2_end.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 130), pady=5)

    canvas_2.update_idletasks()
    canvas_2.config(scrollregion=canvas_2.bbox("all"))

    label_summary = ctk.CTkLabel(master=right_frame_page2, text="PODSUMOWANIE", font=FONT)
    label_summary.pack(pady=10)

    label_rated = ctk.CTkLabel(master=right_frame_page2, text=f"Ocenione testy:  {graded_tests}",font=FONT, text_color="#42A5F5")
    label_rated.pack(anchor='w', padx=10, pady=5)

    label_passed = ctk.CTkLabel(master=right_frame_page2, text=f"Zaliczone:  {passed_test}",font=FONT, text_color="green")
    label_passed.pack(anchor='w',padx=10, pady=5)

    label_failed = ctk.CTkLabel(master=right_frame_page2, text=f"Niezaliczone:  {failed_tests}",font=FONT, text_color="red")
    label_failed.pack(anchor='w', padx=10,pady=5)

    label_avg_score = ctk.CTkLabel(master=right_frame_page2, text=f"Średnia ocena:  {round(summary_score / graded_tests, 2)}",font=FONT)
    label_avg_score.pack(anchor='w', padx=10,pady=5)

    label_avg_num_pt = ctk.CTkLabel(master=right_frame_page2, text=f"Średnia ilość punktów:  {round(summary_points/graded_tests,2)}",font=FONT)
    label_avg_num_pt.pack(anchor='w',padx=10, pady=5)

def raport_button_clicked():
    generate_report(graded_tests, passed_test, failed_tests,round(summary_score / graded_tests, 2),round(summary_points / graded_tests, 2))






''' ----------------------------------------  WYGLĄD -------------------------------------------- '''


button_tests_approve = ctk.CTkButton(master=page1, height=40, fg_color="#D9D9D9", text_color="black", text="Zatwierdź", font=font, corner_radius=2, hover_color="gray", command=approve_color_tests ) # Wywołanie funkcji po przetworzeniu testów
button_tests_approve.place_forget()
button_tests_add = ctk.CTkButton(master=page1, height=40, fg_color="#D9D9D9", text_color="black", text="Dodaj", font=font, corner_radius=2, hover_color="gray", command=load_tests)
button_tests_add.place_forget()

# Przyciski
button_options = ctk.CTkButton(master=toolbar_frame, height=40, fg_color="#9a9a9a", text_color=TEXT_COLOR, text="Opcje", font=font, corner_radius=0, hover_color="gray", command=toggle_options_menu)
button_options.pack(side="left")

button_create_template = ctk.CTkButton(master=toolbar_frame, height=40, fg_color=FG_COLOR, text_color=TEXT_COLOR, text="Ustawienia testu", font=font, corner_radius=1, hover_color="gray",command=toggle_test_settings)
button_create_template.pack(side="left")

button_load_template = ctk.CTkButton(master=toolbar_frame, height=40, fg_color="#9a9a9a", text_color=TEXT_COLOR, text="Wczytaj szablon", font=font, corner_radius=1, hover_color="gray", command=load_template)
button_load_template.pack(side="left")

button_load_tests = ctk.CTkButton(master=toolbar_frame, height=40, fg_color=FG_COLOR, text_color=TEXT_COLOR, text="Wczytaj testy", font=font, corner_radius=1, hover_color="gray", command=load_tests)
button_load_tests.pack(side="left")

button_evaluate = ctk.CTkButton(master=toolbar_frame, height=40, fg_color="#9a9a9a", text_color=TEXT_COLOR, text="Oceń", font=font, corner_radius=1, hover_color="gray",command=evaluate)
button_evaluate.pack(side="left")

button_create_report = ctk.CTkButton(master=toolbar_frame, height=40, fg_color="#9BCFF8", text_color=TEXT_COLOR, text="Stwórz raport", font=font, corner_radius=1, hover_color="gray",command=raport_button_clicked)
arrow_image_right = ctk.CTkImage(light_image=Image.open("Images/right-arrow.png"),
                                 size=(30, 30))

arrow_image_left = ctk.CTkImage(light_image=Image.open("Images/left-arrow.png"),
                                size=(30, 30))

button_right = ctk.CTkButton(master=toolbar_frame, height=40, width=100, image=arrow_image_right, text="", font=font, fg_color="transparent", command=show_page2, corner_radius=1, hover_color="gray")
button_right.pack(side="right")

button_left = ctk.CTkButton(master=toolbar_frame, height=40, width=100, image=arrow_image_left, text="", font=font, fg_color="transparent", command=show_page1, corner_radius=1, hover_color="gray")
button_left.pack(side="right", padx=5)

# opcje menu
options_frame = ctk.CTkFrame(master=root, width=button_options.winfo_width(), fg_color="#484545")
x = button_options.winfo_rootx()
y = button_options.winfo_rooty() + button_options.winfo_height()


button_help = ctk.CTkButton(master=options_frame, height=40, text="Pomoc", command=toggle_help_text, fg_color=FG_COLOR, hover_color="gray", corner_radius=1, text_color=TEXT_COLOR, font=font)
button_help.pack(fill="x")

button_exit = ctk.CTkButton(master=options_frame, height=40, text="Wyjdź", command=exit_program, fg_color=FG_COLOR, hover_color="gray", corner_radius=1, text_color=TEXT_COLOR, font=font)
button_exit.pack(fill="x")

# ustawienia testu
test_settings_frame = ctk.CTkFrame(master= root, width=400,height=400,fg_color="#484545",corner_radius=4,border_color="gray",border_width=1)
test_settings_frame.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
test_settings_frame.place_forget()

question_number_label = ctk.CTkLabel(master=test_settings_frame, text="Liczba pytań:")
question_number_label.grid(row=0, column=0,columnspan=2,padx=10,pady=10)

points_entry = ctk.CTkEntry(master=test_settings_frame,width=80)
points_entry.grid(row=1,column=2,columnspan=2)


max_score_label = ctk.CTkLabel(master=test_settings_frame, text="Liczba punktów: ")
max_score_label.grid(row=1, column=0,columnspan=2,padx=10,pady=10)

questions_entry = ctk.CTkEntry(master=test_settings_frame,width=80)
questions_entry.grid(row=0, column=2,columnspan=2)


grade_text_label = ctk.CTkLabel(master=test_settings_frame,text="Progi procentowe ocen")
grade_text_label.grid(row=2,column=1,columnspan=2,padx=10,pady=5)

grade_five_label = ctk.CTkLabel(master=test_settings_frame,text="Ocena 5")
grade_five_label.grid(row=3,column=0)

grade_five_entry = ctk.CTkEntry(master=test_settings_frame,width=50)
grade_five_entry.grid(row=4,column=0,padx=10)

grade_four_label = ctk.CTkLabel(master=test_settings_frame,text="Ocena 4")
grade_four_label.grid(row=3,column=1)

grade_four_entry = ctk.CTkEntry(master=test_settings_frame,width=50)
grade_four_entry.grid(row=4,column=1)

grade_three_label = ctk.CTkLabel(master=test_settings_frame,text="Ocena 3")
grade_three_label.grid(row=3,column=2)

grade_three_entry = ctk.CTkEntry(master=test_settings_frame,width=50)
grade_three_entry.grid(row=4,column=2)

pass_threshold_label = ctk.CTkLabel(master=test_settings_frame,text="Ocena 2")
pass_threshold_label.grid(row=3,column=3)

pass_entry = ctk.CTkEntry(master=test_settings_frame,width=50)
pass_entry.grid(row=4,column=3,padx=10)


button_test_settings_save = ctk.CTkButton(master=test_settings_frame, height=30, width=100 ,text="Zapisz",
                                          command=save_value,fg_color="#e0dcdc", hover_color="gray", font=font, text_color=TEXT_COLOR, corner_radius=2)
button_test_settings_save.grid(row=5, column=2,columnspan=2, padx=10, pady=(20,10))

button_test_settings_cancel = ctk.CTkButton(master=test_settings_frame, height=30, width=100, text="Anuluj",
                                            command=toggle_test_settings,fg_color="#e0dcdc", hover_color="gray", font=font, text_color=TEXT_COLOR, corner_radius=2)
button_test_settings_cancel.grid(row=5, column=0,columnspan=2, padx=10,pady=(20,10))


# pomoc menu
help_frame = ctk.CTkFrame(master=root, width=400, fg_color="#484545", corner_radius=3,border_color="gray",border_width=1)
help_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
help_frame.place_forget()

text_help_label = ctk.CTkLabel(master=help_frame, text="1. Załaduj szablon korzystając z przycisku 'Wczytaj szalbon'\n\n2. Załaduj testy które chcesz ocenić klikajac 'Wczytaj testy'\n\n3. Przejdź do zakładki 'Ustawienia testu' i ustal parametry \n\n4. Zatwierdź ustawienia i wczytane pliki\n\n5. Kliiknij 'Oceń' aby wykonać automatyczną ocenę testów\n\n6. Przejdź na drugą stronę aby zobaczyc rezultaty\n\n7. Wygeneruj raport", font=font)
text_help_label.configure(justify=tk.LEFT)
text_help_label.pack(pady=10, padx=10,side="top")


ok_button = ctk.CTkButton(master=help_frame, height=30, text="OK", command=toggle_help_text, fg_color="gray", hover_color="gray", font=font, text_color=TEXT_COLOR, corner_radius=3,width=90)
ok_button.pack(pady=10,side="bottom")

# ustawienia menu
settings_frame = ctk.CTkFrame(master=root, width=400, height=300, fg_color=FG_COLOR, corner_radius=0)
settings_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
settings_frame.place_forget()

text_settings_label = ctk.CTkLabel(master=settings_frame, text="Tutaj będa ustawienia", font=font, text_color=TEXT_COLOR)
text_settings_label.pack(pady=10, padx=10)

button_settings_cancel = ctk.CTkButton(master=settings_frame, height=30, text="Anuluj", command=toggle_settings_option, fg_color="gray", hover_color="gray", font=font, text_color=TEXT_COLOR, corner_radius=0)
button_settings_cancel.pack(side="left", padx=5, pady=5)

button_settings_approve = ctk.CTkButton(master=settings_frame, height=30, text="Zatwierdź", fg_color="gray", hover_color="gray", font=font, text_color=TEXT_COLOR, corner_radius=0)
button_settings_approve.pack(side="right", padx=5, pady=5)


separator = ctk.CTkFrame(master=page1, width=2, fg_color="gray")
separator.place(relx=0.5, rely=0.05, anchor=tk.N, relheight=0.85)

help_frame.lift(page1)
settings_frame.lift(page1)
help_frame.lift(page2)
settings_frame.lift(page2)

root.mainloop()