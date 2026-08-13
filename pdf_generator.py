from fpdf import FPDF
from fpdf.enums import Align
from PIL import Image
import datetime as dt



image_location = "assets/logo.png"
#duration = 6500
#date = "2026-07-22"
#place = "GaragePub"
#setlist = [{'number': '1', 'title': 'droga'}, 
#           {'number': '2', 'title': 'bez slow'}, 
#           {'number': '3', 'title': 'tesknota'}, 
#           {'number': '4', 'title': 'popioly'}]
#soundcheck = {'number': '5', 'title': 'chwila'}
#bis = [ {'number': '6', 'title': 'cykl'}, 
#        {'number': '7', 'title': 'sam'}]

def generate_pdf_file(date,
                      place,
                      soundcheck,
                      setlist, 
                      setlist_duration,
                      bis):
    
    pdf = FPDF()

    pdf.add_page()

# Add and position logo
    pdf.image(  name= image_location,
                x = Align.C,
                y = 5,
                w = 200
                )

# Add place
    pdf.set_font("Times", style = "B", size = 25)
    pdf.set_y(70)
    pdf.cell(
            text = f"{place}",
            align = "C",
            center = True,
            new_y= "NEXT"
            )
    pdf.ln(10)
# Add time
    pdf.set_font("Times", style = "B", size = 25)
    pdf.cell(
            text = f"{convert_date_to_display_format(date)}r",
            align = "C",
            center = True,
            new_y= "NEXT"
            )
    pdf.ln(15)
# Add soundcheck
    pdf.line(5,pdf.get_y(),200,pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Times", style = "B", size = 20)
    pdf.cell(
            w=0,
            text= f"soundcheck: ",
            align= "L",
            )
    pdf.set_x(60)
    pdf.cell(
            w=0,
            text= f"{soundcheck["number"]}  -  {soundcheck["title"]} ",
            align= "L",
            new_y= "NEXT"
            )
    pdf.ln(5)
# Add setlit
    pdf.line(5,pdf.get_y(),200,pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Times", style = "B", size = 20)
    pdf.cell(w=0, text= "setlist: ", align= "L",new_y= "NEXT" )
    pdf.ln(5)
    pdf.set_font("Times", style = "B", size = 20)
    for row in setlist:
        pdf.set_x(60)
        pdf.cell(text = f"{row["number"]}  -  {row["title"]}",
                w = 0,
                align = "L",
                new_y= "NEXT"
                )
        pdf.ln(5)
    pdf.ln(10)
    pdf.line(x1= 5, y1= pdf.get_y(), x2= 200, y2= pdf.get_y())

# Add bis
    pdf.set_font("Times", style = "B", size = 20)
    pdf.ln(5)
    pdf.cell(w=0, text= "bis: ", align= "L", new_y= "NEXT")
    pdf.ln(5)
    for row in bis:
        pdf.set_x(60)
        pdf.cell(text = f"{row["number"]}  -  {row["title"]}",
                w = 0,
                align = "L",
                new_y= "NEXT"
                )
        pdf.ln(5)

# Save pdf file
    pdf.output(
        f"{date}_souldrone_{place}_setlist_{convert_setlist_duration_to_rounded_minutes(setlist_duration)}min.pdf"
                )




# ======================= Sub-function definition

def convert_date_to_display_format(date):

    year, month, day = date.split("-")
    d = dt.date(int(year), int(month), int(day))
    display_date = d.strftime("%d.%m.%Y")
    return display_date

def convert_setlist_duration_to_rounded_minutes(setlist_duration):

    minutes, seconds = convert_sec_to_time(setlist_duration)
    if seconds > 0:
        minutes += 1

    return minutes

def convert_sec_to_time(sec_time):
    minutes = sec_time // 60
    seconds = sec_time % 60

    return minutes, seconds

# =======================

#Only for test
#generate_pdf_file(setlist,duration,date,place,soundcheck,bis)

