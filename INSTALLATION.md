# Panduan Instalasi GlassWorm Advanced Scanner

## Prasyarat

### Untuk Semua Platform:
- Visual Studio Code dengan ekstensi yang terinstal
- Koneksi internet (hanya untuk mengunduh scanner, bukan untuk scanning)

### Untuk Windows:
- Windows 10 atau 11
- Python 3.x (opsional, untuk versi Python) atau PowerShell 5.1+
- Hak akses baca ke direktori ekstensi VS Code

### Untuk Linux/macOS:
- Python 3.x
- Hak akses baca ke direktori ekstensi VS Code
- Git (untuk mengunduh repositori)

## Langkah-langkah Instalasi

### 1. Unduh Scanner

**Opsi A: Clone repositori (disarankan)**
```bash
git clone https://github.com/cahyod/glassworm-scanner.git
cd glassworm-scanner
```

**Opsi B: Download manual**
- Kunjungi https://github.com/cahyod/glassworm-scanner
- Klik tombol "Code" dan pilih "Download ZIP"
- Ekstrak file ke folder pilihan Anda

### 2. Verifikasi Instalasi

**Untuk Linux/macOS:**
```bash
# Buat file skrip dapat dieksekusi
chmod +x glassworm-advanced.sh
chmod +x run_scanner.sh
```

**Untuk Windows:**
- File PowerShell mungkin perlu izin eksekusi (lihat dokumentasi utama)

### 3. Instalasi Spesifik Platform

#### Windows
Tidak perlu instalasi tambahan. Gunakan salah satu dari:
- `glassworm_windows.ps1` (dengan PowerShell)
- `glassworm_windows.bat` (dengan Command Prompt)
- `gwscan_crossplatform.py` (dengan Python)

#### Linux/macOS
Tidak perlu instalasi tambahan. Gunakan salah satu dari:
- `./run_scanner.sh` (disarankan)
- `./glassworm-advanced.sh`
- `python3 gwscan.py`

## Verifikasi Instalasi

Setelah instalasi, Anda dapat melakukan cek dasar:
- Pastikan direktori VS Code extensions ditemukan:
  - Windows: `%USERPROFILE%\.vscode\extensions`
  - Linux/macOS: `~/.vscode/extensions`
- Pastikan file scanner ada dan dapat diakses
- Cek versi Python: `python --version`

## Troubleshooting Instalasi

### Jika muncul masalah eksekusi di Linux/macOS:
```bash
# Pastikan file memiliki izin eksekusi
chmod +x glassworm-advanced.sh run_scanner.sh
```

### Jika muncul masalah di Windows PowerShell:
```powershell
# Atur kebijakan eksekusi skrip
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Jika Python tidak ditemukan:
- **Windows**: Unduh dari python.org dan instal, pastikan centang "Add Python to PATH"
- **Linux**: `sudo apt install python3` (Ubuntu/Debian) atau `sudo yum install python3` (CentOS/RHEL)
- **macOS**: `brew install python3` (jika menggunakan Homebrew)

## Pembersihan (Opsional)

Scanner hanya membaca file (tidak mengubah apapun), tapi Anda dapat membersihkan file sementara:
- Hapus direktori `glassworm-report` setelah meninjau laporan
- Hapus direktori scanner jika tidak digunakan lagi

## Update Scanner

Untuk memperbarui scanner ke versi terbaru:
```bash
# Di direktori scanner
git pull origin main
```