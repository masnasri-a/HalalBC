from fpdf import FPDF


def Lampiran(nama: str, ktp, no, jabatan, perusahaan, alamat):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(10, 15, txt="Lampiran 6. Surat pernyataan daftar alamat fasilitas dan bebas dari babi dan turunannya", ln=1)
    pdf.set_font('helvetica', style="B", size=15)
    pdf.cell(
        200, 15, txt="SURAT PERNYATAAN DAFTAR ALAMAT FASILITAS PRODUKSI", align='C', ln=1)
    pdf.set_font('helvetica', style="B")
    pdf.cell(200, 2, txt="DAN BEBAS DARI BABI DAN TURUNANNYA", align='C', ln=1)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 50, "Saya yang bertanda tangan dibawah ini: ", ln=1)
    pdf.cell(10, -30, "Nama           : "+format(nama), ln=1)
    pdf.cell(10, 45, "No KTP        : "+format(ktp), ln=1)
    pdf.cell(10, -30, "No Telp        : "+format(no), ln=1)
    pdf.cell(10, 45, "Jabatan        : "+format(jabatan), ln=1)

    pdf.cell(200, 0, 'Menyatakan bahwa alamat produksi untuk Perusahaan ' +
             perusahaan+' yaitu:', ln=1)
    pdf.cell(200, 20, alamat, ln=1)
    pdf.cell(200, 0, "Seluruh fasilitas tersebut dan peralatan yang kami gunakan untuk produksi adalah bebas", ln=1)
    pdf.cell(200, 10, "dari cemaran babi dan turunannya", ln=1)
 
    pdf.output('demox.pdf')


Lampiran("Nasri", "320230234234234", "0822228832323",
         "Pemimping perusahaan", "Pt Owi Mulet", "Jln Permata berlian blok AA no 5")
