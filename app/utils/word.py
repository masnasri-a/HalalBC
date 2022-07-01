""" service for creator docx files """
import traceback
from fastapi.exceptions import HTTPException
from docx import Document
from docx.shared import Pt
from docx.enum.style import WD_STYLE_TYPE

def word_generator() -> str:
    """ function for generating word files """
    try:
        document = Document()
        # document.add_heading('MANUAL SJH', 0)
        # document.
        # document.add_heading('SISTEM JAMINAN HALAL', 0)

        font_styles = document.styles
        font_charstyle = font_styles.add_style('lampiran', WD_STYLE_TYPE.CHARACTER)
        font_object = font_charstyle.font
        font_object.size = Pt(10)
        font_object.name = 'Arial'


        paragraph = document.add_paragraph("")
        paragraph.add_run('Lampiran 6. Surat pernyataan dasar alamat fasilitas dan bebas dari babi dan turunannya').bold = True
        # paragraph.alignment = 1
        

        paragraph_1 = document.add_paragraph("")
        paragraph_1.add_run("SURAT PERNYATAAN DAFTAR ALAMAT FASILITAS PRODUKSI \nDAN BEBAS DARI BABI DAN TURUNANNYA").bold = True
        style = document.styles['Normal']
        font_1 = style.font
        font_1.name = 'Arial'
        font_1.size = Pt(12)
        paragraph_1.alignment = 1

        document.add_heading('Heading, level 1', level=1)
        document.add_paragraph('Intense quote', style='Intense Quote')

        document.add_paragraph(
            'first item in unordered list', style='List Bullet'
        )
        document.add_paragraph(
            'first item in ordered list', style='List Number'
        )

        # document.add_picture('monty-truth.png', width=Inches(1.25))

        records = (
            (3, '101', 'Spam'),
            (7, '422', 'Eggs'),
            (4, '631', 'Spam, spam, eggs, and spam')
        )

        table = document.add_table(rows=1, cols=3)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Qty'
        hdr_cells[1].text = 'Id'
        hdr_cells[2].text = 'Desc'
        for qty, _id, desc in records:
            row_cells = table.add_row().cells
            row_cells[0].text = str(qty)
            row_cells[1].text = _id
            row_cells[2].text = desc

        document.add_page_break()

        document.save('demox.docx')
    except Exception as err:
        traceback.print_exc()
        raise HTTPException(400, "failed generate file") from err


word_generator()