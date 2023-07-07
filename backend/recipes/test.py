
from fpdf import FPDF


pdf = FPDF()
pdf.add_page()
pdf.add_font('DejaVuSansCondensed', '', "d:/Dev/Диплом/foodgram-project-react/backend/recipes/ttf/DejaVuSansCondensed.ttf", uni=True)
pdf.set_font('DejaVuSansCondensed', size=16)


with open('файл', 'r') as f:
    for i in f:

        pdf.cell(200, 10, txt=i, ln=1, align='L')


pdf.output('spisok.pdf')
