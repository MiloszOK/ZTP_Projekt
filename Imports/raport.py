from Imports.imports import *

def generate_report(graded_tests, passed_tests, failed_tests, avg_score, avg_points,
                    loaded_tests, test_scores, score_points, pass_threshold, grade_table):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(60,60,60)
    pdf.add_font('DejaVu', '', "../Assets/DejaVuSans.ttf")

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

    pdf.output("Assets/raport.pdf")
    CTkMessagebox(title="Sukces", message="Raport wygenerowany pomyślnie!", icon="check", text_color="white",
                button_hover_color="grey")
