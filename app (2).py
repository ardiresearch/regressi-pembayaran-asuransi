# =====================================================================
# app.py - Aplikasi web prediksi dengan Streamlit
# Jalankan dengan:  streamlit run app.py
# =====================================================================
import json
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Prediksi Regresi Linear", layout="centered")


# @st.cache_resource membuat model dimuat sekali saja, bukan setiap kali
# pengguna menekan tombol.
@st.cache_resource
def muat_berkas():
    model = joblib.load("model_terpilih.joblib")
    with open("metadata.json", encoding="utf-8") as f:
        meta = json.load(f)
    return model, meta


model, meta = muat_berkas()


def label(nama):
    """Nama kolom yang ramah dibaca; jatuh ke nama aslinya bila tak ada."""
    return meta.get("label_kolom", {}).get(nama, nama)


st.title(meta["judul_aplikasi"])
st.write(
    f"Aplikasi ini memperkirakan **{meta['label_target']}** "
    f"dalam satuan {meta['satuan_target']} menggunakan model Regresi Linear "
    "yang dilatih pada data publik Kaggle."
)

# ------------------------- Formulir masukan --------------------------
with st.form("formulir_prediksi"):
    st.subheader("Masukkan data")
    masukan = {}

    for nama in meta["kolom_numerik"]:
        batas = meta["rentang_numerik"][nama]
        if batas.get("bulat"):
            masukan[nama] = st.number_input(
                label=label(nama),
                min_value=int(batas["min"]),
                max_value=int(batas["max"]),
                value=int(batas["median"]),
                step=1,
            )
        else:
            masukan[nama] = st.number_input(
                label=label(nama),
                min_value=float(batas["min"]),
                max_value=float(batas["max"]),
                value=float(batas["median"]),
                step=0.1,
                format="%.2f",
            )

    for nama in meta["kolom_kategorik"]:
        masukan[nama] = st.selectbox(
            label=label(nama),
            options=meta["kategori_opsi"][nama],
        )

    tombol = st.form_submit_button("Hitung prediksi")

# ------------------------- Proses prediksi ---------------------------
if tombol:
    urutan = meta["kolom_numerik"] + meta["kolom_kategorik"]
    baris = pd.DataFrame([masukan])[urutan]

    hasil = float(model.predict(baris)[0])
    mae = meta["metrik_uji"]["mae"]

    # Regresi Linear tidak dibatasi: pada kombinasi masukan ekstrem ia dapat
    # menghasilkan nilai negatif, padahal target tidak mungkin negatif.
    # Nilai negatif ditampilkan sebagai peringatan, bukan disembunyikan.
    if hasil < 0:
        st.warning(
            f"Model menghasilkan nilai negatif ({hasil:,.2f} "
            f"{meta['satuan_target']}). Regresi Linear tidak memiliki batas bawah, "
            "sehingga kombinasi masukan yang ekstrem dapat keluar dari rentang "
            "yang masuk akal. Perlakukan hasil ini sebagai 'mendekati nilai "
            "terendah', bukan sebagai angka yang sahih."
        )
    else:
        st.success(
            f"Perkiraan {meta['label_target']}: "
            f"{hasil:,.2f} {meta['satuan_target']}"
        )
    st.caption(
        f"Rata-rata kesalahan model pada data uji adalah "
        f"±{mae:,.2f} {meta['satuan_target']} (MAE). "
        "Angka di atas adalah perkiraan, bukan kepastian, dan bukan nasihat keuangan."
    )

    with st.expander("Lihat data yang dikirim ke model"):
        st.dataframe(baris)

# ------------------------- Informasi model ---------------------------
with st.sidebar:
    st.header("Tentang model")
    st.write(f"R² pada data uji: {meta['metrik_uji']['r2']:.4f}")
    st.write(f"MAE: {meta['metrik_uji']['mae']:,.2f} {meta['satuan_target']}")
    st.write(f"RMSE: {meta['metrik_uji']['rmse']:,.2f} {meta['satuan_target']}")
    st.write(f"Dilatih pada: {meta['tanggal_latih']}")
    st.write(f"scikit-learn {meta['versi_sklearn']}")
    st.markdown(f"[Sumber dataset]({meta['sumber_dataset']})")

