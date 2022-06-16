""" service for creator docx files """
import traceback
from fastapi.exceptions import HTTPException
from docx import Document

def word_generator() -> str:
    """ function for generating word files """
    try:
        document = Document()
        document.add_heading('MANUAL SJH', 0)
        # document.
        # document.add_heading('SISTEM JAMINAN HALAL', 0)

        paragraph = document.add_paragraph("MANUAL SJH\nSISTEM JAMINAN HALAL")
        paragraph.alignment = 1

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
