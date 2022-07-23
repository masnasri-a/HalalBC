""" service for creator docx files """
import traceback
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Pt, Inches

def soal_evaluasi_docx(data_evaluasi: dict) -> str:
    """ function for generating soal & jawaban evaluasi files """
    data = [
        {
            "id": 1,
            "soal": "1.	Allah SWT memerintahkan Manusia untuk konsumsi makanan yang….",
            "jawaban": {
                "a": "a.	Halal",
                "b": "b.	Thoyib",
                "c": "c.	Kotor",
                "d": "d.	a dan b"
            }
        }, {
            "id": 2,
            "soal": "2.	Berikut makanan dan minuman yang halal adalah",
            "jawaban": {
                "a": "a.	Klepon",
                "b": "b.	Anjing",
                "c": "c.	Babi",
                "d": "d.	Bangkai Ayam"
            }
        }, {
            "id": 3,
            "soal": "3.	Daging Babi dan turunannya merupakan najis",
            "jawaban": {
                "a": "a.	Ringan (mukhaffafah)",
                "b": "b.	Berat (mughallazhah)",
                "c": "c.	Sedang (mutawassithah)",
                "d": "d.	Tidak Najis"
            }
        }, {
            "id": 4,
            "soal": "4.	Cara Mengghilangkan Najis Sedang (mutawassithah) yaitu",
            "jawaban": {
                "a": "a.	Dengan mengucurinya dengan air atau mencucinya di dalam air yang banyak (direndam) hingga hilang rasa, bau dan warna dari bahan najisnya",
                "b": "b.	Di Diamkan Saja",
                "c": "c.	Di Bakar",
                "d": "d.	Dicuci tujuh kali dengan air dan salah satunya dengan tanah atau bahan lain yang mempunyai kemampuan menghilangkan rasa, bau dan warna"
            }
        }, {
            "id": 5,
            "soal": "5.	Cara Mengghilangkan Najis Berat (mughallazhah) yaitu",
            "jawaban": {
                "a": "a.	Dengan mengucurinya dengan air atau mencucinya di dalam air yang banyak (direndam) hingga hilang rasa, bau dan warna dari bahan najisnya.",
                "b": "b.	Di Diamkan Saja",
                "c": "c.	Di Bakar",
                "d": "d.	Dicuci tujuh kali dengan air dan salah satunya dengan tanah atau bahan lain yang mempunyai kemampuan menghilangkan rasa, bau dan warna."
            }
        }, {
            "id": 6,
            "soal": "6.	Cara menjaga Konsistensi dalam memproduksi Produk dan bahan yang halal perusahaan harus menerapkan",
            "jawaban": {
                "a": "a.	Sistem Keamanan Pangan",
                "b": "b.	Sistem Keselamatan Kerja",
                "c": "c.	Sistem Jaminan Halal",
                "d": "d.	Sistem Informasi"
            }
        }, {
            "id": 7,
            "soal": "7.	Kriteria Sistem Jaminan Halal Terdiri dari …. Kriteria",
            "jawaban": {
                "a": "a.	11",
                "b": "b.	20",
                "c": "c.	12",
                "d": "d.	14"
            }
        }, {
            "id": 8,
            "soal": "8.	Aktifitas manakah dibawah ini yang merupakan aktifitas kritis dalam Sistem Jaminan Halal",
            "jawaban": {
                "a": "a.	Seleksi Bahan Baru",
                "b": "b.	Pembelian",
                "c": "c.	Formulasi Produk baru",
                "d": "d.	Semua Benar"
            }
        }, {
            "id": 9,
            "soal": "9.	Setiap ada Bahan Baru perusahaan tidak wajib melaporkan kepada LPPOM MUI",
            "jawaban": {
                "a": "benar",
                "b": "salah"
            }
        }, {
            "id": 10,
            "soal": "10.	Audit Internal dilakukan 6 Bulan Sekali dan dilaporkan kepada LPPOM MUI",
            "jawaban": {
                "a": "benar",
                "b": "salah"
            }
        }
    ]
    try:
        doc = Document()
        header_style = doc.styles['Body Text']
        header_style.paragraph_format.space_after = 0
        header_style.font.bold = True
        header_style.font.size = Pt(11)
        
        task_style = doc.styles['List 2']
        task_style.paragraph_format.line_spacing = 1
        task_style.paragraph_format.space_before = Pt(2.8)
        task_style.paragraph_format.space_after = 0
        task_style.font.size = Pt(10)
        
        answer_style = doc.styles['List 3']
        answer_style.paragraph_format.line_spacing = 1
        answer_style.paragraph_format.space_after = 0
        answer_style.font.size = Pt(10)
        
        
        doc.add_paragraph(style=header_style).add_run('SOAL EVALUASI PELATIHAN INTERNAL SISTEM JAMINAN HALAL')
        sub_title = doc.add_paragraph(style=header_style).add_run('(soal ini diberikan kepada seluruh peserta pelatihan)')
        sub_title.font.italic = True
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-2].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph(style=header_style).add_run(f'NAMA\t\t: {data_evaluasi["nama"]}')
        doc.add_paragraph(style=header_style).add_run(f'TANGGAL\t: {data_evaluasi["tanggal"]}')
        doc.add_paragraph(style=header_style).add_run(f'NILAI\t\t: ')
        doc.add_paragraph(style=header_style).add_run()
        
        for task in data:
            if "c" in task['jawaban']:
                doc.add_paragraph(style=task_style).add_run(task['soal'])
                for answer in task['jawaban']:
                    ans = doc.add_paragraph(style=answer_style).add_run(task['jawaban'][answer])
                    if data_evaluasi['data'][str(task['id'])] == answer:
                        ans.font.bold = True
            else:
                rad_task_style = doc.add_paragraph(style=task_style)
                rad_task_style.add_run(task['soal'])
                rad_task_ans_1 = rad_task_style.add_run("(Benar")
                rad_task_ans_1.font.bold = True
                rad_task_ans_2 = rad_task_style.add_run("/")
                rad_task_ans_2.font.bold = True
                rad_task_ans_3 = rad_task_style.add_run("Salah)")
                rad_task_ans_3.font.bold = True
                if data_evaluasi['data'][str(task['id'])] == "b":
                    rad_task_ans_1.font.strike = True
                else:
                    rad_task_ans_3.font.strike = True
        doc.save('./app/data/coba.docx')
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error
    

def bukti_pelaksanan_docx(data_bukti_pelaksanan: dict, sign_data: dict) -> str:
    """ function for generating Bukti pelaksanaan Pelatihan internal files """
    try:
        doc = Document()
        primary_style = doc.styles['Body Text']
        primary_style.font.size = Pt(11)
        primary_style.font.bold = True
        
        
        header = doc.add_paragraph(style=primary_style).add_run('Bukti Pelaksanaan Pelatihan Internal')
        header.font.size = Pt(14)
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        
        doc.add_paragraph(style=primary_style).add_run()
        doc.add_paragraph(style=primary_style).add_run(f'Tanggal Pelatihan\t: {data_bukti_pelaksanan["tanggal_pelaksanaan"]}')
        doc.add_paragraph(style=primary_style).add_run(f'Pemateri\t\t: {data_bukti_pelaksanan["pemateri"]}')
        doc.add_paragraph(style=primary_style).add_run('Materi\t\t\t: PENGENALAN HALAL HARAM DAN PENERAPAN SJH')
        
        
        
        table = doc.add_table(rows=1, cols=5)
        table.style = 'Table Grid'
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'No'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[1].text = 'Nama Peserta'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[2].text = 'Posisi/Jabatan'
        hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[3].text = 'Tanda Tangan'
        hdr_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[4].text = 'Nilai'
        hdr_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        data = data_bukti_pelaksanan['data']
        for index in range(len(data)):
            row_cells = table.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = data[index]['nama']
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[2].text = data[index]['posisi']
            row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[3].paragraphs[0].add_run().add_picture(f'./app/data/{data[index]["ttd"]}', width=Pt(28))
            row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[4].text = str(data[index]['nilai'])
            row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        doc.add_paragraph(style=primary_style).add_run()
        
        notes = doc.add_paragraph(style=primary_style).add_run('Keterangan: \n1. Nilai Lulus  minimal 60, Jika tidak lulus harus melakukan remedial/pelatihan dan mengulang mengerjakan soal pelatihan \n2. Pelatihan internal harus menyertakan bukti foto (dokumentasi)')
        notes.font.size = Pt(10)
        
        doc.add_paragraph(style=primary_style).add_run()
        doc.add_paragraph(style=primary_style).add_run()
        
        detail_sign = doc.add_paragraph(style=primary_style).add_run(f'Jakarta, {data_bukti_pelaksanan["tanggal_pelaksanaan"]}\nMengetahui,')
        detail_sign.font.bold = False
        doc.add_paragraph(style=primary_style).add_run(f'{sign_data["title"]},')
        doc.add_picture(f'./app/data/{sign_data["sign"]}', width=Inches(1))
        doc.add_paragraph(style=primary_style).add_run(f'({sign_data["name"]})')
        
        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error