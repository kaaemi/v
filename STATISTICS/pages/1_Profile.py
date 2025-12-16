# pages/1_Profile.py
import streamlit as st

# ===============================
# I. KONFIGURASI BAHASA & DATA
# ===============================

# Pastikan LANG dan MEMBERS_DATA sudah dimuat dari session state (oleh Data Analysis.py)
if 'LANG' not in st.session_state or 'MEMBERS_DATA' not in st.session_state:
    st.warning("Silakan kembali ke halaman 'Data Analysis' terlebih dahulu untuk menginisialisasi pengaturan bahasa.")
    st.stop()
    
LANG = st.session_state['LANG']
MEMBERS_DATA = st.session_state['MEMBERS_DATA']

# --- Language Selection (Sidebar) ---
if 'lang_key' not in st.session_state:
    st.session_state['lang_key'] = 'INDONESIA' # Default
    
st.session_state['lang_key'] = st.sidebar.selectbox(
    LANG['INDONESIA']['language_select'], 
    list(LANG.keys()), 
    index=list(LANG.keys()).index(st.session_state['lang_key']),
    format_func=lambda x: x.capitalize()
)

# Ambil kamus bahasa yang dipilih (L)
L = LANG[st.session_state['lang_key']]

# ===============================
# II. TAMPILAN PROFILE
# ===============================

st.set_page_config(page_title=L["profile_title"], layout="wide")


# Apply Custom CSS for Profile Page
st.markdown("""
<style>
/* Background dan Card Styling */
.profile-card {padding: 20px; border-radius: 18px; box-shadow: 0px 8px 20px rgba(0,0,0,0.08); margin-bottom: 25px;}
.working-card {background: #e0f2fe;} 
.not-working-card {background: #fce7f3;} 
.role {font-weight: bold; color: #2563eb;} 
.not-working {color: #dc2626; font-weight: bold;}

/* Styling Gambar Profil: TARGET SEMUA GAMBAR UNTUK ROUNDED STYLE */
img {
    border-radius: 50%;
    border: 3px solid #93c5fd; 
    object-fit: cover;
}
/* PERUBAHAN H1 UNTUK JUDUL UTAMA (Besar, Tebal, Tengah) */
h1 {color: #7c3aed; text-align: center; font-weight: 800; margin-bottom: 30px; font-size: 2.5rem;}
h2 {color: #7c3aed; font-weight: 700;}
.profile-info {line-height: 1.8;}
.explanation-content {padding-left: 20px; padding-bottom: 15px;}
</style>
""", unsafe_allow_html=True)


# PERUBAHAN #1: Mengubah Judul Utama: Emotikon menjadi SATU (👥)
st.markdown(f"<h1>{L['profile_title']}</h1>", unsafe_allow_html=True)
st.markdown("---")

# PERUBAHAN #2: MENGHAPUS SUBHEADER INI:
# st.subheader(L["profile_title"])

# --- LOOPING UNTUK MENAMPILKAN PROFIL ---
for member in MEMBERS_DATA:
    card_class = "working-card" if member["status"] == "active" else "not-working-card"
    
    # Ambil terjemahan peran/status dari kamus bahasa
    display_role_status = L[member["role_key"]]
    
    # Tentukan HTML untuk baris peran/status
    if member["status"] == "active":
        role_html = f'<span class="role">{L["role_label"]}: {display_role_status}</span>'
    else:
        role_html = f'<span class="not-working">{L["status_label"]}: {display_role_status}</span>'

    col_img, col_info = st.columns([1, 4]) # Lebar kolom data diperluas sedikit

    with col_img:
        if member["status"] == "active" and 'image' in member:
            try:
                # Lebar gambar: 150 (sesuai permintaan sebelumnya)
                image_path = member.get("image", "assets/default.jpg") 
                st.image(image_path, width=150)
            except:
                 st.markdown(f"*(Image path not valid for {member['name']})*")


        with col_info:
            st.markdown(f"""
            <div class="profile-card {card_class}">
                <div class="profile-info">
                    <b>{L["name_label"]}:</b> {member["name"]}<br>
                    <b>{L["sid_label"]}:</b> {member["sid"]}<br>
                    {role_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")

# =========================
# PENJELASAN METODOLOGI STATISTIK
# =========================

st.markdown("---") 

st.markdown(f"""
<div class="profile-card working-card"> 
    <h3>{L['explanation_title']}</h3>
    <div class="explanation-content">
        {L['explanation_content']}
    </div>
</div>
""", unsafe_allow_html=True)