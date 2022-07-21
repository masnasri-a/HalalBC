""" service for creator docx files """
import traceback
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

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
    