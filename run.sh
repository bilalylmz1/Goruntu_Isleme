#!/bin/bash
if [ ! -d "venv" ]; then
    echo "Sanal ortam (venv) bulunamadı. Lütfen önce kurulumu bekleyin."
    exit 1
fi
source venv/bin/activate
python3 src/main.py
