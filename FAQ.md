# Pertanyaan Umum (FAQ) - GlassWorm Advanced Scanner

## Pertanyaan Umum

### 1. Apa itu GlassWorm malware?
GlassWorm adalah jenis malware yang menyamar sebagai ekstensi Visual Studio Code (VS Code). Malware ini biasanya menyamar sebagai ekstensi yang tampak sah untuk mengelabui pengguna dan mencuri informasi sensitif atau melakukan aktivitas jahat lainnya.

### 2. Apakah scanner ini aman digunakan?
Ya, sangat aman. Scanner hanya melakukan analisis statis (membaca dan memindai) file ekstensi VS Code tanpa mengeksekusi kode apapun. Scanner tidak mengubah file ekstensi Anda.

### 3. Apakah VS Code sudah menyediakan perlindungan terhadap GlassWorm?
VS Code dan marketplace ekstensi terus diperbarui untuk mencegah ekstensi berbahaya, tapi ekstensi yang sudah terinstal sebelumnya mungkin tetap ada. Scanner ini memberikan perlindungan tambahan dengan memindai ekstensi yang terinstal di sistem Anda.

### 4. Apakah scanner ini berjalan di semua sistem operasi?
Ya, scanner ini didesain untuk berjalan di Windows 10/11, Linux, dan macOS dengan antarmuka yang disesuaikan untuk masing-masing platform.

### 5. Apakah scanner ini perlu koneksi internet saat scan?
Tidak, scanner bekerja secara offline dan tidak memerlukan koneksi internet saat proses scanning. Namun, koneksi internet dibutuhkan untuk mengunduh scanner pertama kali.

## Penggunaan Scanner

### 6. Berapa lama waktu yang dibutuhkan untuk scan?
Waktu scan tergantung pada jumlah dan ukuran ekstensi yang terinstal. Biasanya, scan lengkap memakan waktu beberapa menit.

### 7. Apakah scanner ini akan menghapus ekstensi berbahaya secara otomatis?
Tidak, scanner hanya mendeteksi dan memberikan laporan. Anda perlu menghapus ekstensi mencurigakan secara manual melalui VS Code.

### 8. Bagaimana cara menghapus ekstensi yang terdeteksi berbahaya?
1. Buka VS Code
2. Tekan `Ctrl+Shift+P` (Windows/Linux) atau `Cmd+Shift+P` (macOS)
3. Ketik "Extensions: Uninstall Extension"
4. Pilih ekstensi mencurigakan dan klik uninstall

### 9. Apakah saya perlu scan secara berkala?
Ya, disarankan untuk melakukan scan secara berkala, terutama setelah menginstal ekstensi baru atau menerima update ekstensi.

### 10. Apakah file laporan aman untuk dibagikan?
Laporan berisi informasi tentang ekstensi dan file yang terdeteksi mencurigakan. Secara umum aman untuk dibagikan untuk tujuan analisis keamanan, tapi hindari membagikan jika khawatir akan informasi sensitif.

## Hasil Scanner

### 11. Apa arti status Clean, Suspicious, dan Infected?
- **Clean**: Ekstensi memiliki kurang dari 4 indikator mencurigakan
- **Suspicious**: Ekstensi memiliki 4-10 indikator mencurigakan
- **Infected**: Ekstensi memiliki lebih dari 10 indikator mencurigakan

### 12. Apakah false positive mungkin terjadi?
Ya, beberapa ekstensi sah mungkin memiliki pola yang terdeteksi sebagai mencurigakan karena penggunaan API tertentu. Selalu tinjau hasil dengan hati-hati dan pertimbangkan sumber ekstensi.

### 13. Apakah ekstensi Suspicious berarti berbahaya?
Tidak selalu. Ekstensi Suspicious berisi beberapa indikator mencurigakan tapi belum tentu berbahaya. Tinjau sendiri kodenya jika memungkinkan, atau hapus jika tidak diperlukan.

### 14. Apakah ekstensi yang "Clean" 100% aman?
Tidak ada jaminan 100%, tapi ekstensi yang dinilai "Clean" memiliki risiko rendah karena tidak menunjukkan indikator mencurigakan yang terdeteksi oleh scanner.

### 15. Apa yang dimaksud dengan "suspicious patterns"?
Pola mencurigakan adalah potongan kode atau konfigurasi yang umumnya digunakan oleh malware, seperti:
- Panggilan jaringan keluar (network calls)
- Penggunaan API berbahaya (child_process, eval, dll.)
- Akses ke token atau credential
- Penggunaan teknik obfuscation

## Teknis

### 16. File jenis apa yang dipindai?
Scanner memindai file `.js`, `.json`, `.ts`, `.jsx`, dan `.tsx` yang umumnya ditemukan dalam ekstensi VS Code.

### 17. Apakah scanner ini mengirim data ke server eksternal?
Tidak, semua scanning dilakukan secara lokal dan tidak ada data yang dikirim ke server eksternal.

### 18. Apakah saya bisa menyesuaikan pola deteksi?
Ya, dalam versi Python, Anda bisa mengubah daftar `SUSPICIOUS_PATTERNS` untuk menyesuaikan dengan kebutuhan Anda.

### 19. Apakah scanner ini akan memperbarui dirinya sendiri?
Scanner tidak memiliki fungsi otomatis-update, tapi Anda bisa memperbarui secara manual dengan mengunduh versi terbaru dari repositori.

### 20. Apakah ada alternatif lain selain scanner ini?
Anda bisa menggunakan alat keamanan lain, tapi GlassWorm Advanced Scanner dirancang khusus untuk mendeteksi jenis ancaman yang spesifik terkait dengan ekstensi VS Code.

## Masalah Umum

### 21. Scanner tidak menemukan ekstensi apapun?
Pastikan VS Code telah terinstal dan memiliki ekstensi. Jalur ekstensi standar:
- Windows: `C:\Users\<username>\.vscode\extensions`
- Linux/macOS: `~/.vscode/extensions`

### 22. Laporan HTML tidak bisa dibuka?
Coba salah satu metode ini:
- Klik dua kali file `report.html` untuk membuka di browser default
- Gunakan perintah `python -m http.server` di direktori laporan dan buka via `http://localhost:8000`

### 23. Muncul error saat menjalankan scanner?
Periksa hal-hal berikut:
- Versi Python yang kompatibel
- Izin baca ke direktori ekstensi
- Versi PowerShell yang cukup (untuk Windows)

### 24. Bagaimana jika saya menemukan ekstensi jahat?
1. Segera uninstall ekstensi tersebut melalui VS Code
2. Laporkan ke marketplace VS Code jika memungkinkan
3. Pertimbangkan untuk memindai sistem Anda dengan alat keamanan lain
4. Ganti credential yang mungkin telah dicuri

### 25. Apakah scanner ini open source?
Ya, scanner ini open source dan tersedia di repositori publik GitHub untuk transparansi dan audit komunitas.