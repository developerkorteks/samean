FROM python:3.11-slim

WORKDIR /app

# Salin requirements.txt terlebih dahulu untuk memanfaatkan Docker cache
COPY requirements.txt .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi
COPY . .

# Expose port yang digunakan aplikasi
EXPOSE 8001

# Jalankan aplikasi
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]