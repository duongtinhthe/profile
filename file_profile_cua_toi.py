import base64
import json
import os
import streamlit as st

# Setup thư mục lưu trữ file upload thực tế
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

DATA_NOTES_FILE = "data_notes.txt"
SOCIAL_LINKS_FILE = "social_links.json"

st.set_page_config(
    page_title="Trang Cá Nhân & Quản Lý Dữ Liệu", page_icon="🎵", layout="centered"
)

# -------------------------------------------------------------------
# 1. KHỞI TẠO BỘ NHỚ TẠM (SESSION STATE)
# -------------------------------------------------------------------
if "uploaded_file_info" not in st.session_state:
    st.session_state["uploaded_file_info"] = None

if "notes" not in st.session_state:
    if os.path.exists(DATA_NOTES_FILE):
        with open(DATA_NOTES_FILE, "r", encoding="utf-8") as f:
            st.session_state["notes"] = f.read()
    else:
        st.session_state["notes"] = ""

if "social_links" not in st.session_state:
    if os.path.exists(SOCIAL_LINKS_FILE):
        with open(SOCIAL_LINKS_FILE, "r", encoding="utf-8") as f:
            st.session_state["social_links"] = json.load(f)
    else:
        st.session_state["social_links"] = {
            "Facebook": "https://facebook.com",
            "Discord": "https://discord.com",
            "YouTube": "https://youtube.com",
        }

st.title("📌 Trang Profile & Quản Lý File")

# -------------------------------------------------------------------
# 2. XỬ LÝ UPLOAD FILE (KHÔNG MẤT DỮ LIỆU KHI BẤM LINK)
# -------------------------------------------------------------------
st.subheader("📤 Tải lên Tệp / Nhạc nền / Ảnh")

uploaded_file = st.file_uploader(
    "Chọn file để tải lên (Ảnh, Nhạc MP3, Tài liệu...)",
    type=["png", "jpg", "mp3", "txt", "pdf", "docx"],
)

if uploaded_file is not None:
    save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state["uploaded_file_info"] = {
        "name": uploaded_file.name,
        "path": save_path,
        "size": uploaded_file.size,
    }
    st.success(f"Dữ liệu đã được lưu an toàn: **{uploaded_file.name}**")

# Hiển thị thông tin file đã upload
if st.session_state["uploaded_file_info"] is not None:
    file_data = st.session_state["uploaded_file_info"]
    st.info(
        f"📄 **File đang lưu trong phiên:** `{file_data['name']}` ({file_data['size']} bytes)"
    )

    if st.button("🗑️ Xóa file upload hiện tại"):
        if os.path.exists(file_data["path"]):
            os.remove(file_data["path"])
        st.session_state["uploaded_file_info"] = None
        st.rerun()

st.divider()

# -------------------------------------------------------------------
# 3. MỤC GHI CHÚ (LƯU VÀO DATA_NOTES.TXT)
# -------------------------------------------------------------------
st.subheader("📝 Ghi Chú Cá Nhân")
user_notes = st.text_area(
    "Nội dung ghi chú:", value=st.session_state["notes"], height=120
)

if st.button("💾 Lưu Ghi Chú"):
    st.session_state["notes"] = user_notes
    with open(DATA_NOTES_FILE, "w", encoding="utf-8") as f:
        f.write(user_notes)
    st.success("Đã lưu ghi chú vào `data_notes.txt`!")

st.divider()

# -------------------------------------------------------------------
# 4. DANH SÁCH LINK MẠNG XÃ HỘI (AN TOÀN - MỞ TAB MỚI)
# -------------------------------------------------------------------
st.subheader("🌐 Liên Kết Mạng Xã Hội")

cols = st.columns(len(st.session_state["social_links"]))

for idx, (platform, url) in enumerate(st.session_state["social_links"].items()):
    with cols[idx]:
        html_link = f"""
        <a href="{url}" target="_blank" style="
            display: inline-block;
            width: 100%;
            padding: 10px 0px;
            text-align: center;
            background-color: #262730;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            border: 1px solid #464b5d;
        ">🔗 {platform}</a>
        """
        st.markdown(html_link, unsafe_allow_html=True)

st.caption("⚡ *Các liên kết đều tự động mở tab mới để giữ toàn bộ dữ liệu file & ghi chú của bạn không bị mất.*")

# -------------------------------------------------------------------
# 5. NÚT PAUSE/PLAY NHẠC NỀN CỐ ĐỊNH Ở GÓC DƯỚI BÊN PHẢI (FLOATING BUTTON)
# -------------------------------------------------------------------
# Nếu có file MP3 đã upload, tự động lấy làm nhạc nền, nếu không dùng file mp3 mặc định
audio_src = ""
if (
    st.session_state["uploaded_file_info"]
    and st.session_state["uploaded_file_info"]["name"].lower().endswith(".mp3")
):
    bg_music_path = st.session_state["uploaded_file_info"]["path"]
    with open(bg_music_path, "rb") as f:
        audio_bytes = f.read()
        audio_src = f"data:audio/mp3;base64,{base64.b64encode(audio_bytes).decode()}"
elif os.path.exists("bg_music.mp3"):
    with open("bg_music.mp3", "rb") as f:
        audio_bytes = f.read()
        audio_src = f"data:audio/mp3;base64,{base64.b64encode(audio_bytes).decode()}"

if audio_src:
    player_html = f"""
    <audio id="bg-audio" loop autoplay src="{audio_src}"></audio>

    <button id="music-toggle-btn" onclick="toggleAudio()" style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background-color: #ff4b4b;
        color: white;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        font-size: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.2s, background-color 0.2s;
    ">⏸️</button>

    <script>
    function toggleAudio() {{
        var audio = document.getElementById("bg-audio");
        var btn = document.getElementById("music-toggle-btn");
        if (audio.paused) {{
            audio.play();
            btn.innerHTML = "⏸️";
            btn.style.backgroundColor = "#ff4b4b";
        }} else {{
            audio.pause();
            btn.innerHTML = "▶️";
            btn.style.backgroundColor = "#0e1117";
        }}
    }}
    </script>
    """
    st.components.v1.html(player_html, height=0)
