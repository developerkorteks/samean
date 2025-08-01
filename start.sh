#!/bin/bash

# Aktifkan virtual environment jika ada
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Jalankan aplikasi dengan uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8001} --workers ${WORKERS:-4} --log-level info