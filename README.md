# GlassWorm Advanced Scanner

**Advanced Security Scanner untuk VS Code Extensions - Cross-Platform (Windows, Linux, macOS)**

GlassWorm adalah alat keamanan canggih yang dirancang untuk mendeteksi potensi malware dan ancaman keamanan pada ekstensi Visual Studio Code. Alat ini melakukan analisis mendalam terhadap file ekstensi tanpa mengeksekusi kode berpotensi berbahaya. 

## 📋 Daftar Isi
- [Fitur Utama](#-fitur-utama)
- [Kebutuhan Sistem](#-kebutuhan-sistem)
- [Instalasi](#-instalasi)
- [Cara Menjalankan Scanner](#-cara-menjalankan-scanner)
  - [Untuk Windows](#untuk-windows)
  - [Untuk Linux/macOS](#untuk-linuxmacos)
- [Contoh Hasil](#-contoh-hasil)
- [Sistem Penilaian Risiko](#-sistem-penilaian-risiko)
- [Output Laporan](#-output-laporan)
- [Struktur File](#-struktur-file)
- [Cara Kerjanya](#-cara-kerjanya)
- [Pola Deteksi](#-pola-deteksi)
- [Catatan Keamanan](#-catatan-keamanan)
- [Kontak](#-kontak)

## 🚀 Fitur Utama

- **Deep scan** dari ekstensi VS Code
- **Deteksi pola mencurigakan**:
  - Komunikasi C2 (Solana, Google Calendar, RPC langsung)
  - Akses token GitHub/NPM
  - Obfuscation dan payload eval/base64
  - Network beacon tersembunyi
  - Abuse proses anak Node.js
- **Pemeriksaan integritas file** dengan hashing
- **Penilaian risiko otomatis** (clean/suspicious/infected)
- **Laporan HTML dan JSON** interaktif
- **Analisis statis saja** (tidak mengeksekusi kode berbahaya)
- **Kompatibel lintas platform** (Windows, Linux, macOS)

## 📋 Kebutuhan Sistem

### Untuk Linux/macOS:
- Python 3
- VS Code dengan ekstensi yang terinstal
- Bash shell (Linux)

### Untuk Windows:
- Windows 10/11
- Python 3 atau PowerShell 5.1+
- VS Code dengan ekstensi yang terinstal

## 🛠️ Instalasi

1. **Clone repositori:**
   ```bash
   git clone https://github.com/cahyod/glassworm-scanner.git
   cd glassworm-scanner
   ```

2. **(Linux/macOS saja) Buat skrip eksekutabel:**
   ```bash
   chmod +x glassworm-advanced.sh
   chmod +x run_scanner.sh
   ```

## ▶️ Cara Menjalankan Scanner

### Untuk Windows:
Anda memiliki beberapa pilihan untuk menjalankan scanner di Windows:

#### Metode 1: Menggunakan skrip PowerShell (Disarankan)
```powershell
# Pastikan untuk mengizinkan eksekusi skrip (sekali saja):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Jalankan scanner:
.\glassworm_windows.ps1
```

#### Metode 2: Menggunakan Python (jika telah terinstal)
```cmd
python gwscan_crossplatform.py
```

#### Metode 3: Menggunakan file batch Windows
```cmd
.\glassworm_windows.bat
```

### Untuk Linux/macOS:
#### Metode 1: Menggunakan skrip wrapper (Disarankan)
```bash
./run_scanner.sh
```

#### Metode 2: Eksekusi langsung
```bash
./glassworm-advanced.sh
```

#### Metode 3: Eksekusi Python langsung
```bash
python3 gwscan.py
```

#### Metode 4: Scanner Python lintas platform
```bash
python3 glassworm_crossplatform.py
```

## 🖼️ Contoh Hasil

Lihat hasil scan sampel di direktori [images](images/) untuk melihat seperti apa tampilan laporan.

Untuk pengalaman terbaik saat melihat laporan HTML, Anda dapat:

### Pada Linux/macOS:
- Buka dengan Firefox: `firefox ~/glassworm-report/report.html`
- Akses via HTTP: `cd ~/glassworm-report && python3 -m http.server 8080` dan buka via `http://localhost:8080/report.html`

### Pada Windows:
- Klik dua kali file `report.html` untuk membuka di browser default
- Atau gunakan PowerShell: `Start-Process "C:\Users\$env:USERNAME\glassworm-report\report.html"`
- Atau gunakan Command Prompt: `start C:\Users\%USERNAME%\glassworm-report\report.html`

## 📊 Sistem Penilaian Risiko

- 🟢 **Clean**: Kurang dari 4 indikator mencurigakan ditemukan
- 🟠 **Suspicious**: 4-10 indikator mencurigakan ditemukan  
- 🔴 **Infected**: Lebih dari 10 indikator mencurigakan ditemukan

## 📊 Output Laporan

Setelah scan selesai, laporan akan dihasilkan di lokasi berdasarkan sistem operasi:

### Pada Linux/macOS:
- Lokasi: `~/glassworm-report/`
- `report.json` - Data JSON mentah dengan semua temuan
- `report.html` - Laporan HTML interaktif yang dapat dibuka di browser

### Pada Windows:
- Lokasi: `C:\Users\%USERNAME%\glassworm-report\`
- `report.json` - Data JSON mentah dengan semua temuan
- `report.html` - Laporan HTML interaktif yang dapat dibuka di browser

Laporan HTML menyediakan:
- Ringkasan visual hasil scan dengan jumlah ekstensi clean/suspicious/infected
- Indikator risiko berwarna (Clean, Suspicious, Infected)
- Analisis ekstensi terperinci menunjukkan file dan pola mencurigakan
- Tampilan yang kompatibel dengan browser (bekerja saat dibuka dengan protokol file://)
- Desain responsif untuk navigasi mudah

## 🗂️ Lokasi Direktori Ekstensi VS Code

Scanner mencari ekstensi VS Code di lokasi berdasarkan sistem operasi:

### Pada Linux/macOS:
- Lokasi: `~/.vscode/extensions`

### Pada Windows:
- Lokasi: `C:\Users\%USERNAME%\.vscode\extensions`

## 📁 Struktur File

GlassWorm Scanner mencakup:

- `glassworm-advanced.sh` - Skrip bash utama dengan Python tersemat (Linux/macOS)
- `gwscan.py` - Modul scanner Python mandiri
- `gwscan_crossplatform.py` - Scanner Python lintas platform dengan penanganan path spesifik OS
- `glassworm_crossplatform.py` - Titik masuk utama Python lintas platform
- `glassworm_windows.ps1` - Skrip PowerShell untuk Windows
- `glassworm_windows.bat` - Skrip batch Windows
- `run_scanner.sh` - Skrip wrapper kenyamanan (Linux/macOS)
- `requirements.txt` - Kebutuhan Python (hanya menggunakan pustaka standar)
- `.gitignore` - File git ignore untuk pengembangan
- `README.md` - Dokumentasi ini

## 🛠️ Cara Kerjanya

Scanner:

1. **Menemukan ekstensi** di direktori ekstensi spesifik OS
2. **Menjelajahi** setiap direktori ekstensi
3. **Menganalisis** file `.js`, `.json`, `.ts`, `.jsx`, dan `.tsx` untuk pola mencurigakan
4. **Menghitung** skor risiko berdasarkan jumlah indikator mencurigakan
5. **Menghasilkan** laporan JSON dan HTML dengan temuan
6. **Memberi peringkat** setiap ekstensi sebagai Clean, Suspicious, atau Infected

## 🔍 Pola Deteksi

Scanner mencari pola-pola mencurigakan berikut dalam file ekstensi:

- **C2 Solana**: `(solana|mainnet-beta|rpc)`
- **C2 Google Calendar**: `googleapis\.com/calendar`
- **Akses Token**: `(GITHUB_TOKEN|npmrc|PAT|accessToken)`
- **Obfuscation**: `(eval\(|Function\(|atob\(|btoa\(|base64)`
- **API Berbahaya**: `(child_process|spawn|exec)`
- **Panggilan Jaringan**: `(fetch\(|axios|http|https)`
- **Domain Mencurigakan**: `(pastebin|ipfs|raw\.githubusercontent|tunnel)`

## 🔒 Catatan Keamanan

- Melakukan **analisis statis saja** - tidak mengeksekusi kode berpotensi berbahaya
- **Tidak mengubah** ekstensi Anda atau instalasi VS Code
- **Aman untuk dijalankan** di sistem Anda
- Semua operasi bersifat baca-saja

## Contact
E-mail: cahyod@yahoo.co.id
Github: https://github.com/cahyod/glassworm-scanner.git