import streamlit as st
import pandas as pd
import random

# ---------- STYLE ----------
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}
.card {
    background: white;
    padding: 15px;
    border-radius: 11px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    text-align: center;
}
.price {
    font-size: 14px;
    font-weight: bold;
    color: black;
}
.promo {
    color: red;
    font-size: 16px;
    font-weight: bold;
}
.old-price {
    text-decoration: line-through;
    color: gray;
}
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA ----------
if "produk_data" not in st.session_state:
    st.session_state.produk_data = pd.DataFrame({
        "Nama": ["Nugget", "Sosis", "Dimsum"],
        "Harga": [25000, 18000, 22000],
        "Promo": [20000, None, None]
    })

# ---------- AUTH ----------
USER_CREDENTIALS = {"admin": "12345"}

if "login" not in st.session_state:
    st.session_state.login = False

if "page" not in st.session_state:
    st.session_state.page = "konsumen"

# ---------- SIMULASI SUHU ----------
def read_temperature():
    return round(random.uniform(-25, -5), 2)

# ---------- LOGIN ----------
def login_page():
    st.markdown("<h2 style='text-align:center;'>🔐 Login Admin</h2>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.login = True
            st.session_state.page = "admin"
        else:
            st.error("Salah login")

    if st.button("Kembali"):
        st.session_state.page = "konsumen"

# ---------- ADMIN ----------
def admin_dashboard():
    st.sidebar.title("📊 Menu Admin")
    menu = st.sidebar.radio("Menu", ["Dashboard", "Monitoring Suhu", "Manajemen Harga"])

    st.title("👨‍💼 Admin Dashboard")

    if menu == "Dashboard":
        col1, col2 = st.columns(2)
        col1.metric("Total Produk", len(st.session_state.produk_data))
        col2.metric("Promo Aktif", st.session_state.produk_data['Promo'].count())

    elif menu == "Monitoring Suhu":
        temp = read_temperature()
        st.metric("Suhu Freezer", f"{temp} °C")

        if temp > -10:
            st.error("⚠️ Suhu terlalu tinggi!")
        else:
            st.success("✅ Suhu normal")

    elif menu == "Manajemen Harga":
        df = st.session_state.produk_data

        produk = st.selectbox("Pilih Produk", df["Nama"])
        idx = df[df["Nama"] == produk].index[0]

        harga = st.number_input("Harga", value=int(df.loc[idx, "Harga"]))
        promo = st.number_input("Promo (0 jika tidak ada)", value=int(df.loc[idx, "Promo"] or 0))

        if st.button("Simpan"):
            df.loc[idx, "Harga"] = harga
            df.loc[idx, "Promo"] = promo if promo != 0 else None
            st.success("Update berhasil")

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.session_state.page = "konsumen"

# ---------- KONSUMEN ----------
def customer_display():

    temp = read_temperature()

    # HEADER + LOGO
    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/869/869869.png", width=50)

    with col2:
        st.markdown("<h2>FROZEN MART</h2>", unsafe_allow_html=True)

    with col3:
        if st.button("🔐 Admin"):
            st.session_state.page = "login"

    # SUHU
    st.markdown(f"""
    <div style='text-align:right; font-size:18px;'>
    🌡️ Suhu Freezer: <b>{temp} °C</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>🛒 DAFTAR HARGA PRODUK</h1>", unsafe_allow_html=True)

    df = st.session_state.produk_data
    cols = st.columns(3)

    for i, row in df.iterrows():
        with cols[i % 3]:
            if pd.notna(row["Promo"]):
                st.markdown(f"""
                <div class="card">
                    <h3>{row['Nama']}</h3>
                    <p class="old-price">Rp {row['Harga']:,}</p>
                    <p class="promo">Rp {int(row['Promo']):,}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="card">
                    <h3>{row['Nama']}</h3>
                    <p class="price">Rp {row['Harga']:,}</p>
                </div>
                """, unsafe_allow_html=True)

# ---------- MAIN ----------
if st.session_state.page == "konsumen":
    customer_display()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "admin":
    if st.session_state.login:
        admin_dashboard()
    else:
        st.session_state.page = "login"
        login_page()
