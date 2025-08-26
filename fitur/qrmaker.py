import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def buat_qr_dengan_label(data_qr, logo_img, label_text):
    """
    Fungsi untuk membuat satu gambar QR code dengan logo di tengah
    dan label teks di bawahnya.
    Mengembalikan object gambar PIL.
    """ 
    # --- 1. Buat QR Code dengan Logo ---
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data_qr)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    logo_size_ratio = 5
    logo_w = img_qr.size[0] // logo_size_ratio
    logo_h = img_qr.size[1] // logo_size_ratio
    
    logo_copy = logo_img.copy()
    logo_copy.thumbnail((logo_w, logo_h))

    pos_w = (img_qr.size[0] - logo_copy.size[0]) // 2
    pos_h = (img_qr.size[1] - logo_copy.size[1]) // 2
    img_qr.paste(logo_copy, (pos_w, pos_h), mask=logo_copy.split()[3] if logo_copy.mode == 'RGBA' else None)

    # --- 2. Siapkan untuk Menambahkan Label Teks ---
    try:
        # Coba gunakan font Arial yang umum. Ganti path jika perlu.
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        print("Font Arial tidak ditemukan, menggunakan font default.")
        font = ImageFont.load_default()

    # Buat object untuk menggambar
    draw = ImageDraw.Draw(img_qr)

    # Hitung ukuran teks untuk menentukan posisi
    # Menggunakan textbbox untuk akurasi yang lebih baik
    bbox = draw.textbbox((0, 0), label_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Buat kanvas baru yang lebih tinggi untuk menampung QR dan teks
    padding_bawah = 20
    tinggi_baru = img_qr.height + text_height + padding_bawah
    gambar_final = Image.new('RGB', (img_qr.width, tinggi_baru), 'white')
    
    # Tempel QR code di bagian atas kanvas baru
    gambar_final.paste(img_qr, (0, 0))
    
    # Gambar ulang untuk kanvas baru
    draw = ImageDraw.Draw(gambar_final)
    
    # Hitung posisi teks agar berada di tengah bawah
    pos_text_x = (gambar_final.width - text_width) / 2
    pos_text_y = img_qr.height + (padding_bawah / 2)
    
    # Tulis teksnya
    draw.text((pos_text_x, pos_text_y), label_text, font=font, fill="black")
    
    return gambar_final

# --- UTAMA: PENGATURAN & EKSEKUSI ---

# 1. Pengaturan Awal
kode_produksi = "00702601"
kapasitas_box = 150
nama_file_logo = 'logo.png'

# 2. Input dari Pengguna
try:
    jumlah_butir_total = int(input("Masukkan total jumlah butir telur: "))
except ValueError:
    print("❌ Error: Input harus berupa angka.")
    exit()

# 3. Memuat Gambar Logo
try:
    logo = Image.open(nama_file_logo)
except FileNotFoundError:
    print(f"❌ Error: File logo '{nama_file_logo}' tidak ditemukan.")
    exit()

# 4. Perhitungan Box
jumlah_box_penuh = jumlah_butir_total // kapasitas_box
sisa_butir = jumlah_butir_total % kapasitas_box
print(f"\nMenghitung... \n- Box Penuh (@{kapasitas_box} butir): {jumlah_box_penuh} \n- Box Sisa (@{sisa_butir} butir): {1 if sisa_butir > 0 else 0}")

# 5. Proses Pembuatan QR Code Massal
daftar_gambar_qr = []
print("Membuat QR code untuk box penuh...")
for i in range(jumlah_box_penuh):
    data_unik = f"{kode_produksi}-{kapasitas_box}"
    label = str(kapasitas_box)
    daftar_gambar_qr.append(buat_qr_dengan_label(data_unik, logo, label))

if sisa_butir > 0:
    print("Membuat QR code untuk box sisa...")
    data_unik = f"{kode_produksi}-{sisa_butir}"
    label = str(sisa_butir)
    daftar_gambar_qr.append(buat_qr_dengan_label(data_unik, logo, label))

# 6. Susun Semua QR Code ke dalam Halaman PDF (Otomatis Tambah Halaman Baru)
if not daftar_gambar_qr:
    print("Tidak ada QR code yang dibuat.")
else:
    lebar_halaman, tinggi_halaman = 1240, 1754 
    margin, spasi = 50, 20
    
    lebar_qr, tinggi_qr = daftar_gambar_qr[0].size
    
    daftar_halaman = []
    halaman_sekarang = Image.new('RGB', (lebar_halaman, tinggi_halaman), 'white')
    daftar_halaman.append(halaman_sekarang)
    
    posisi_x, posisi_y = margin, margin

    print("\nMenyusun QR code ke dalam halaman PDF...")
    for qr_img in daftar_gambar_qr:
        if posisi_x + lebar_qr > lebar_halaman - margin:
            posisi_x = margin
            posisi_y += tinggi_qr + spasi
        
        if posisi_y + tinggi_qr > tinggi_halaman - margin:
            halaman_sekarang = Image.new('RGB', (lebar_halaman, tinggi_halaman), 'white')
            daftar_halaman.append(halaman_sekarang)
            posisi_x, posisi_y = margin, margin

        halaman_sekarang.paste(qr_img, (posisi_x, posisi_y))
        posisi_x += lebar_qr + spasi

    nama_file_pdf = "hasil_qr_dengan_label.pdf"
    
    if len(daftar_halaman) > 1:
        gambar_utama = daftar_halaman[0]
        gambar_lainnya = daftar_halaman[1:]
        gambar_utama.save(
            nama_file_pdf, "PDF", resolution=150.0, save_all=True, append_images=gambar_lainnya
        )
    else:
        daftar_halaman[0].save(nama_file_pdf, "PDF", resolution=150.0)
    
    print(f"\n✅ Semua {len(daftar_gambar_qr)} QR code berhasil disusun dalam {len(daftar_halaman)} halaman dan disimpan sebagai '{nama_file_pdf}'")
