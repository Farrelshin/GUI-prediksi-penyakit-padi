import streamlit as st
import numpy as np
import pickle

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Rice Guard | Deteksi Penyakit Padi",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Google Font ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---- Background ---- */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #161616 40%, #000000 100%);
    min-height: 100vh;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #121212 0%, #1c1c1c 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}
[data-testid="stSidebar"] * { color: #ffffff !important; }
[data-testid="stSidebar"] .stNumberInput label { color: #e0e0e0 !important; font-size: 0.82rem !important; }
[data-testid="stSidebar"] input {
    background: rgba(30, 30, 30, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: #ffffff !important;
    box-shadow: 0 0 0 2px rgba(255,255,255,0.2) !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(30, 30, 30, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}

/* ---- Hero header ---- */
.hero {
    background: linear-gradient(135deg, rgba(30,30,30,0.9) 0%, rgba(20,20,20,0.95) 100%);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 20px;
}
.hero-icon { font-size: 3.2rem; }
.hero-title { font-size: 1.85rem; font-weight: 700; color: #ffffff; line-height: 1.2; }
.hero-sub   { font-size: 0.92rem; color: #b0b0b0; margin-top: 4px; }

/* ---- Metric cards ---- */
.metric-row { display: flex; gap: 16px; margin-bottom: 24px; }
.metric-card {
    flex: 1;
    background: rgba(30,30,30,0.7);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 18px 22px;
    text-align: center;
}
.metric-card .m-value { font-size: 2rem; font-weight: 700; color: #ffffff; }
.metric-card .m-label { font-size: 0.78rem; color: #b0b0b0; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px; }

/* ── Accuracy gauge-style card ── */
.acc-card {
    background: linear-gradient(135deg, rgba(40,40,40,0.8), rgba(60,60,60,0.4));
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 12px;
    padding: 18px 22px;
    text-align: center;
    flex: 1;
}
.acc-card .acc-value { font-size: 2.2rem; font-weight: 700; color: #ffffff; }
.acc-card .acc-label { font-size: 0.78rem; color: #e0e0e0; text-transform: uppercase; letter-spacing: 0.08em; }
.acc-badge {
    display: inline-block;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.3);
    color: #ffffff;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 20px;
    margin-top: 6px;
    letter-spacing: 0.04em;
}

/* ---- Section divider ---- */
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #ffffff;
    margin: 0 0 12px 0;
    border-left: 3px solid #ffffff;
    padding-left: 10px;
}

/* ---- Result cards ---- */
.result-healthy {
    background: linear-gradient(135deg, rgba(40,40,40,0.85), rgba(60,60,60,0.5));
    border: 1.5px solid #ffffff;
    border-radius: 14px;
    padding: 28px 32px;
    text-align: center;
}
.result-disease {
    background: linear-gradient(135deg, rgba(140,20,20,0.7), rgba(160,30,30,0.4));
    border: 1.5px solid #ff4d4d;
    border-radius: 14px;
    padding: 28px 32px;
    text-align: center;
}
.result-warning {
    background: linear-gradient(135deg, rgba(200,100,0,0.6), rgba(220,120,20,0.3));
    border: 1.5px solid #ff9800;
    border-radius: 14px;
    padding: 28px 32px;
    text-align: center;
}
.result-status { font-size: 1.5rem; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
.result-desc   { font-size: 0.92rem; color: #e0e0e0; line-height: 1.6; }
.result-icon   { font-size: 3rem; margin-bottom: 14px; }

/* ---- Primary button ---- */
.stButton > button {
    background: linear-gradient(135deg, #222222, #444444) !important;
    color: #ffffff !important;
    border: 1px solid #ffffff !important;
    border-radius: 10px !important;
    padding: 12px 32px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #444444, #666666) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(255,255,255,0.15) !important;
}

/* ---- Input number tweaks in main ---- */
[data-testid="stNumberInput"] input {
    background: rgba(30,30,30,0.5) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}
[data-testid="stNumberInput"] label { color: #e0e0e0 !important; font-size: 0.82rem !important; }

/* ---- Feature importance bar ---- */
.fi-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.fi-label { color: #e0e0e0; font-size: 0.8rem; width: 200px; flex-shrink: 0; }
.fi-bar-bg { flex: 1; background: rgba(50,50,50,0.7); border-radius: 4px; height: 8px; }
.fi-bar { background: linear-gradient(90deg, #666666, #ffffff); border-radius: 4px; height: 8px; }
.fi-pct { color: #b0b0b0; font-size: 0.78rem; width: 42px; text-align: right; flex-shrink: 0; }

/* ---- Model comparison bars ---- */
.model-cmp-row { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
.model-cmp-label { color: #e0e0e0; font-size: 0.82rem; font-weight: 600; width: 170px; flex-shrink: 0; }
.model-cmp-bar-bg { flex: 1; background: rgba(30,30,30,0.8); border-radius: 6px; height: 18px; border: 1px solid rgba(255,255,255,0.1); overflow: hidden; }
.model-cmp-bar-rf  { background: linear-gradient(90deg, #333333, #888888, #ffffff); border-radius: 6px; height: 18px; }
.model-cmp-bar-dt  { background: linear-gradient(90deg, #555555, #bbbbbb); border-radius: 6px; height: 18px; }
.model-cmp-bar-knn { background: linear-gradient(90deg, #444444, #999999); border-radius: 6px; height: 18px; }
.model-cmp-pct { color: #ffffff; font-size: 0.82rem; font-weight: 700; width: 50px; text-align: right; flex-shrink: 0; }
.model-cmp-active-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.6);
    color: #ffffff;
    font-size: 0.62rem;
    font-weight: 700;
    padding: 1px 7px;
    border-radius: 20px;
    margin-left: 6px;
    letter-spacing: 0.06em;
    vertical-align: middle;
}

/* ---- Sidebar section title ---- */
.sb-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #ffffff !important;
    margin: 20px 0 8px 0;
    padding-left: 8px;
    border-left: 3px solid #ffffff;
}

/* ---- KNN info card ---- */
.knn-info {
    background: rgba(40,40,40,0.6);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 8px;
}

/* ---- Generic text color fix ---- */
p, span, div { color: #ffffff; }
h1, h2, h3   { color: #ffffff; }

/* ─ hide streamlit branding ─ */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Load model artefacts ────────────────────────────────────────
@st.cache_resource
def load_artefacts():
    try:
        scaler   = pickle.load(open('scaler_padi.pkl',   'rb'))
        features = pickle.load(open('model_features.pkl','rb'))
    except FileNotFoundError:
        return None, None, None, None, None, None

    # ── Decision Tree ──
    try:
        model_dt  = pickle.load(open('model_padi_dt.pkl', 'rb'))
    except FileNotFoundError:
        model_dt = None
    try:
        acc_dt = pickle.load(open('model_accuracy_dt.pkl', 'rb'))
    except FileNotFoundError:
        try:
            acc_dt = pickle.load(open('model_accuracy.pkl', 'rb'))
        except FileNotFoundError:
            acc_dt = 92.0


    # ── K-Nearest Neighbors ──
    try:
        model_knn = pickle.load(open('model_padi_knn.pkl', 'rb'))
    except FileNotFoundError:
        model_knn = None
    try:
        acc_knn = pickle.load(open('model_accuracy_knn.pkl', 'rb'))
    except FileNotFoundError:
        acc_knn = 87.5

    return scaler, features, model_dt, acc_dt, model_knn, acc_knn


scaler, FEATURES, model_dt, acc_dt, model_knn, acc_knn = load_artefacts()

MODEL_MAP = {
    "Decision Tree": {
        "model":    model_dt,
        "accuracy": acc_dt,
        "badge":    "DT · Decision Tree",
        "has_fi":   True,
    },
    "K-Nearest Neighbors": {
        "model":    model_knn,
        "accuracy": acc_knn,
        "badge":    "KNN · K-Nearest Neighbors",
        "has_fi":   False,
    },
}


# ── Disease metadata ────────────────────────────────────────────
DISEASE_INFO = {
    'Padi Sehat': {
        'icon': '✅', 'type': 'healthy',
        'desc': 'Kondisi lingkungan optimal dan mendukung pertumbuhan padi yang sehat. Pertahankan pola irigasi dan pemupukan yang ada.',
        'tips': ['Pantau rutin setiap 7 hari', 'Jaga drainase lahan', 'Lanjutkan pemupukan berimbang'],
    },
    'Penyakit Blas': {
        'icon': '🦠', 'type': 'disease',
        'desc': 'Kondisi mendukung jamur Magnaporthe oryzae. Hawar Blas dapat merusak leher malai dan menyebabkan kehilangan hasil panen hingga 70%.',
        'tips': ['Semprotkan fungisida berbahan aktif Trisiklazol', 'Kurangi kelembapan dengan perbaikan drainase', 'Hindari pemupukan N berlebihan'],
    },
    'Hawar Daun': {
        'icon': '🍂', 'type': 'disease',
        'desc': 'Bakteri Xanthomonas oryzae pv. oryzae aktif. Penyakit ini dapat menyebar cepat terutama saat angin kencang dan hujan deras.',
        'tips': ['Gunakan varietas tahan hawar daun', 'Semprotkan bakterisida berbasis tembaga', 'Hindari irigasi berlebih di pagi hari'],
    },
    'Penyakit Tungro': {
        'icon': '🐛', 'type': 'disease',
        'desc': 'Virus Tungro ditularkan oleh wereng hijau. Daun menguning dimulai dari ujung dan tanaman kerdil adalah tanda khas infeksi.',
        'tips': ['Kendalikan populasi wereng hijau dengan insektisida', 'Tanam varietas tahan Tungro', 'Lakukan penanaman serempak'],
    },
    'Hama Pelipat Daun': {
        'icon': '🪲', 'type': 'warning',
        'desc': 'Larva Cnaphalocrocis medinalis melipat dan menggerek daun padi. Serangan berat mengurangi area fotosintesis secara signifikan.',
        'tips': ['Lepaskan musuh alami (parasitoid)', 'Gunakan lampu perangkap pada malam hari', 'Semprotkan insektisida jika populasi > 10 larva/rumpun'],
    },
    'Serangan Serangga': {
        'icon': '🦗', 'type': 'warning',
        'desc': 'Terdeteksi kondisi yang mendukung serangan serangga hama umum seperti wereng coklat atau kepik hijau pada lahan Anda.',
        'tips': ['Pasang perangkap serangga di sekitar lahan', 'Periksa bagian bawah daun secara berkala', 'Pertimbangkan aplikasi insektisida sistemik'],
    },
    'Penyakit Garis Daun': {
        'icon': '📊', 'type': 'disease',
        'desc': 'Gejala garis-garis kuning atau coklat pada daun padi terdeteksi. Dapat disebabkan oleh virus atau defisiensi hara.',
        'tips': ['Uji sampel daun di laboratorium pertanian', 'Periksa status hara tanah', 'Konsultasikan dengan penyuluh pertanian setempat'],
    },
}


# ─────────────────────────────────────────────────────────────
# SIDEBAR — Input Panel
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌾 Smart Rice Guard")
    st.markdown("<p style='color:#b0b0b0;font-size:0.82rem;margin-top:-8px;'>v3.0 · Multi-Model · 10 Parameter Iklim</p>", unsafe_allow_html=True)
    st.markdown("---")

    if scaler is None:
        st.error("⚠️ Artefak model tidak ditemukan!\nPastikan `scaler_padi.pkl` & `model_features.pkl` tersedia, lalu jalankan ulang.")
        st.stop()

    st.markdown("<div class='sb-title'>🤖 Pilih Model Analisis</div>", unsafe_allow_html=True)
    selected_model_name = st.selectbox(
        label="Model",
        options=list(MODEL_MAP.keys()),
        index=0,
        label_visibility="collapsed",
    )

    active_info     = MODEL_MAP[selected_model_name]
    active_model    = active_info["model"]
    active_accuracy = active_info["accuracy"]
    active_badge    = active_info["badge"]
    active_has_fi   = active_info["has_fi"]

    st.markdown(f"""
    <div style='background:rgba(50,50,50,0.3);border:1px solid rgba(255,255,255,0.2);
    border-radius:10px;padding:14px;text-align:center;margin-top:10px;margin-bottom:16px;'>
        <div style='font-size:0.72rem;color:#b0b0b0;letter-spacing:0.08em;text-transform:uppercase;'>Akurasi Model Aktif</div>
        <div style='font-size:2rem;font-weight:700;color:#ffffff;'>{active_accuracy}%</div>
        <div style='font-size:0.7rem;color:#e0e0e0;margin-top:2px;'>{active_badge} · 10 Fitur · 150 Data</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sb-title'>🌡️ Temperatur</div>", unsafe_allow_html=True)
    suhu_maks  = st.number_input("Suhu Maksimal (°C)",           min_value=30.0,  max_value=50.0,   value=39.7,  step=0.1)

    st.markdown("<div class='sb-title'>🌧️ Curah Hujan & Radiasi</div>", unsafe_allow_html=True)
    curah_hujan = st.number_input("Total Curah Hujan (mm)",       min_value=0.0,   max_value=1500.0, value=197.5, step=1.0)

    st.markdown("<div class='sb-title'>💧 Kelembapan</div>", unsafe_allow_html=True)
    kel_udara      = st.number_input("Kelembapan Udara (%)",            min_value=4.0,  max_value=18.0, value=10.0,  step=0.1)
    kel_tanah_akar = st.number_input("Kelembapan Tanah Akar (0–1)",     min_value=0.0,  max_value=1.0,  value=0.49,  step=0.01, format="%.3f")

    st.markdown("---")
    predict_btn = st.button("🔍 Analisis Sekarang", type="primary")


# ─────────────────────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="hero">
    <div class="hero-icon">🌾</div>
    <div>
        <div class="hero-title">Smart Rice Guard</div>
        <div class="hero-sub">
            Sistem Deteksi Dini Penyakit Tanaman Padi Berbasis Machine Learning ·
            Model Aktif: <strong style="color:#ffffff; text-decoration: underline;">{selected_model_name}</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="acc-card">
        <div class="acc-value">{active_accuracy}%</div>
        <div class="acc-label">Akurasi Model</div>
        <div class="acc-badge">{selected_model_name}</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="metric-card">
        <div class="m-value">10</div>
        <div class="m-label">Parameter Input</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="metric-card">
        <div class="m-value">7</div>
        <div class="m-label">Kelas Penyakit</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""<div class="metric-card">
        <div class="m-value">150</div>
        <div class="m-label">Data Pelatihan</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Perbandingan Performa Model ──────────────────────────────
st.markdown("<div class='section-label'>📊 Perbandingan Performa Model</div>", unsafe_allow_html=True)

model_comparison_data = [
    ("Decision Tree",        acc_dt,  "model-cmp-bar-dt",  selected_model_name == "Decision Tree"),
    ("K-Nearest Neighbors",  acc_knn, "model-cmp-bar-knn", selected_model_name == "K-Nearest Neighbors"),
]
model_comparison_data = sorted(model_comparison_data, key=lambda x: x[1], reverse=True)

def _build_comparison_html(data):
    rows = ""
    for name, acc, bar_class, is_active in data:
        badge   = "<span class='model-cmp-active-badge'>AKTIF</span>" if is_active else ""
        bw      = round(float(acc), 1)
        lstyle  = "border-left:3px solid #ffffff;padding-left:10px;border-radius:3px;" if is_active else ""
        rows += (
            f"<div class='model-cmp-row' style='{lstyle}'>"
            f"<div class='model-cmp-label'>{name}{badge}</div>"
            f"<div class='model-cmp-bar-bg'><div class='{bar_class}' style='width:{bw}%;'></div></div>"
            f"<div class='model-cmp-pct'>{bw}%</div>"
            f"</div>"
        )
    return (
        "<div style='background:rgba(30,30,30,0.7);border:1px solid rgba(255,255,255,0.15);"
        "border-radius:12px;padding:20px 24px;margin-bottom:20px;'>"
        + rows +
        "</div>"
    )

st.markdown(_build_comparison_html(model_comparison_data), unsafe_allow_html=True)

# ── Layout Dua Kolom: Hasil | Feature Importance ──────────────
col_result, col_fi = st.columns([3, 2], gap="large")

with col_result:
    st.markdown("<div class='section-label'>Hasil Analisis</div>", unsafe_allow_html=True)

    if predict_btn:
        model_to_use   = active_model if active_model is not None else model_dt
        using_fallback = (active_model is None)
        if model_to_use is None:
            st.error("❌ Tidak ada model yang tersedia. Pastikan minimal `model_padi_dt.pkl` ada.")
            st.stop()

        if using_fallback:
            pkl_name = 'knn'
            st.markdown(
                f"<div style='background:rgba(50,35,0,0.6);border:1px solid rgba(255,167,38,0.4);"
                f"border-radius:8px;padding:10px 14px;margin-bottom:12px;font-size:0.8rem;color:#ffcc80;'>"
                f"ℹ️ File <code style='color:#ffe082;background:rgba(255,255,255,0.08);"
                f"padding:1px 5px;border-radius:4px;'>model_padi_{pkl_name}.pkl</code> "
                f"belum tersedia — prediksi menggunakan <strong>Decision Tree</strong> sebagai cadangan."
                f"</div>",
                unsafe_allow_html=True
            )

        input_values = [
            suhu_maks, curah_hujan, kel_tanah_akar,kel_udara
        ]
        input_arr    = np.array([input_values])
        input_scaled = scaler.transform(input_arr)
        prediction   = model_to_use.predict(input_scaled)[0]
        proba        = model_to_use.predict_proba(input_scaled)[0]
        confidence   = round(max(proba) * 100, 1)

        info = DISEASE_INFO.get(prediction, {
            'icon': '⚠️', 'type': 'warning',
            'desc': 'Kondisi terdeteksi memerlukan perhatian lebih lanjut.',
            'tips': ['Hubungi penyuluh pertanian setempat'],
        })

        card_class = {
            'healthy': 'result-healthy',
            'disease': 'result-disease',
            'warning': 'result-warning',
        }.get(info['type'], 'result-warning')

        model_label_note = ""
        if active_model is None:
            model_label_note = f"<div style='font-size:0.72rem;color:#ffa726;margin-top:6px;'>⚠ File {selected_model_name} belum ada · Menggunakan Decision Tree</div>"

        st.markdown(f"""
        <div class="{card_class}">
            <div class="result-icon">{info['icon']}</div>
            <div class="result-status">{prediction}</div>
            <div class="result-desc">{info['desc']}</div>
            {model_label_note}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"""
            <div style='background:rgba(30,30,30,0.7);border:1px solid rgba(255,255,255,0.15);
            border-radius:10px;padding:16px;text-align:center;'>
                <div style='font-size:0.7rem;color:#b0b0b0;text-transform:uppercase;letter-spacing:.08em;'>Kepercayaan Model</div>
                <div style='font-size:2.2rem;font-weight:700;color:#ffffff;'>{confidence}%</div>
                <div style='font-size:0.68rem;color:#e0e0e0;margin-top:4px;'>{selected_model_name}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            tips_html = "".join([
                f"<li style='margin-bottom:6px;color:#ffffff;font-size:0.85rem;'>{t}</li>"
                for t in info['tips']
            ])
            st.markdown(f"""
            <div style='background:rgba(30,30,30,0.7);border:1px solid rgba(255,255,255,0.15);
            border-radius:10px;padding:16px;'>
                <div style='font-size:0.7rem;color:#ffffff;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px;'>
                    💡 Rekomendasi Tindakan
                </div>
                <ul style='margin:0;padding-left:16px;'>{tips_html}</ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>Probabilitas Semua Kelas</div>", unsafe_allow_html=True)
        classes      = model_to_use.classes_
        sorted_pairs = sorted(zip(proba, classes), reverse=True)
        for p, c in sorted_pairs:
            pct         = round(p * 100, 1)
            bar_color   = "#ffffff" if c == prediction else "#333333"
            label_color = "#ffffff" if c == prediction else "#888888"
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>
                <div style='width:180px;font-size:0.8rem;color:{label_color};flex-shrink:0;'>{c}</div>
                <div style='flex:1;background:rgba(50,50,50,0.5);border-radius:4px;height:10px;'>
                    <div style='width:{pct}%;background:{bar_color};border-radius:4px;height:10px;transition:width .5s;'></div>
                </div>
                <div style='width:44px;text-align:right;font-size:0.8rem;color:{label_color};flex-shrink:0;'>{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style='background:rgba(30,30,30,0.5);border:1.5px dashed rgba(255,255,255,0.3);
        border-radius:14px;padding:48px;text-align:center;'>
            <div style='font-size:3rem;margin-bottom:16px;'>🌱</div>
            <div style='font-size:1.1rem;color:#ffffff;font-weight:600;margin-bottom:8px;'>
                Siap Menganalisis
            </div>
            <div style='font-size:0.88rem;color:#b0b0b0;'>
                Pilih model &amp; masukkan data parameter iklim di panel kiri,<br>
                lalu klik <b style='color:#ffffff;'>Analisis Sekarang</b>.
            </div>
        </div>
        """, unsafe_allow_html=True)


with col_fi:
    FEATURE_LABELS = {
        'Suhu_Maks_C':                'Suhu Maksimal',
        'Total_Curah_Hujan':          'Curah Hujan',
        'Kelembapan_Tanah_Akar':      'Kelembapan Akar',
        'Kelembapan_Udara_%':         'Kelembapan Udara',
    }

    if not active_has_fi:
        ref_model      = model_dt
        ref_model_name = "Decision Tree"

        if ref_model is not None:
            st.markdown(
                f"<div class='section-label'>Kepentingan Fitur (Referensi: {ref_model_name})</div>",
                unsafe_allow_html=True
            )
            st.markdown(f"""
            <div class="knn-info">
                <div style='font-size:0.78rem;color:#e0e0e0;'>
                    ℹ️ <strong>K-Nearest Neighbors</strong> tidak memiliki atribut
                    <em>feature importances</em> secara langsung. Grafik di bawah
                    menampilkan kepentingan fitur dari model <strong>{ref_model_name}</strong>
                    sebagai referensi global.
                </div>
            </div>
            """, unsafe_allow_html=True)
            importances = ref_model.feature_importances_
        else:
            st.markdown("<div class='section-label'>Kepentingan Fitur</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="knn-info">
                <div style='font-size:0.78rem;color:#e0e0e0;'>
                    ℹ️ <strong>K-Nearest Neighbors</strong> tidak memiliki atribut
                    <em>feature importances</em>. Tidak ada model berbasis pohon yang
                    tersedia untuk dijadikan referensi saat ini.
                </div>
            </div>
            """, unsafe_allow_html=True)
            importances = None
    else:
        st.markdown(
            f"<div class='section-label'>Kepentingan Fitur ({selected_model_name})</div>",
            unsafe_allow_html=True
        )
        fi_model    = active_model if active_model is not None else model_dt
        importances = fi_model.feature_importances_ if fi_model is not None else None

    if importances is not None and FEATURES is not None:
        fi_pairs = sorted(zip(importances, FEATURES), reverse=True)
        max_fi   = max(importances)
        for imp, feat in fi_pairs:
            label = FEATURE_LABELS.get(feat, feat)
            pct   = round(imp * 100, 1)
            bar_w = round((imp / max_fi) * 100)
            st.markdown(f"""
            <div class="fi-row">
                <div class="fi-label">{label}</div>
                <div class="fi-bar-bg"><div class="fi-bar" style="width:{bar_w}%;"></div></div>
                <div class="fi-pct">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Input Saat Ini</div>", unsafe_allow_html=True)

    current_inputs = {
        '🌡️ Suhu Maks':       f"{suhu_maks} °C",
        '🌧️ Curah Hujan':    f"{curah_hujan} mm",
        '💧 Kel. Udara':      f"{kel_udara}%",
        '🌱 Kel. Akar':       f"{kel_tanah_akar:.3f}",
    }

    rows_html = "".join([
        f"<tr><td style='color:#b0b0b0;font-size:0.8rem;padding:5px 8px;'>{k}</td>"
        f"<td style='color:#ffffff;font-size:0.8rem;padding:5px 8px;font-weight:500;text-align:right;'>{v}</td></tr>"
        for k, v in current_inputs.items()
    ])

    st.markdown(f"""
    <div style='background:rgba(30,30,30,0.6);border:1px solid rgba(255,255,255,0.15);
    border-radius:10px;overflow:hidden;'>
        <table style='width:100%;border-collapse:collapse;'>
            {rows_html}
        </table>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ──────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center;padding:16px;border-top:1px solid rgba(255,255,255,0.1);margin-top:16px;'>
    <p style='color:#888888;font-size:0.75rem;letter-spacing:0.04em;'>
        🌾 Smart Rice Guard v3.0 · Model Aktif: <span style='color:#ffffff;font-weight:600;'>{selected_model_name}</span>
        · DT {acc_dt}% | KNN {acc_knn}% ·
        <span style='color:#e0e0e0;'>Sistem Deteksi Penyakit Padi</span>
    </p>
</div>
""", unsafe_allow_html=True)
