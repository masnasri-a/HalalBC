from fpdf import FPDF
from datetime import date

def get_time_parse():
    today = date.today()
    day = today.strftime("%d")
    month = today.strftime("%m")
    if month == "01":
        month = "Januari"
    elif month == "02":
        month = "Februari"
    elif month == "03":
        month = "Maret"
    elif month == "04":
        month = "April"
    elif month == "05":
        month = "Mei"
    elif month == "06":
        month = "Juni"
    elif month == "07":
        month = "Juli"
    elif month == "08":
        month = "Agustus"
    elif month == "09":
        month = "September"
    elif month == "10":
        month = "Oktober"
    elif month == "11":
        month = "November"
    elif month == "12":
        month = "Desember"
    year = today.strftime("%Y")
    return str(day+" "+month+" "+year)

def Lampiran(nama: str, ktp, no, jabatan, perusahaan, alamat, region):
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
    pdf.cell(200, 15, "dari cemaran babi dan turunannya.", ln=1)
    pdf.set_font('helvetica', style="")
    pdf.cell(200, 0, "Demikian pernyataan ini saya buat dengan sebenar benarnya untuk dapat digunakan", ln=1)
    pdf.cell(200, 15, "sebagaimana mestinya.", ln=1)


    pdf.cell(200, 10, region+", "+get_time_parse(), ln=1)
    pdf.cell(200, 10, region+", "+get_time_parse(), ln=1)
    pdf.cell(200, 10, region+", "+get_time_parse())
    pdf.output('demox.pdf')


Lampiran("Nasri", "320230234234234", "0822228832323",
         "Pemimpin perusahaan", "Pt Owi Mulet", "Jln Permata berlian blok AA no 5",
         "Jakarta")
