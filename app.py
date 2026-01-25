import streamlit as st
import os, json, uuid, shutil
from datetime import datetime

from auth import login_user, register_user
from modules.file_splitter import split_file
from modules.encryption import encrypt_data
from modules.erasure_coding import encode_chunk
from modules.storage_manager import store_chunks, load_chunks
from modules.file_reconstructor import reconstruct
from modules.integrity import generate_hash
from config import KEY

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Secure Cloud Console",
    page_icon="☁️",
    layout="wide"
)

# -------------------------------------------------
# ENTERPRISE CLOUD CSS
# -------------------------------------------------
st.markdown("""
<style>
body {
    background-color:#0e1117;
}
.title {
    font-size:40px;
    font-weight:800;
}
.subtitle {
    color:#9ca3af;
}
.card {
    background:#161b22;
    padding:20px;
    border-radius:14px;
    border:1px solid #30363d;
}
.badge {
    background:#1f6feb;
    padding:4px 10px;
    border-radius:12px;
    font-size:12px;
}
.table-header {
    color:#9ca3af;
    font-size:13px;
}
.file-row {
    border-bottom:1px solid #30363d;
    padding:10px 0;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "uploaded_once" not in st.session_state:
    st.session_state.uploaded_once = False
if "selected_files" not in st.session_state:
    st.session_state.selected_files = set()

# -------------------------------------------------
# LOGIN
# -------------------------------------------------
if not st.session_state.user:
    st.markdown("<div class='title'>☁️ Secure Cloud Console</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Enterprise-grade encrypted cloud storage</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if login_user(u, p):
                st.session_state.user = u
                st.session_state.uploaded_once = False
                st.session_state.selected_files = set()
                st.rerun()
            else:
                st.warning("Invalid credentials")

    with tab2:
        u = st.text_input("New Username")
        p = st.text_input("New Password", type="password")
        if st.button("Create Account", use_container_width=True):
            if register_user(u, p):
                st.success("Account created. Login now.")
            else:
                st.warning("Username already exists")
    st.stop()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.markdown("## ☁️ Secure Cloud")
st.sidebar.markdown(f"👤 **{st.session_state.user}**")
st.sidebar.markdown("<span class='badge'>ACTIVE</span>", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Upload Files", "My Files"]
)

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

# -------------------------------------------------
# USER ROOT
# -------------------------------------------------
USER_ROOT = f"user_files/{st.session_state.user}"
os.makedirs(USER_ROOT, exist_ok=True)

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
if menu == "Dashboard":
    st.markdown("<div class='title'>📊 Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>System security overview</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='card'>🔐 Encryption<br><b>AES-256</b></div>", unsafe_allow_html=True)
    c2.markdown("<div class='card'>🧬 Integrity<br><b>SHA-256</b></div>", unsafe_allow_html=True)
    c3.markdown("<div class='card'>☁️ Storage<br><b>Distributed Nodes</b></div>", unsafe_allow_html=True)

# -------------------------------------------------
# UPLOAD
# -------------------------------------------------
elif menu == "Upload Files":
    st.markdown("<div class='title'>⬆ Upload Files</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Encrypt and store securely</div>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Choose a file")

    if uploaded and not st.session_state.uploaded_once:
        st.session_state.uploaded_once = True

        file_id = str(uuid.uuid4())
        base = f"{USER_ROOT}/{file_id}"
        os.makedirs(base, exist_ok=True)

        data = uploaded.read()
        chunks = split_file(data)

        encrypted_chunks = []
        encrypted_full = b''

        for c in chunks:
            enc = encrypt_data(c, KEY)
            encrypted_full += enc
            encrypted_chunks.append(encode_chunk(enc))

        store_chunks(base, encrypted_chunks)

        with open(f"{base}/encrypted.bin", "wb") as f:
            f.write(encrypted_full)

        with open(f"{base}/file_hash.txt", "w") as f:
            f.write(generate_hash(data))

        with open(f"{base}/metadata.json", "w") as f:
            json.dump({
                "filename": uploaded.name,
                "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }, f)

        st.success("File uploaded and encrypted successfully")
        st.rerun()

    if uploaded is None:
        st.session_state.uploaded_once = False

# -------------------------------------------------
# MY FILES
# -------------------------------------------------
elif menu == "My Files":
    st.markdown("<div class='title'>📂 My Files</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Your encrypted cloud storage</div>", unsafe_allow_html=True)

    files_meta = []
    for fid in os.listdir(USER_ROOT):
        meta_path = f"{USER_ROOT}/{fid}/metadata.json"
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
                meta["id"] = fid
                files_meta.append(meta)

    if not files_meta:
        st.info("No files uploaded yet.")
    else:
        # Table header
        h1, h2, h3 = st.columns([1, 5, 3])
        h1.markdown("<div class='table-header'>Select</div>", unsafe_allow_html=True)
        h2.markdown("<div class='table-header'>File Name</div>", unsafe_allow_html=True)
        h3.markdown("<div class='table-header'>Uploaded At</div>", unsafe_allow_html=True)

        for f in files_meta:
            fid = f["id"]
            c1, c2, c3 = st.columns([1, 5, 3])

            checked = c1.checkbox("", key=f"chk_{fid}", value=fid in st.session_state.selected_files)
            if checked:
                st.session_state.selected_files.add(fid)
            else:
                st.session_state.selected_files.discard(fid)

            c2.markdown(f"<div class='file-row'>📄 {f['filename']}</div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='file-row'>{f['uploaded_at']}</div>", unsafe_allow_html=True)

        st.divider()

        if st.session_state.selected_files:
            st.subheader("⬇ Download Selected")

            for fid in st.session_state.selected_files:
                base = f"{USER_ROOT}/{fid}"

                with open(f"{base}/metadata.json") as f:
                    meta = json.load(f)

                recovered = reconstruct(load_chunks(base))
                encrypted_data = open(f"{base}/encrypted.bin", "rb").read()

                col1, col2 = st.columns(2)
                col1.download_button(
                    f"⬇ Original – {meta['filename']}",
                    recovered,
                    file_name=meta["filename"],
                    key=f"orig_{fid}"
                )
                col2.download_button(
                    f"🔐 Encrypted – {meta['filename']}.bin",
                    encrypted_data,
                    file_name=f"{meta['filename']}.bin",
                    key=f"enc_{fid}"
                )

            if st.button("🗑 Delete Selected Files"):
                for fid in st.session_state.selected_files:
                    shutil.rmtree(f"{USER_ROOT}/{fid}", ignore_errors=True)
                st.session_state.selected_files = set()
                st.success("Selected files deleted")
                st.rerun()
