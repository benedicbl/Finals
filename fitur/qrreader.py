import cv2
import pyodbc
from datetime import datetime

# --- Konfigurasi Database (Sudah Disesuaikan) ---
SERVER_NAME = r'DESKTOP-RM8VU8M\SQLEXPRESS' # Menggunakan raw string (r'') untuk handle backslash
DATABASE_NAME = 'dbTA'

# Connection String untuk Otentikasi Windows (Trusted Connection)
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"Trusted_Connection=yes;"
)

def inisialisasi_database():
    """Membuat tabel jika belum ada menggunakan pyodbc."""
    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            create_table_query = """
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='log_scan' and xtype='U')
                CREATE TABLE log_scan (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    waktu_scan DATETIME NOT NULL,
                    kode_produksi NVARCHAR(MAX) NOT NULL
                );
            """
            cursor.execute(create_table_query)
            conn.commit()
            print(f"✅ Berhasil terhubung dan tabel 'log_scan' di database '{DATABASE_NAME}' siap digunakan.")
    except pyodbc.Error as e:
        print(f"❌ Gagal terhubung atau inisialisasi database: {e}")
        exit()

def simpan_ke_db(kode_produksi):
    """Menyimpan satu entri scan ke dalam database."""
    insert_query = "INSERT INTO log_scan (waktu_scan, kode_produksi) VALUES (?, ?)"
    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            waktu_sekarang = datetime.now()
            cursor.execute(insert_query, waktu_sekarang, kode_produksi)
            conn.commit()
            return True
    except pyodbc.Error as e:
        print(f"❌ Gagal menyimpan ke database: {e}")
        return False

# --- Variabel untuk State & Counter ---
total_barang = 0
scan_ready = True

# --- Inisialisasi ---
inisialisasi_database()
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

print("\nScanner siap. Arahkan ke QR Code. Tekan 'q' untuk keluar.")

# --- Loop Utama ---
while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    data, bbox, _ = detector.detectAndDecode(frame)
    
    if data and scan_ready:
        if simpan_ke_db(data):
            total_barang += 1
            print(f"✅ Scan Berhasil! Kode '{data}' disimpan ke DB. Total: {total_barang}")
            scan_ready = False
            cv2.putText(frame, "Scan Berhasil!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
    elif not data:
        scan_ready = True
        
    # --- Bagian visualisasi ---
    if not scan_ready:
        instruction_text = "Jauhkan QR dari kamera..."
        cv2.putText(frame, instruction_text, (50, 100), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 1)
    else:
        cv2.putText(frame, "SIAP SCAN", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)

    status_text = f"Total Barang Hari Ini: {total_barang}"
    cv2.putText(frame, status_text, (50, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow('QR Scanner -> SQL Server', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("\nMenutup aplikasi...")
cap.release()
cv2.destroyAllWindows()