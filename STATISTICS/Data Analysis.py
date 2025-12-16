# main_app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ===============================
# I. KONFIGURASI BAHASA & DATA ANGGOTA
# ===============================

# --- Data Anggota Kelompok (Hanya disimpan di sini, akan diimpor oleh Profile.py) ---
MEMBERS_DATA = [
    {
        "name": "Muhammad Dicky Ramadhan",
        "sid": "004202400011",
        "role_key": "role_dicky",  # Ketua Kelompok Statistik 1
        "status": "active",
        "image": "assets/dicky.jpg" 
    },
    {
        "name": "Kenrick Sierra Kisworo",
        "sid": "004202400070",
        "role_key": "role_kenrick", # Ketua Kelompok Aljabar Linear
        "status": "active",
        "image": "assets/kenrick.jpg" 
    },
]

# --- Kamus Bahasa (Multilanguage Support) ---
LANG = {
    "INDONESIA": {
        "title": "Analisis Data Survey",
        "sidebar_title": "Konfigurasi Analisis",
        "upload": "1. Unggah Dataset (CSV/Excel) - Data Harus Berupa Angka!",
        "members": "Dibuat oleh: Dicky dan Kenrick",
        "language_select": "Pilih Bahasa",
        
        # Profile Labels
        "profile_title": "👥 Profil Pengembang", 
        "name_label": "Nama",
        "sid_label": "NIM",
        "role_label": "Peran",
        "status_label": "Status",
        
        # Profile Roles (MATCHES user's template)
        "role_kenrick": "Ketua Kelompok Aljabar Linear",
        "role_dicky": "Ketua Kelompok Statistik 1",
        "not_working_status": "Tidak Bekerja",
        
        # Section Headers
        "sec_demo": "A. Analisis Demografi / Kategorikal (Tabel Frekuensi)",
        "sec_desc": "B. Statistik Deskriptif (Numerik)",
        "sec_composite": "C. Konstruksi Variabel (Skor Komposit)",
        "sec_assump": "D. Uji Asumsi (Normalitas)",
        "sec_assoc": "E. Analisis Asosiasi (Uji Hipotesis)",
        
        # Widgets & Labels
        "sel_demo": "Pilih Variabel Demografi (cth: Gender, Status)",
        "sel_items_x": "Pilih Item untuk Variabel X",
        "sel_items_y": "Pilih Item untuk Variabel Y",
        "freq_table": "Tabel Frekuensi & Persentase",
        "desc_table": "Tabel Statistik Deskriptif",
        
        "desc_select_label": "Pilih Item yang Akan Dideskripsikan",
        "comp_note": "Skor komposit dibuat berdasarkan nilai Rata-Rata (Mean) dari item yang Anda pilih.",
        "comp_success": "Variabel Komposit berhasil dibuat",
        "txt_from": "dari",
        "txt_item": "item",
        "res_strength": "Kekuatan Hubungan",
        "res_sig": "Signifikansi",
        
        # STATUS DATA BARU
        "status_normal": "Normal",
        "status_not_normal": "Tidak Normal",
        "status_data_err": "Tidak Cukup Data/Varian Nol",
        
        # LABEL SCATTERPLOT BARU
        "scatter_x_label": "Variabel X (Skor Rata-Rata)",
        "scatter_y_label": "Variabel Y (Skor Rata-Rata)",
        # -------------------------------------------

        "method": "Metode Korelasi", # Tetap ada untuk Judul
        "interpret": "Interpretasi",
        "result": "Hasil Analisis",
        "scatter": "Visualisasi Scatterplot",
        "normality_note": "Uji Shapiro-Wilk: Jika p > 0.05, data berdistribusi Normal.",
        "upload_instruction_status": "Silakan unggah file CSV atau Excel",
        
        # Data/File Handling Labels
        "data_loaded": "Data dimuat:", 
        "respondents": "responden", 
        "columns": "kolom", 
        "preview_data": "Preview Data", 
        "view_all_data": "Lihat Semua Data Responden (Layar Penuh)", 
        "full_screen_note": "Saat mode layar penuh (ikon di kanan atas tabel) diaktifkan, seluruh data akan ditampilkan tanpa *scrolling* internal.", 
        "error_processing": "Error memproses file atau kolom data. Pastikan semua kolom X dan Y sudah diubah menjadi angka murni (1, 2, 3, dst.) sebelum diunggah. Detail Error:", 
        
        # Interpretations
        "weak": "Korelasi Lemah",
        "moderate": "Korelasi Sedang",
        "strong": "Korelasi Kuat",
        "sig": "Signifikan (p < 0.05)",
        "not_sig": "Tidak Signifikan (p ≥ 0.05)",
        
        # NEW LABEL
        "corr_method_auto": "Metode Korelasi yang Dipilih Otomatis",

        # Metodologi Text
        "explanation_title": "💡 Metodologi Analisis Statistik 1",
        "explanation_content": """
* **Uji Normalitas:** Digunakan Uji Shapiro-Wilk untuk menentukan distribusi data X\_Score dan Y\_Score. Hasil ini krusial untuk memilih metode korelasi yang tepat.
* **Korelasi Pearson:** Digunakan jika **kedua** variabel terdistribusi Normal. Mengukur hubungan linear antara dua variabel interval/rasio.
* **Korelasi Spearman:** Digunakan jika **salah satu atau kedua** variabel tidak Normal. Mengukur hubungan monotonik (derajat seiring/berlawanan) antara dua variabel ordinal.
* **Skor Komposit:** Variabel X dan Y dibentuk dari rata-rata (mean) item penyusunnya (misalnya, X\_Score = avg(X1, X2)).
        """,
    },
    "ENGLISH": {
        "title": "Survey Data Analysis",
        "sidebar_title": "Analysis Configuration",
        "upload": "1. Upload Dataset (CSV/Excel) - Data Must Be Numeric!",
        "members": "Created by: Dicky and Kenrick",
        "language_select": "Select Language",

        # Profile Labels
        "profile_title": "👥 Developer Profile", 
        "name_label": "Name",
        "sid_label": "SID",
        "role_label": "Role",
        "status_label": "Status",

        # Profile Roles (MATCHES user's template)
        "role_kenrick": "Lead Group of Linear Algebra",
        "role_dicky": "Lead Group of Statistics 1",
        "not_working_status": "Not Working",

        # Section Headers
        "sec_demo": "A. Demographic / Categorical Analysis (Frequency Tables)",
        "sec_desc": "B. Descriptive Statistics (Numeric)",
        "sec_composite": "C. Variable Construction (Composite Score)",
        "sec_assump": "D. Assumption Test (Normality)",
        "sec_assoc": "E. Association Analysis (Hypothesis Testing)",

        # Widgets & Labels
        "sel_demo": "Select Demographic Variable (e.g.: Gender, Status)",
        "sel_items_x": "Select Items for Variable X",
        "sel_items_y": "Select Items for Variable Y",
        "freq_table": "Frequency & Percentage Table",
        "desc_table": "Descriptive Statistics Table",

        "desc_select_label": "Select Items to Describe",
        "comp_note": "Composite scores are created based on the Mean value of the items you selected.",
        "comp_success": "Composite Variables successfully created",
        "txt_from": "from",
        "txt_item": "items",
        "res_strength": "Correlation Strength",
        "res_sig": "Significance",

        # STATUS DATA BARU
        "status_normal": "Normal",
        "status_not_normal": "Not Normal",
        "status_data_err": "Insufficient Data/Zero Variance",
        
        # LABEL SCATTERPLOT BARU
        "scatter_x_label": "Variable X (Mean Score)",
        "scatter_y_label": "Variable Y (Mean Score)",
        # -----------------------------------------------------

        "method": "Correlation Method",
        "interpret": "Interpretation",
        "result": "Analysis Results",
        "scatter": "Scatterplot Visualization",
        "normality_note": "Shapiro-Wilk Test: If p > 0.05, data is Normally distributed.",
        "upload_instruction_status": "Please upload a CSV or Excel file",
        
        # Data/File Handling Labels
        "data_loaded": "Data loaded:",
        "respondents": "respondents",
        "columns": "columns",
        "preview_data": "Data Preview",
        "view_all_data": "View All Respondent Data (Full Screen)",
        "full_screen_note": "When full screen mode (icon on the top right of the table) is activated, all data will be displayed without internal scrolling.",
        "error_processing": "Error processing file or data columns. Ensure all X and Y columns are converted to pure numeric values (1, 2, 3, etc.) before uploading. Error Detail:",
        
        # Interpretations
        "weak": "Weak Correlation",
        "moderate": "Moderate Correlation",
        "strong": "Strong Correlation",
        "sig": "Significant (p < 0.05)",
        "not_sig": "Not Significant (p ≥ 0.05)",
        
        # NEW LABEL
        "corr_method_auto": "Automatically Selected Correlation Method",

        # Metodologi Text
        "explanation_title": "💡 Statistics 1 Methodology",
        "explanation_content": """
* **Normality Test:** Shapiro-Wilk Test is used to determine the distribution of X\_Score and Y\_Score. This result is crucial for selecting the appropriate correlation method.
* **Pearson Correlation:** Used if **both** variables are Normally distributed. Measures the linear relationship between two interval/ratio variables.
* **Spearman Correlation:** Used if **one or both** variables are Not Normally distributed. Measures the monotonic relationship (concordance) between two ordinal variables.
* **Composite Score:** Variables X and Y are formed from the mean of their constituent items (e.g., X\_Score = avg(X1, X2)).
        """,
    }
}

# Simpan LANG dan MEMBERS_DATA di session state agar bisa diakses pages
st.session_state['LANG'] = LANG
st.session_state['MEMBERS_DATA'] = MEMBERS_DATA

# ===============================
# II. HELPER FUNCTIONS
# ===============================

def get_descriptive_stats(series):
    """Calculate basic descriptive stats required by the assignment."""
    return {
        "Mean": series.mean(),
        "Median": series.median(),
        "Mode": series.mode().iloc[0] if not series.mode().empty else np.nan,
        "Min": series.min(),
        "Max": series.max(),
        "Std Dev": series.std()
    }

def get_frequency_table(df, col):
    """Generate Frequency and Percentage table."""
    freq = df[col].value_counts()
    perc = df[col].value_counts(normalize=True) * 100
    table = pd.DataFrame({"Frequency": freq, "Percentage (%)": perc})
    return table.sort_index()

def interpret_r(r, lang_dict):
    """Interpret the strength of correlation."""
    abs_r = abs(r)
    if abs_r < 0.3:
        strength = lang_dict["weak"]
    elif abs_r < 0.7:
        strength = lang_dict["moderate"]
    else:
        strength = lang_dict["strong"]
    
    direction = "(+)" if r > 0 else "(-)"
    return f"{strength} {direction}"

def check_normality(series):
    """Perform Shapiro-Wilk test for normality."""
    clean_data = series.dropna()
    if len(clean_data) < 3 or np.std(clean_data) == 0: 
        return np.nan, np.nan
    stat, p = stats.shapiro(clean_data)
    return stat, p

# ===============================
# III. MAIN APP EXECUTION
# ===============================

st.set_page_config(page_title="Survey Analysis App", layout="wide")

# --- Language Selection (Sidebar) ---
if 'lang_key' not in st.session_state:
    st.session_state['lang_key'] = 'INDONESIA'

st.session_state['lang_key'] = st.sidebar.selectbox(
    LANG['INDONESIA']['language_select'], 
    list(LANG.keys()), 
    index=list(LANG.keys()).index(st.session_state['lang_key']),
    format_func=lambda x: x.capitalize()
)

L = LANG[st.session_state['lang_key']]

# Apply Custom CSS for main page
st.markdown("""
<style>
/* Styling Gambar Profil: TARGET SEMUA GAMBAR UNTUK ROUNDED STYLE */
img {
    border-radius: 50%;
    border: 3px solid #93c5fd; 
    object-fit: cover;
}
h1 {color: #7c3aed; text-align: center; font-weight: 800; margin-bottom: 30px;}
</style>
""", unsafe_allow_html=True)


st.title(L["title"])
st.info(L["members"])

# --- STEP 1: UPLOAD DATA ---
st.header(L["upload"])
uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

if uploaded_file:
    # Load Data
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        df.columns = df.columns.str.strip() 

        st.success(f"{L['data_loaded']} {df.shape[0]} {L['respondents']}, {df.shape[1]} {L['columns']}")
        
        with st.expander(L["preview_data"]):
            
            # Tampilkan 5 baris pertama dengan tinggi terbatas
            st.dataframe(
                df.head(), 
                height=180, 
                use_container_width=True
            )
            
            st.markdown("---")
            with st.expander(L["view_all_data"]):
                st.info(L["full_screen_note"])
                st.dataframe(
                    df, 
                    height=500, 
                    use_container_width=True
                )
            
        df_num = df.select_dtypes(include=[np.number])
        df_cat = df.select_dtypes(exclude=[np.number])
        all_cols = df.columns.tolist()

        # --- STEP 2: DEMOGRAPHICS (FREQUENCY TABLES) ---
        st.markdown("---")
        st.header(L["sec_demo"])
        
        demo_cols = st.multiselect(L["sel_demo"], all_cols, default=df_cat.columns.tolist()[:2])
        
        if demo_cols:
            col1, col2 = st.columns(2)
            for i, col in enumerate(demo_cols):
                with (col1 if i % 2 == 0 else col2):
                    st.subheader(f"Variabel: {col}")
                    try:
                        ftable = get_frequency_table(df, col)
                        st.dataframe(ftable.style.format({"Percentage (%)": "{:.2f}"}))
                        st.bar_chart(ftable["Frequency"])
                    except Exception as e:
                        st.warning(f"Tidak dapat membuat tabel frekuensi untuk kolom '{col}'.")

        # --- STEP 3: DESCRIPTIVE STATISTICS (NUMERIC) ---
        st.markdown("---")
        st.header(L["sec_desc"])
        
        valid_num_cols = [col for col in df_num.columns if df_num[col].nunique() > 1]
        
        numeric_cols_selected = st.multiselect(L["desc_select_label"], valid_num_cols, default=valid_num_cols)
        
        if numeric_cols_selected:
            desc_list = []
            for col in numeric_cols_selected:
                stats_res = get_descriptive_stats(df_num[col])
                stats_res["Variable"] = col
                desc_list.append(stats_res)
            
            desc_df = pd.DataFrame(desc_list).set_index("Variable")
            st.dataframe(desc_df.style.format("{:.3f}"))

        # --- STEP 4: COMPOSITE VARIABLES (X and Y) ---
        st.markdown("---")
        st.header(L["sec_composite"])
        
        st.write(L["comp_note"])
        
        c1, c2 = st.columns(2)
        with c1:
            default_x = [col for col in valid_num_cols if col.upper().startswith('X')]
            x_items = st.multiselect(L["sel_items_x"], valid_num_cols, default=default_x)
        with c2:
            default_y = [col for col in valid_num_cols if col.upper().startswith('Y')]
            y_items = st.multiselect(L["sel_items_y"], valid_num_cols, default=default_y)
            
        if x_items and y_items:
            df["X_Score"] = df[x_items].mean(axis=1)
            df["Y_Score"] = df[y_items].mean(axis=1)
            
            st.success(f"{L['comp_success']}: X_Score ({L['txt_from']} {len(x_items)} {L['txt_item']}) & Y_Score ({L['txt_from']} {len(y_items)} {L['txt_item']}).")
            
            # --- STEP 5: ASSUMPTION CHECK (NORMALITAS) ---
            st.markdown("---")
            st.header(L["sec_assump"])
            st.write(L["normality_note"])
            
            shapiro_data = []
            
            # Mendapatkan p-value normalitas X dan Y
            stat_x, p_val_x = check_normality(df["X_Score"])
            stat_y, p_val_y = check_normality(df["Y_Score"])
            
            norm_x = p_val_x > 0.05
            norm_y = p_val_y > 0.05
            
            for var_name, col_name, stat, p_val, is_normal in zip(
                ["Variable X (X_Score)", "Variable Y (Y_Score)"], 
                ["X_Score", "Y_Score"],
                [stat_x, stat_y],
                [p_val_x, p_val_y],
                [norm_x, norm_y]
            ):
                status = ""
                if pd.isna(p_val):
                    status = L["status_data_err"]
                else:
                    status = L["status_normal"] if is_normal else L["status_not_normal"]
                    
                shapiro_data.append({"Variabel": var_name, "Statistic": stat, "p-value": p_val, "Distribusi": status})
            
            st.table(pd.DataFrame(shapiro_data).set_index("Variabel").style.format({"Statistic": "{:.4f}", "p-value": "{:.4f}"}))

            # --- STEP 6: ASSOCIATION ANALYSIS (KORELASI OTOMATIS) ---
            st.markdown("---")
            st.header(L["sec_assoc"])
            
            # LOGIKA OTOMATIS: Pearson hanya jika KEDUA variabel Normal
            if norm_x and norm_y:
                method = "Pearson"
            else:
                method = "Spearman"
                
            st.markdown(f"**{L['corr_method_auto']}:** <span style='color:#7c3aed; font-weight:bold;'>{method}</span>", unsafe_allow_html=True)

            
            clean_xy = df[["X_Score", "Y_Score"]].dropna()
            
            if len(clean_xy) < 2:
                st.error(f"Tidak cukup data ({len(clean_xy)} baris) untuk menghitung korelasi.")
            else:
                if method == "Pearson":
                    corr_coeff, p_val = stats.pearsonr(clean_xy["X_Score"], clean_xy["Y_Score"])
                else:
                    corr_coeff, p_val = stats.spearmanr(clean_xy["X_Score"], clean_xy["Y_Score"])
                
                res_col1, res_col2 = st.columns([1, 2])
                
                with res_col1:
                    st.subheader(L["result"])
                    st.metric(label=f"{method} Correlation (r)", value=f"{corr_coeff:.3f}")
                    st.metric(label="p-value", value=f"{p_val:.4f}")
                    
                    interp_strength = interpret_r(corr_coeff, L)
                    interp_sig = L["sig"] if p_val < 0.05 else L["not_sig"]
                    
                    st.markdown(f"**{L['interpret']}:**")
                    st.info(f"- {L['res_strength']}: {interp_strength}\n- {L['res_sig']}: {interp_sig}")

                with res_col2:
                    st.subheader(L["scatter"])
                    fig, ax = plt.subplots(figsize=(8, 5))
                    # Menggunakan method yang otomatis terpilih untuk judul scatterplot
                    sns.regplot(x="X_Score", y="Y_Score", data=df, ax=ax, color='skyblue', line_kws={"color": "red"})
                    
                    # --- PERBAIKAN: MENGGUNAKAN LABEL SCATTERPLOT DARI L ---
                    ax.set_xlabel(L["scatter_x_label"])
                    ax.set_ylabel(L["scatter_y_label"])
                    # --------------------------------------------------------
                    
                    ax.set_title(f"Scatterplot: X vs Y ({method})")
                    st.pyplot(fig)
                
    except Exception as e:
        st.error(f"{L['error_processing']} {e}")
else:
    st.info(L["upload_instruction_status"])