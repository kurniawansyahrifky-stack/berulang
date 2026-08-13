#!/bin/bash

echo "=========================================="
echo "⚡ MENYIAPKAN LINGKUNGAN BOT (VENV & REQ)"
echo "=========================================="

# 1. Cek apakah python3 tersedia
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 tidak ditemukan. Harap install python3 terlebih dahulu."
    exit 1
fi

# 2. Membuat virtual environment (venv)
if [ ! -d "venv" ]; then
    echo "📦 Membuat Virtual Environment (venv)..."
    python3 -m venv venv
else
    echo "✅ Virtual Environment sudah ada."
fi

# 3. Mengaktifkan venv dan menginstall requirements
echo "📥 Menginstall dependensi dari requirements.txt..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Membuat folder envpath jika belum ada
if [ ! -d "envpath" ]; then
    mkdir envpath
    echo "📁 Membuat folder 'envpath' untuk file konfigurasi .env bot."
fi

# 5. Membuat file contoh bot1.env jika belum ada
if [ ! -f "envpath/bot1.env" ]; then
    echo "API_ID=35873646" > envpath/bot1.env
    echo "API_HASH=3eaf9faf00e794125b7330d4978ffdce" >> envpath/bot1.env
    echo "BOT_TOKEN=ISI_TOKEN_BOT_ANDA_DISINI" >> envpath/bot1.env
    echo "OWNER_IDS=6866643730" >> envpath/bot1.env
    echo "📝 File contoh 'envpath/bot1.env' berhasil dibuat. Silakan edit token Anda di dalamnya!"
fi

echo "=========================================="
echo "🎉 SETUP SELESAI! Gunakan './run.sh bot1' untuk menjalankan bot."
echo "=========================================="
