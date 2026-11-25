# Prediksi Biaya Tagihan Asuransi Kesehatan

Proyek Akhir mata kuliah **Pembelajaran Mesin (INF62325)** - metode **Regresi Linear**.
Program Studi Informatika, UIN Siber Syekh Nurjati Cirebon.

## Aplikasi

Tautan: _(tempel tautan streamlit.app di sini setelah deploy)_

## Anggota kelompok

| Nama | NIM | Varian yang dipegang |
|---|---|---|
| _(nama)_ | _(NIM)_ | Varian 1 - Dasar |
| _(nama)_ | _(NIM)_ | Varian 2 - Perlakuan data (IQR) |
| _(nama)_ | _(NIM)_ | Varian 3 - Pemilihan fitur |

## Dataset

- Sumber: https://www.kaggle.com/datasets/mirichoi0218/insurance
- Target: `charges` - Biaya tagihan asuransi (USD)
- Fitur numerik: `age`, `bmi`
- Fitur kategorik: `sex`, `smoker`, `region`
- Tanggal pelatihan: 2026-11-25
- Lisensi: _(salin dari bagian License pada halaman Kaggle)_

## Varian yang diterapkan

Pemilihan Fitur

| Varian | MAE | RMSE | R2 |
|---|---|---|---|
| Garis dasar (rata-rata) | 9,861.80 | 13,612.43 | -0.0084 |
| Dasar | 9,620.93 | 12,589.41 | 0.1375 |
| Perlakuan Data | 9,627.47 | 12,573.91 | 0.1396 |
| Pemilihan Fitur | 4,175.91 | 5,952.15 | 0.8072 |

Alasan pemilihan: _(isi)_

## Hasil evaluasi pada data uji

| Metrik | Nilai |
|---|---|
| MAE | 4,175.91 USD |
| RMSE | 5,952.15 USD |
| R2 | 0.8072 |

## Menjalankan secara lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Catatan teknis

Seluruh preprocessing berada di dalam objek `Pipeline` yang tersimpan pada
`model_terpilih.joblib`. Aplikasi web tidak melakukan transformasi apa pun; ia hanya
menyusun satu baris `DataFrame` dari isian formulir lalu memanggil `predict`.

Versi scikit-learn disematkan di `requirements.txt` pada **1.9.1**,
sama dengan versi yang melatih model. Penyamaan ini wajib: berkas `.joblib` menyimpan
rujukan ke kelas internal scikit-learn yang berubah antar versi.

## Keterbatasan

1. _(isi - keterbatasan yang spesifik terhadap data, bukan kalimat umum)_
2. Regresi Linear tidak memiliki batas bawah, sehingga kombinasi masukan ekstrem dapat
   menghasilkan prediksi negatif. Aplikasi menampilkan peringatan bila hal ini terjadi.
3. Koefisien model menunjukkan asosiasi, bukan hubungan sebab-akibat.
4. _(isi - temuan dari grafik residual di Pertemuan 13)_

---

Aplikasi ini dibuat untuk keperluan pembelajaran.
