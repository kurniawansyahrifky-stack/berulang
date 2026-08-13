#!/bin/bash

# Pastikan venv aktif
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment belum dibuat. Jalankan './setup.sh' terlebih dahulu!"
    exit 1
fi

source venv/bin/activate

# Tentukan nama bot instance dari argumen (Default: bot1)
BOT_NAME=${1:-bot1}

ENV_FILE="${BOT_NAME}.env"

if [ ! -f "envpath/$ENV_FILE" ]; then
    echo "❌ File konfigurasi 'envpath/$ENV_FILE' tidak ditemukan!"
    echo "💡 Pastikan Anda sudah membuat file env tersebut di dalam folder envpath/"
    exit 1
fi

echo "=========================================="
echo "🚀 MENJALANKAN BOT INSTANCE: [$BOT_NAME]"
echo "📁 Config Env: envpath/$ENV_FILE"
echo "=========================================="

# Menjalankan bot dengan parameter CONFIG_ENV_FILE
export CONFIG_ENV_FILE="$ENV_FILE"
python3 main.py
