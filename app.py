import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

# ========================================
# KONFIGURASI HALAMAN
# ========================================
st.set_page_config(
    page_title="Student Social Media & Mental Health Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# CSS KUSTOM
# ========================================
st.markdown("""
<style>
.main-header {
    font-size: 2.4rem;
    font-weight: bold;
    text-align: center;
    color: #2E86C1;
}
</style>
""", unsafe_allow_html=True)

# ========================================
# LOAD DATASET
# ========================================
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "Students Social Media Addiction.csv"
    if not data_path.exists():
        st.error("❌ File dataset tidak ditemukan")
        st.stop()
    return pd.read_csv(data_path)

df = load_data()

# ========================================
# HEADER
# ========================================
st.markdown(
    '<div class="main-header">🎓 Student Social Media & Mental Health Dashboard</div>',
    unsafe_allow_html=True
)
st.markdown(
    "Dashboard analisis dampak penggunaan media sosial terhadap **kesehatan mental mahasiswa** "
    "sebagai bagian dari **SDG 3 – Kehidupan Sehat dan Sejahtera**."
)
st.markdown("---")

# ========================================
# SIDEBAR FILTER
# ========================================
st.sidebar.header("🔍 Filter Data")

gender = st.sidebar.multiselect(
    "Jenis Kelamin",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

platform = st.sidebar.multiselect(
    "Platform Media Sosial yang Paling Sering Digunakan",
    options=df['Most_Used_Platform'].unique(),
    default=df['Most_Used_Platform'].unique()
)

academic = st.sidebar.multiselect(
    "Jenjang Akademik",
    options=df['Academic_Level'].unique(),
    default=df['Academic_Level'].unique()
)

usage_range = st.sidebar.slider(
    "Durasi Penggunaan Harian (Jam)",
    float(df['Avg_Daily_Usage_Hours'].min()),
    float(df['Avg_Daily_Usage_Hours'].max()),
    (
        float(df['Avg_Daily_Usage_Hours'].min()),
        float(df['Avg_Daily_Usage_Hours'].max())
    )
)

# ========================================
# FILTER DATA
# ========================================
filtered_df = df[
    (df['Gender'].isin(gender)) &
    (df['Most_Used_Platform'].isin(platform)) &
    (df['Academic_Level'].isin(academic)) &
    (df['Avg_Daily_Usage_Hours'].between(usage_range[0], usage_range[1]))
]

if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter")
    st.stop()

# ========================================
# KPI
# ========================================
st.header("📊 Ringkasan Statistik Utama")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Jumlah Mahasiswa", len(filtered_df))
c2.metric(
    "Rata-rata Durasi Harian (Jam)",
    round(filtered_df['Avg_Daily_Usage_Hours'].mean(), 2)
)
c3.metric(
    "Rata-rata Skor Kesehatan Mental",
    round(filtered_df['Mental_Health_Score'].mean(), 2),
    f"±{round(filtered_df['Mental_Health_Score'].std(), 2)}"
)
c4.metric(
    "Rata-rata Skor Kecanduan",
    round(filtered_df['Addicted_Score'].mean(), 2),
    f"±{round(filtered_df['Addicted_Score'].std(), 2)}"
)

st.markdown("---")

# ========================================
# TAB
# ========================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📱 Penggunaan Platform",
    "🧠 Kesehatan Mental",
    "😴 Dampak Gaya Hidup",
    "📊 Korelasi Variabel",
    "🎯 Analisis SDG",
    "📋 Data Mahasiswa"
])

# ========================================
# TAB 1
# ========================================
with tab1:
    st.subheader("Distribusi Platform Media Sosial")

    fig = px.pie(
        filtered_df,
        names="Most_Used_Platform",
        hole=0.4,
        title="Platform Media Sosial yang Paling Sering Digunakan"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        filtered_df.groupby('Most_Used_Platform')['Avg_Daily_Usage_Hours']
        .mean()
        .reset_index(),
        x="Most_Used_Platform",
        y="Avg_Daily_Usage_Hours",
        title="Rata-rata Durasi Penggunaan Harian per Platform"
    )
    st.plotly_chart(fig, use_container_width=True)

# ========================================
# TAB 2
# ========================================
with tab2:
    st.subheader("Hubungan Penggunaan Media Sosial dan Kesehatan Mental")

    fig = px.scatter(
        filtered_df,
        x="Avg_Daily_Usage_Hours",
        y="Mental_Health_Score",
        color="Gender",
        color_discrete_map={
            "Male": "#1f77b4",    # Biru
            "Female": "#e84393"  # Pink
        },
        hover_data=["Academic_Level", "Most_Used_Platform"],
        trendline="ols",
        title="Durasi Penggunaan vs Skor Kesehatan Mental"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.box(
        filtered_df,
        x="Affects_Academic_Performance",
        y="Mental_Health_Score",
        color="Affects_Academic_Performance",
        title="Dampak Kesehatan Mental terhadap Performa Akademik"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.box(
        filtered_df,
        x="Academic_Level",
        y="Mental_Health_Score",
        color="Academic_Level",
        title="Skor Kesehatan Mental Berdasarkan Jenjang Akademik"
    )
    st.plotly_chart(fig, use_container_width=True)

# ========================================
# TAB 3
# ========================================
with tab3:
    st.subheader("Dampak Gaya Hidup")

    fig = px.scatter(
        filtered_df,
        x="Sleep_Hours_Per_Night",
        y="Addicted_Score",
        color="Gender",
        color_discrete_map={
            "Male": "#1f77b4",    # Biru
            "Female": "#e84393"  # Pink
        },
        hover_data=["Avg_Daily_Usage_Hours"],
        title="Jam Tidur vs Skor Kecanduan Media Sosial"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(
        filtered_df,
        x="Conflicts_Over_Social_Media",
        title="Konflik yang Terjadi Akibat Media Sosial"
    )
    st.plotly_chart(fig, use_container_width=True)

# ========================================
# TAB 4
# ========================================
with tab4:
    st.subheader("Heatmap Korelasi Variabel")

    corr_cols = [
        'Avg_Daily_Usage_Hours',
        'Mental_Health_Score',
        'Addicted_Score',
        'Sleep_Hours_Per_Night'
    ]

    corr = filtered_df[corr_cols].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="Blues", ax=ax)
    st.pyplot(fig)

# ========================================
# TAB 5 – ANALISIS SDG
# ========================================
with tab5:
    st.subheader("🎯 Analisis Keterkaitan dengan Sustainable Development Goals (SDGs)")

    st.markdown("""
    Dashboard ini mengaitkan **pengaruh penggunaan media sosial terhadap mahasiswa**
    dengan dua tujuan SDGs utama, yaitu **SDG 3 (Good Health and Well-Being)** dan
    **SDG 4 (Quality Education)**.
    """)

    # ==========================
    # SDG 3: GOOD HEALTH
    # ==========================
    st.markdown("## 🔹 SDG 3: Good Health and Well-Being")
    st.markdown("**Target 3.4 – Kesehatan mental dan kesejahteraan**")

    sdg3_mental = filtered_df['Mental_Health_Score'].mean()
    sdg3_addicted = filtered_df['Addicted_Score'].mean()
    sdg3_sleep = filtered_df['Sleep_Hours_Per_Night'].mean()

    c1, c2, c3 = st.columns(3)
    c1.metric("Rata-rata Skor Kesehatan Mental", round(sdg3_mental, 2))
    c2.metric("Rata-rata Skor Kecanduan", round(sdg3_addicted, 2))
    c3.metric("Rata-rata Jam Tidur", round(sdg3_sleep, 2))

    fig = px.scatter(
        filtered_df,
        x="Avg_Daily_Usage_Hours",
        y="Mental_Health_Score",
        trendline="ols",
        title="SDG 3: Durasi Penggunaan Media Sosial vs Kesehatan Mental"
    )
    st.plotly_chart(fig, use_container_width=True)

    if sdg3_mental < 60:
        st.warning("⚠️ Indikasi risiko terhadap kesehatan mental mahasiswa (SDG 3)")
    else:
        st.success("✅ Kondisi kesehatan mental relatif baik (SDG 3)")

    st.markdown("---")

    # ==========================
    # SDG 4: QUALITY EDUCATION
    # ==========================
    st.markdown("## 🔹 SDG 4: Quality Education")
    st.markdown("**Target 4.1 – Hasil pembelajaran yang efektif dan berkualitas**")

    academic_impact = (
        filtered_df['Affects_Academic_Performance']
        .value_counts()
        .reset_index()
    )
    academic_impact.columns = ['Dampak Akademik', 'Jumlah Mahasiswa']

    fig = px.bar(
        academic_impact,
        x="Dampak Akademik",
        y="Jumlah Mahasiswa",
        title="SDG 4: Dampak Media Sosial terhadap Performa Akademik",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

    negative_impact = academic_impact[
        academic_impact['Dampak Akademik'].str.contains("Negative", case=False)
    ]['Jumlah Mahasiswa'].sum()

    if negative_impact > len(filtered_df) * 0.4:
        st.warning("⚠️ Media sosial berpotensi menghambat kualitas pendidikan (SDG 4)")
    else:
        st.success("✅ Dampak media sosial terhadap pendidikan masih terkendali (SDG 4)")

    st.markdown("---")

    # ==========================
    # KESIMPULAN SDG
    # ==========================
    st.markdown("### 📌 Kesimpulan SDG")
    st.markdown("""
    - Penggunaan media sosial yang berlebihan berpotensi **mengganggu kesehatan mental**
      mahasiswa, sehingga memengaruhi pencapaian **SDG 3 Target 3.4**.
    - Dampak terhadap fokus dan performa akademik menunjukkan keterkaitan langsung
      dengan **SDG 4 Target 4.1** mengenai kualitas pendidikan.
    """)

# ========================================
# TAB 6
# ========================================
with tab6:
    st.subheader("Tabel Data Mahasiswa")

    show_cols = [
        'Student_ID', 'Age', 'Gender', 'Academic_Level', 'Country',
        'Avg_Daily_Usage_Hours', 'Mental_Health_Score', 'Addicted_Score'
    ]

    st.dataframe(filtered_df[show_cols], use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Unduh Data Terfilter",
        csv,
        "student_social_media_filtered.csv",
        "text/csv"
    )

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown(
    "<center>📘 Dashboard Analisis Media Sosial & Kesehatan Mental Mahasiswa | Streamlit</center>",
    unsafe_allow_html=True
)
