# Panduan Deployment KortekStream API

Dokumen ini berisi panduan untuk men-deploy KortekStream API menggunakan uvicorn di berbagai platform.

## Persiapan

1. Pastikan Python 3.8+ sudah terinstall
2. Clone repository ini
3. Buat virtual environment:
   ```bash
   python -m venv venv
   ```
4. Aktifkan virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
5. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
6. Salin file `.env.example` menjadi `.env` dan sesuaikan konfigurasi:
   ```bash
   cp .env.example .env
   ```

## Deployment Lokal

Untuk menjalankan aplikasi di lingkungan lokal:

```bash
./start.sh
```

Atau:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4
```

Aplikasi akan berjalan di `http://localhost:8001`.

## Deployment di Server Linux dengan Systemd

1. Salin file `kortekstream.service` ke direktori systemd:
   ```bash
   sudo cp kortekstream.service /etc/systemd/system/
   ```

2. Sesuaikan path dan user di file `kortekstream.service` jika diperlukan

3. Reload systemd daemon:
   ```bash
   sudo systemctl daemon-reload
   ```

4. Aktifkan service agar berjalan saat startup:
   ```bash
   sudo systemctl enable kortekstream
   ```

5. Jalankan service:
   ```bash
   sudo systemctl start kortekstream
   ```

6. Cek status service:
   ```bash
   sudo systemctl status kortekstream
   ```

## Deployment di Heroku

1. Pastikan sudah memiliki akun Heroku dan Heroku CLI terinstall
2. Login ke Heroku:
   ```bash
   heroku login
   ```

3. Buat aplikasi baru di Heroku:
   ```bash
   heroku create nama-aplikasi
   ```

4. Deploy aplikasi:
   ```bash
   git push heroku main
   ```

5. Pastikan minimal 1 dyno berjalan:
   ```bash
   heroku ps:scale web=1
   ```

6. Buka aplikasi:
   ```bash
   heroku open
   ```

## Deployment dengan Docker

1. Build Docker image:
   ```bash
   docker build -t kortekstream .
   ```

2. Jalankan container:
   ```bash
   docker run -d -p 8001:8001 --name kortekstream kortekstream
   ```

Aplikasi akan berjalan di `http://localhost:8001`.

## Catatan Penting

- Pastikan file `.env` sudah dikonfigurasi dengan benar
- Untuk production, pastikan `reload=True` tidak diaktifkan
- Gunakan jumlah workers yang sesuai dengan jumlah CPU core (biasanya 2-4 workers sudah cukup)
- Pastikan port yang digunakan tidak terblokir oleh firewall