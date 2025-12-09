#!/usr/bin/env python3
"""
GlassWorm Cross-Platform Scanner
================================

Script utama untuk menjalankan GlassWorm Scanner di berbagai sistem operasi:
- Windows 10/11
- Linux
- macOS

Fitur:
- Deteksi otomatis sistem operasi
- Lokasi ekstensi VS Code yang sesuai untuk masing-masing platform
- Laporan JSON dan HTML
- Antarmuka konsisten di semua platform
"""

import sys
import os
from pathlib import Path


def main():
    """Fungsi utama untuk menjalankan scanner lintas platform"""
    # Impor dari file yang telah kita buat
    try:
        from gwscan_crossplatform import main as scanner_main
        scanner_main()
    except ImportError as e:
        print(f"Error importing scanner: {e}")
        print("Harap pastikan file 'gwscan_crossplatform.py' ada di direktori yang sama.")
        sys.exit(1)


if __name__ == "__main__":
    main()