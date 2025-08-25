# Griyata Promo Video (Auto Render)

Workflow ini menghasilkan video MP4 siap diputar di HP, langsung dari GitHub Actions.

## Cara pakai
1. Pastikan logo tersedia:
   - `assets/logo-griyata.png` (sudah ada)

2. Jalankan workflow:
   - Buka tab **Actions** → pilih **Render video** → klik **Run workflow** → **Run**.
   - Tunggu 2–4 menit.

3. Unduh hasil:
   - Masuk ke run terakhir → bagian **Artifacts** → unduh `griyata-promo-<run_id>.zip`.
   - Di dalamnya ada:
     - `griyata_promo.mp4` (1080p)
     - `griyata_promo_mobile.mp4` (1080p, faststart)
     - `griyata_promo_720p.mp4` (720p, ukuran lebih kecil)

## Kustomisasi
- Ubah teks:
  - Jalankan dengan argumen:
    ```bash
    python generate_griyata_video.py --title "Griyata" --subtitle1 "KPR digital" --subtitle2 "Cepat • Mudah • Transparan"
    ```
- Tambahkan musik latar:
  - Simpan ke `assets/bgm.mp3` lalu modifikasi script untuk memuat `AudioFileClip` (opsional).

## Catatan
- Codec: H.264 (yuv420p) + AAC dengan `+faststart` untuk kompatibilitas mobile.
- Durasi default: 12 detik @24 fps, 1920×1080.