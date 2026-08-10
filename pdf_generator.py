from fpdf import FPDF
from PIL import Image

image_location = "assets/logo.png"

def generate_pdf_file(setlist):
    
    pdf = FPDF()

    pdf.image(  name= image_location,
                x = ...,
                y = 50,
                w = 100
                )


