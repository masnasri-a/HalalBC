""" service for creator docx files """
import traceback
from datetime import date
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
        doc.add_paragraph(style=header_style).add_run(f'TANGGAL\t: {date.fromtimestamp(int(data_evaluasi["tanggal"]) / 1000).strftime("%d %B %Y")}')
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
    

def bukti_pelaksanan_docx(data_bukti_pelaksanan: dict, sign_data: dict = {}) -> str:
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
        doc.add_paragraph(style=primary_style).add_run(f'Tanggal Pelatihan\t: {date.fromtimestamp(int(data_bukti_pelaksanan["tanggal_pelaksanaan"]) / 1000).strftime("%d %B %Y")}')
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
            if data[index]["ttd"]:
                row_cells[3].paragraphs[0].add_run().add_picture(f'./app/data/{data[index]["ttd"]}', width=Pt(28))
                row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                row_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            else:
                row_cells[3].text = ""
            row_cells[4].text = str(data[index]['nilai'])
            row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        doc.add_paragraph(style=primary_style).add_run()
        
        notes = doc.add_paragraph(style=primary_style).add_run('Keterangan: \n1. Nilai Lulus  minimal 60, Jika tidak lulus harus melakukan remedial/pelatihan dan mengulang mengerjakan soal pelatihan \n2. Pelatihan internal harus menyertakan bukti foto (dokumentasi)')
        notes.font.size = Pt(10)
        
        doc.add_paragraph(style=primary_style).add_run()
        doc.add_paragraph(style=primary_style).add_run()
        
        if sign_data:
            detail_sign = doc.add_paragraph(style=primary_style).add_run(f'Jakarta, {date.fromtimestamp(int(data_bukti_pelaksanan["tanggal_pelaksanaan"]) / 1000).strftime("%d %B %Y")}\nMengetahui,')
            detail_sign.font.bold = False
            doc.add_paragraph(style=primary_style).add_run(f'{sign_data["title"]},')
            if sign_data['sign']:
                doc.add_picture(f'./app/data/{sign_data["sign"]}', width=Inches(1))
            else:
                doc.add_paragraph(style=primary_style).add_run()
                doc.add_paragraph(style=primary_style).add_run()
                doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run(f'({sign_data["name"]})')
        else:
            detail_sign = doc.add_paragraph(style=primary_style).add_run('Jakarta, \nMengetahui,')
            detail_sign.font.bold = False
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run("Ttd + nama jelas")
        
        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error
    

def audit_internal_docx(jawaban_audit: dict, sign_data: dict = {}): 
    try:
        pertanyaan = [
            "Apakah kebijakan halal telah dijelaskan pada semua karyawan ?",
            "Apakah ada bukti sosialisasi kebijakan halal ? (daftar hadir sosialisasi)",
            "Apakah tersedia poster kebijakan halal dan edukasi halal di kantor, area produksi dan udang?",
            "Apakah ketua/anggota Tim Manajemen Halal telah mengikuti pelatihan eksternal setidaknya sekali dalam dua tahun?",
            "Apakah ada bukti pelatihan eksternal (sertifikat pelatihan) ?",
            "Apakah pelatihan internal kepada semua karyawan, termasuk karyawan baru, dengan materi seperti tercantum dalam Lampiran 3 telah dilaksanakan setidaknya setahun sekali ?",
            "Apakah ada bukti pelatihan internal (daftar hadir pelatihan) ?",
            "Apakah Daftar Bahan dengan format seperti pada Lampiran 4 telah dibuat ?",
            "Apakah nama/merk bahan dan nama produsen bahan yang dibeli sesuai dengan yang tercantum dalam Daftar Bahan Halal ?",
            "Apakah bukti pembelian (nota/kuitansi) dan contoh label kemasan (jika ada) selalu disimpan setidaknya selama 6 bulan ?",
            "Apakah setiap ada bahan baru selalu dimintakan persetujuan ke LPPOM MUI sebelum digunakan? (kecuali bahan tidak kritis dan bahan bersertifikat halal MUI yang ada di www.halalmui.org)",
            "Apakah bukti persetujuan penggunaan bahan baru dari LPPOM MUI selalu disimpan setidaknya selama dua tahun ?",
            "Apakah dilakukan pemeriksaan label bahan pada setiap pembelian atau penerimaan bahan ? (kecuali bahan tidak kritis)",
            "Apakah hasil pemeriksaan menunjukkan informasi nama bahan dan produsen yang tercantum di label sesuai dengan Daftar Bahan Halal ?",
            "Apakah ada formula/resep produk baku (untuk produk yang memiliki formula) ?",
            "Apakah bahan yang digunakan dalam produksi hanya bahan yang tercantum dalam Daftar Bahan ?",
            "Apakah formula produk yang digunakan pada proses produksi mengacu pada formula baku ?",
            "Jika terlanjur ada penggunaan bahan yang tidak tercantum dalam Daftar Bahan Halal, apakah produk yang dihasilkan tidak akan dijual ke konsumen dan dimusnahkan ?",
            "Apakah semua fasilitas dan peralatan produksi selalu dalam keadaan bersih (bebas dari najis) sebelum dan sesudah digunakan ?",
            "Apakah bahan dan produk selalu disimpan di tempat yang bersih dan terhindar dari najis?",
            "Apakah kendaraan yang digunakan untuk mengangkut produk halal dalam kondisi baik dan tidak digunakan untuk mengangkut produk lain yang diragukan kehalalannya ?",
            "Apakah setiap ada produk baru dengan merk yang sama selalu disertifikasi halal sebelum dipasarkan?",
            "Apakah setiap ada penambahan fasilitas produksi baru selalu didaftarkan untuk disertifikasi ?",
            "Apakah telah dilakukan audit internal setiap enam bulan sekali dengan cara memeriksa pelaksanaan seluruh prosedur operasional ? *",
            "Apakah audit internal dilakukan oleh ketua/ anggota Tim Manajemen Halal yang sudah mengikuti pelatihan ? *",
            "Apakah ada bukti pelaksanaan audit internal? *",
            "Apakah hasil audit internal telah dibahas dalam rapat kaji ulang manajemen yang dihadiri oleh ketua dan anggota Tim Manajemen Halal ? *",
            "Jika dalam audit internal ditemukan kelemahan, yaitu ada pertanyaan yang dijawab “tidak”, apakah segera dilakukan perbaikan agar kelemahan tersebut tidak terulang ? *",
            "Jika dalam audit internal ditemukan kelemahan, apakah ada bukti pelaksanaan perbaikan ? *",
            "Apakah ada bukti pelaksanaan rapat kaji ulang manajemen ? *",
            "Apakah form hasil audit internal yang telah terisi telah dikirimkan ke LPPOM MUI melalui Cerol? *"
        ]
        doc = Document()
        primary_style = doc.styles['Body Text']
        primary_style.font.size = Pt(11)
        
        header = doc.add_paragraph(style=primary_style).add_run('Lampiran 4.  Daftar Pertanyaan untuk Audit Internal')
        header.font.bold = True
        
        
        title = doc.add_paragraph(style=primary_style).add_run('AUDIT INTERNAL')
        title.font.size = Pt(14)
        title.font.bold = True
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        
        doc.add_paragraph(style=primary_style).add_run()
        doc.add_paragraph(style=primary_style).add_run(f'Tanggal Audit \t\t: {date.fromtimestamp(int(jawaban_audit["created_at"]) / 1000).strftime("%d %B %Y")}')
        doc.add_paragraph(style=primary_style).add_run(f'Auditor (yang mengaudit)\t: {jawaban_audit["auditee"]}')
        doc.add_paragraph(style=primary_style).add_run(f'Bagian yang di audit\t\t: {jawaban_audit["bagian_diaudit"]}')
        
        data = jawaban_audit['data']
        table = doc.add_table(rows=2, cols=5)
        table.style = 'Table Grid'
        
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'NO'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        table.cell(0,0).merge(table.cell(1,0))
        
        hdr_cells[1].text = 'PERTANYAAN'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        table.cell(0,1).merge(table.cell(1,1))
        
        
        hdr_cells[2].text = 'HASIL AUDIT'
        hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        table.cell(0,2).merge(table.cell(0,4))
        
        hdr_cells2 = table.rows[1].cells
        hdr_cells2[2].text = 'YA'
        hdr_cells2[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells2[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells2[3].text = 'TIDAK'
        hdr_cells2[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells2[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells2[4].text = 'KETERANGAN'
        hdr_cells2[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells2[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        for index in range(len(data)):
            row_cells = table.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = pertanyaan[index]
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            if data[index]['jawaban']:
                row_cells[2].text = "v"
                row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                row_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
                row_cells[3].text = ""
            else:
                row_cells[2].text = ""
                row_cells[3].text = "x"
                row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                row_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            row_cells[4].text = str(data[index]['keterangan'])
            row_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        keterangan = doc.add_paragraph(style=primary_style).add_run('*)Keterangan: Khusus pertanyaan mengenai audit internal dan kaji ulang manajemen, auditor dapat memeriksa pelaksanaan audit internal dan kaji ulang manajemen pada periode sebelumnya.')
        doc.add_paragraph(style=primary_style).add_run()
        
        if sign_data:
            detail_sign.font.bold = False
            doc.add_paragraph(style=primary_style).add_run(f'{sign_data["title"]},')
            if sign_data['sign']:
                doc.add_picture(f'./app/data/{sign_data["sign"]}', width=Inches(1))
            else:
                doc.add_paragraph(style=primary_style).add_run()
                doc.add_paragraph(style=primary_style).add_run()
                doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run(f'({sign_data["name"]})')
        else:
            detail_sign = doc.add_paragraph(style=primary_style).add_run('Jakarta, \nMengetahui,')
            detail_sign.font.bold = False
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run("Ttd + nama jelas")
        
        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error
    
def data_hadir_kaji_ulang_docx(daftar_hasil_kaji: dict, sign_data: dict):
    try:
        doc = Document()
        primary_style = doc.styles['Body Text']
        primary_style.font.size = Pt(11)
        
        
        header = doc.add_paragraph(style=primary_style).add_run('Lampiran 5.  Format Hasil Rapat Kaji Ulang Manajemen')
        header.font.bold = True
        
        title = doc.add_paragraph(style=primary_style).add_run('DAFTAR HADIR KAJI ULANG MANAJEMEN')
        title.font.size = Pt(14)
        title.font.bold = True
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        
        doc.add_paragraph(style=primary_style).add_run(f'Tanggal Kaji Ulang Manajemen\t :{date.fromtimestamp(int(daftar_hasil_kaji["tanggal"]) / 1000).strftime("%d %B %Y")}')
        # doc.add_paragraph(style=primary_style).add_run(f'Nama Pimpinan Perusahaan \t\t: {sign_data["name"]}')
        
        doc.add_paragraph(style=primary_style).add_run()
        
        
        list_orang = daftar_hasil_kaji['list_orang']
        pembahasan = daftar_hasil_kaji['pembahasan']
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'No'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[1].text = 'Nama'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[2].text = 'Jabatan/Bagian'
        hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[3].text = 'Paraf'
        hdr_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        for index in range(len(list_orang)):
            row_cells = table.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = list_orang[index]['nama']
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[2].text = list_orang[index]['jabatan']
            row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[3].text = list_orang[index]['paraf']
            row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        table2 = doc.add_table(rows=1, cols=3)
        table2.style = 'Table Grid'
        hdr_cells = table2.rows[0].cells
        hdr_cells[0].text = 'No'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[1].text = 'Pembahasan Kaji Ulang'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[2].text = 'Perbaikan (jika ada)'
        hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        for index in range(len(pembahasan)):
            row_cells = table2.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = pembahasan[index]['pembahasan']
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[2].text = pembahasan[index]['perbaikan']
            row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        doc.add_paragraph(style=primary_style).add_run()
        doc.add_paragraph(style=primary_style).add_run()
        
        if sign_data:
            detail_sign.font.bold = False
            doc.add_paragraph(style=primary_style).add_run(f'{sign_data["title"]},')
            if sign_data['sign']:
                doc.add_picture(f'./app/data/{sign_data["sign"]}', width=Inches(1))
            else:
                doc.add_paragraph(style=primary_style).add_run()
                doc.add_paragraph(style=primary_style).add_run()
                doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run(f'({sign_data["name"]})')
        else:
            detail_sign = doc.add_paragraph(style=primary_style).add_run('Jakarta, \nMengetahui,')
            detail_sign.font.bold = False
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run("Ttd + nama jelas")

        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error


def surat_pernyataan_daftar_alamat_docx():
    try:
        doc = Document()
        normal_text = doc.styles['Body Text']
        normal_text.font.size = Pt(11)


        header = doc.add_paragraph(style=normal_text).add_run("lampiran 6. Surat Pernyataan Daftar Alamat Fasilitas Produksi Dan Bebas Dari Babi dan Turunannya")
        header.font.bold = True

        doc.add_paragraph(style=normal_text).add_run()

        title = doc.add_paragraph(style=normal_text).add_run('SURAT PERNYATAAN DAFTAR ALAMAT FASILITAS PRODUKSI DAN BEBAS DARI BABI DAN TURUNANNYA')
        title.font.size = Pt(14)
        title.font.bold = True
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

        doc.add_paragraph(style=normal_text).add_run()
        doc.add_paragraph(style=normal_text).add_run()

        doc.add_paragraph(style=normal_text).add_run("Saya yang bertanda tangan dibawah ini :")
        doc.add_paragraph(style=normal_text).add_run()
        doc.add_paragraph(style=normal_text).add_run()

        doc.add_paragraph(style=normal_text).add_run(f"Nama\t\t:")
        # doc.add_paragraph(style=normal_text).add_run(f"No. Ktp\t\t: {company['ktp']}")
        doc.add_paragraph(style=normal_text).add_run(f"No. Ktp\t\t:")
        doc.add_paragraph(style=normal_text).add_run(f"No. Telepon\t:")
        doc.add_paragraph(style=normal_text).add_run(f"Jabatan\t\t:")

        doc.add_paragraph(style=normal_text).add_run()
        doc.add_paragraph(style=normal_text).add_run()

        doc.add_paragraph(style=normal_text).add_run(f"Menyatakan bahwa, alamat produksi untuk perusahaan (\t\t) yaitu :")

        doc.add_paragraph(style=normal_text).add_run()

        doc.add_paragraph(style=normal_text).add_run(f"Seluruh fasilitas tersebut dan peralatan yang kami gunakan untuk produksi adalah bebas dari cemaran babi & turunannya.")
        doc.add_paragraph(style=normal_text).add_run(f"Demikian pernyataan ini saya buat dengan sebenar sebenarnya untuk dapat dipergunakan sebagaimana mestinya.")

        doc.add_paragraph(style=normal_text).add_run()

        doc.add_paragraph(style=normal_text).add_run(f'Jakarta, {date.today().strftime("%d %B %Y")}')
        doc.add_paragraph(style=normal_text).add_run()
        doc.add_paragraph(style=normal_text).add_run()
        doc.add_paragraph(style=normal_text).add_run()
        doc.add_paragraph(style=normal_text).add_run(f"(\t\t)")

        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error

def form_pembelian_pemeriksaan_bahan_docx(pembelian: list, pembelian_impor: list):
    try:
        
        doc = Document()
        primary_style = doc.styles['Body Text']
        primary_style.font.size = Pt(11)
        
        header = doc.add_paragraph(style=primary_style).add_run('Lampiran 7.  Format Form Aktivitas Kritis')
        header.font.bold = True
        
        title = doc.add_paragraph(style=primary_style).add_run('FORM PEMBELIAN DAN PEMERIKSAAN BAHAN')
        title.font.size = Pt(14)
        title.font.bold = True
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph(style=primary_style).add_run()
        
        table = doc.add_table(rows=1, cols=7)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'No'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[1].text = 'Tanggal datang/beli'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[2].text = 'Nama/Merk Bahan'
        hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[3].text = 'Nama & Negara Produsen'
        hdr_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[4].text = 'Ada di Daftar Bahan Halal? (Ya/Tidak)'
        hdr_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[5].text = 'Exp. Date Bahan'
        hdr_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[6].text = 'Paraf'
        hdr_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        for index in range(len(pembelian)):
            row_cells = table.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = date.fromtimestamp(int(pembelian[index]['Tanggal']) / 1000).strftime("%d %B %Y")
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[2].text = pembelian[index]['nama_dan_merk']
            row_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[3].text = pembelian[index]['nama_dan_negara']
            row_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[4].text = "Ya" if pembelian[index]['halal'] else "Tidak"
            row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[5].text = date.fromtimestamp(int(pembelian[index]['exp_bahan']) / 1000).strftime("%d %B %Y")
            row_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            if pembelian[index]['paraf']:
                row_cells[6].text = ""
                # row_cells[6].paragraphs[0].add_run().add_picture(f'./app/data/{pembelian[index]["paraf"]}', width=Pt(28))
                # row_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                # row_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            else:
                row_cells[6].text = ""
        
        doc.add_paragraph(style=primary_style).add_run()
        sub_head = doc.add_paragraph(style=primary_style).add_run('Khusus Daging Impor')
        sub_head.font.bold = True
        
        table2 = doc.add_table(rows=1, cols=7)
        table2.style = 'Table Grid'
        hdr_cells = table2.rows[0].cells
        hdr_cells[0].text = 'No'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[1].text = 'Tanggal datang/beli'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[2].text = 'Nama/Merk/Kode Bahan'
        hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[3].text = 'Nama & Lokasi Produsen'
        hdr_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[4].text = 'Ada di Daftar Bahan Halal? (Ya/Tidak)'
        hdr_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[5].text = 'Kesesuaian nomor lot dengan SH per pengapalan (Ya/Tdk)'
        hdr_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[6].text = 'Paraf'
        hdr_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        for index in range(len(pembelian_impor)):
            row_cells = table2.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = date.fromtimestamp(int(pembelian_impor[index]['Tanggal']) / 1000).strftime("%d %B %Y")
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[2].text = pembelian_impor[index]['nama_dan_merk']
            row_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[3].text = pembelian_impor[index]['nama_dan_negara']
            row_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[4].text = "Ya" if pembelian_impor[index]['halal'] else "Tidak"
            row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[5].text = date.fromtimestamp(int(pembelian_impor[index]['exp_bahan']) / 1000).strftime("%d %B %Y")
            row_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            if pembelian_impor[index]['paraf']:
                row_cells[6].text = ""
                # row_cells[6].paragraphs[0].add_run().add_picture(f'./app/data/{pembelian_impor[index]["paraf"]}', width=Pt(28))
                # row_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                # row_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            else:
                row_cells[6].text = ""
        
        doc.add_paragraph(style=primary_style).add_run()
        keterangan = doc.add_paragraph(style=primary_style).add_run('Sesuaikan dengan yang digunakan perusahaan saat ini untuk masing-masing aktivitas kritis, diatas hanya contoh saja')
        keterangan.font.italic = True
        
        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error
    
def form_stok_bahan_docx(stok_barang: list):
    try:
        
        doc = Document()
        primary_style = doc.styles['Body Text']
        primary_style.font.size = Pt(11)
        
        
        header = doc.add_paragraph(style=primary_style).add_run('FORM STOK BAHAN')
        header.font.size = Pt(14)
        header.font.bold = True
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph(style=primary_style).add_run()
        
        table = doc.add_table(rows=1, cols=7)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'No'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[1].text = 'Tanggal Pembelian'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[2].text = 'Nama Bahan'
        hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[3].text = 'Jumlah Bahan Masuk'
        hdr_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[4].text = 'Jumlah Bahan Keluar'
        hdr_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[5].text = 'Sisa Stok'
        hdr_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[6].text = 'Paraf'
        hdr_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        for index in range(len(stok_barang)):
            row_cells = table.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = date.fromtimestamp(int(stok_barang[index]['tanggal_beli']) / 1000).strftime("%d %B %Y")
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[2].text = stok_barang[index]['nama_bahan']
            row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[3].text = stok_barang[index]['jumlah_bahan']
            row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[4].text = stok_barang[index]['jumlah_keluar']
            row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[5].text = stok_barang[index]['stok_sisa']
            row_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
            if stok_barang[index]['paraf']:
                row_cells[6].text = ""
                # row_cells[6].paragraphs[0].add_run().add_picture(f'./app/data/{pembelian_impor[index]["paraf"]}', width=Pt(28))
                # row_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                # row_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            else:
                row_cells[6].text = ""
        
        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error
    
    
def form_produksi_docx(produksi: list):
    try:
        
        doc = Document()
        primary_style = doc.styles['Body Text']
        primary_style.font.size = Pt(11)
        
        
        header = doc.add_paragraph(style=primary_style).add_run('FORM PRODUKSI')
        header.font.size = Pt(14)
        header.font.bold = True
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph(style=primary_style).add_run()
        
        table = doc.add_table(rows=1, cols=7)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'No'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[1].text = 'Tanggal produksi'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[2].text = 'Nama Produk'
        hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[3].text = 'Jumlah Awal'
        hdr_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[4].text = 'Jumlah Produk Keluar'
        hdr_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[5].text = 'Sisa Stok'
        hdr_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[6].text = 'Paraf'
        hdr_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        for index in range(len(produksi)):
            row_cells = table.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = date.fromtimestamp(int(produksi[index]['tanggal_produksi']) / 1000).strftime("%d %B %Y")
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[2].text = produksi[index]['nama_produk']
            row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[3].text = produksi[index]['jumlah_awal']
            row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[4].text = produksi[index]['jumlah_produk_keluar']
            row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[5].text = produksi[index]['sisa_stok']
            row_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
            if produksi[index]['paraf']:
                row_cells[6].text = ""
                # row_cells[6].paragraphs[0].add_run().add_picture(f'./app/data/{pembelian_impor[index]["paraf"]}', width=Pt(28))
                # row_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                # row_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            else:
                row_cells[6].text = ""
        
        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error
    
    
def form_pemusnahan_barang_docx(kebersihan: list):
    try:
        
        doc = Document()
        primary_style = doc.styles['Body Text']
        primary_style.font.size = Pt(11)
        
        
        header = doc.add_paragraph(style=primary_style).add_run('LAPORAN PEMUSNAHAN BARANG/PRODUK')
        header.font.size = Pt(14)
        header.font.bold = True
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph(style=primary_style).add_run()
        
        table = doc.add_table(rows=1, cols=7)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'No'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[1].text = 'Nama Produk'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[2].text = 'Kode/Tgl Produksi'
        hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[3].text = 'Jumlah'
        hdr_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[4].text = 'Penyebab'
        hdr_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[5].text = 'Tgl Pemusnahan'
        hdr_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[6].text = 'Penanggungjawab'
        hdr_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        for index in range(len(kebersihan)):
            row_cells = table.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = date.fromtimestamp(int(kebersihan[index]['tanggal_produksi']) / 1000).strftime("%d %B %Y")
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[2].text = kebersihan[index]['nama_produk']
            row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[3].text = kebersihan[index]['jumlah']
            row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[4].text = kebersihan[index]['penyebab']
            row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[5].text = date.fromtimestamp(int(kebersihan[index]['tanggal_pemusnahan']) / 1000).strftime("%d %B %Y")
            row_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[6].text = kebersihan[index]['penanggungjawab']
            row_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error
    
    
def form_pengecheckan_kebersihan_docx(kebersihan: list):
    try:
        
        doc = Document()
        primary_style = doc.styles['Body Text']
        primary_style.font.size = Pt(11)
        
        
        header = doc.add_paragraph(style=primary_style).add_run('FORM PENGECEKAN KEBERSIHAN FASILITAS PRODUKSI DAN KENDARAAN')
        header.font.size = Pt(14)
        header.font.bold = True
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph(style=primary_style).add_run()
        
        table = doc.add_table(rows=1, cols=7)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'No'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[1].text = 'Hari/Tgl'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[2].text = 'R. Produksi'
        hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[3].text = 'R. Gudang'
        hdr_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[4].text = 'Peralatan dan Mesin Produksi'
        hdr_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[5].text = 'Kebersihan Kendaraan'
        hdr_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[6].text = 'Penanggungjawab'
        hdr_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        for index in range(len(kebersihan)):
            row_cells = table.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = date.fromtimestamp(int(kebersihan[index]['tanggal']) / 1000).strftime("%d %B %Y")
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[2].text = "v" if kebersihan[index]['produksi'] else "x"
            row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[3].text = "v" if kebersihan[index]['gudang'] else "x"
            row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[4].text = "v" if kebersihan[index]['mesin'] else "x"
            row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[5].text = "v" if kebersihan[index]['kendaraan'] else "x"
            row_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[6].text = kebersihan[index]['penanggungjawab']
            row_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error
    
    
def daftar_bahan_halal_docx(bahan_halal: list, company: dict, sign_data: dict):
    try:
        doc = Document()
        primary_style = doc.styles['Body Text']
        primary_style.font.size = Pt(11)
        
        header = doc.add_paragraph(style=primary_style).add_run('Lampiran 8.  Daftar Bahan Halal (TIDAK WAJIB DIISI)')
        header.font.bold = True
        
        title = doc.add_paragraph(style=primary_style).add_run('DAFTAR BAHAN HALAL')
        title.font.size = Pt(14)
        title.font.bold = True
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph(style=primary_style).add_run(f'Nama Perusahaan\t :{company["company_name"]}')
        doc.add_paragraph(style=primary_style).add_run(f'Kelompok produk\t :{company["product_type"]}')
        
        doc.add_paragraph(style=primary_style).add_run()
        
        table = doc.add_table(rows=1, cols=9)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'No'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[1].text = 'Nama/Merk/ Kode Bahan'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[2].text = 'Nama dan Negara Produsen'
        hdr_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[3].text = 'Pemasok'
        hdr_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[4].text = 'Lembaga Penerbit'
        hdr_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[5].text = 'Nomor'
        hdr_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[6].text = 'Masa Berlaku'
        hdr_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[7].text = 'Dokumen Lain'
        hdr_cells[7].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[7].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[8].text = 'Keterangan'
        hdr_cells[8].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[8].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        for index in range(len(bahan_halal)):
            row_cells = table.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = bahan_halal[index]['nama_merk']
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[2].text = bahan_halal[index]['nama_negara']
            row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[2].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[3].text = bahan_halal[index]['pemasok']
            row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[3].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[4].text = bahan_halal[index]['penerbit']
            row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[4].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[5].text = bahan_halal[index]['nomor']
            row_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[5].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[6].text = bahan_halal[index]['masa_berlaku']
            row_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[6].text = bahan_halal[index]['keterangan']
            row_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[6].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        
        doc.add_paragraph(style=primary_style).add_run()
        
        if sign_data:
            detail_sign.font.bold = False
            doc.add_paragraph(style=primary_style).add_run(f'{sign_data["title"]},')
            if sign_data['sign']:
                doc.add_picture(f'./app/data/{sign_data["sign"]}', width=Inches(1))
            else:
                doc.add_paragraph(style=primary_style).add_run()
                doc.add_paragraph(style=primary_style).add_run()
                doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run(f'({sign_data["name"]})')
        else:
            detail_sign = doc.add_paragraph(style=primary_style).add_run('Jakarta, \nMengetahui,')
            detail_sign.font.bold = False
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run("Ttd + nama jelas")

        
        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error
    
def matrik_produk_docx(matrik: list, company: dict, sign_data: dict):
    try:
        doc = Document()
        primary_style = doc.styles['Body Text']
        primary_style.font.size = Pt(11)
        
        header = doc.add_paragraph(style=primary_style).add_run('Lampiran 9.  Matriks Produk  (TIDAK WAJIB DIISI)')
        header.font.bold = True
        
        title = doc.add_paragraph(style=primary_style).add_run('MATRIKS PRODUK')
        title.font.size = Pt(14)
        title.font.bold = True
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph(style=primary_style).add_run(f'Nama Perusahaan\t :{company["company_name"]}')
        doc.add_paragraph(style=primary_style).add_run(f'Kelompok produk\t :{company["product_type"]}')
        
        doc.add_paragraph(style=primary_style).add_run()
        
        table = doc.add_table(rows=1, cols=(2+len(matrik)))
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'No'
        hdr_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        hdr_cells[1].text = 'Nama Bahan'
        hdr_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
        
        list_barang = []
        for bahan in matrik:
            for barang in bahan['list_barang']:
                list_barang.append(barang['barang'])
        if len(list_barang) > 1:
            list_barang = list(dict.fromkeys(list_barang))
        
        for index_barang in range(len(list_barang)):
            hdr_cells[2+index_barang].text = list_barang[index_barang]
            hdr_cells[2+index_barang].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            hdr_cells[2+index_barang].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
        for index in range(len(matrik)):
            row_cells = table.add_row().cells
            row_cells[0].text = str(index + 1)
            row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[0].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            row_cells[1].text = matrik[index]['nama_bahan']
            row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row_cells[1].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
            for index_barang in range(len(list_barang)):
                row_cells[2+index_barang].text = "v" if matrik[index]['list_barang'][index_barang]['status'] else "x"
                row_cells[2+index_barang].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                row_cells[2+index_barang].vertical_alignment = WD_TABLE_ALIGNMENT.CENTER
            
        
        if sign_data:
            detail_sign.font.bold = False
            doc.add_paragraph(style=primary_style).add_run(f'{sign_data["title"]},')
            if sign_data['sign']:
                doc.add_picture(f'./app/data/{sign_data["sign"]}', width=Inches(1))
            else:
                doc.add_paragraph(style=primary_style).add_run()
                doc.add_paragraph(style=primary_style).add_run()
                doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run(f'({sign_data["name"]})')
        else:
            detail_sign = doc.add_paragraph(style=primary_style).add_run('Jakarta, \nMengetahui,')
            detail_sign.font.bold = False
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run()
            doc.add_paragraph(style=primary_style).add_run("Ttd + nama jelas")
        doc.save('./app/data/coba.docx')
        
        return './app/data/coba.docx'
    except Exception as error:
        traceback.print_exc()
        return error
    