import base64
import os
import streamlit as st

st.set_page_config(
    page_title="Profile Cá Nhân",
    page_icon="✨",
    layout="centered"
)

# -------------------------------------------------------------------
# 1. TÙY CHỈNH STYLES VÀ GIAO DIỆN PROFILE
# -------------------------------------------------------------------
st.markdown("""
    <style>
    /* Gradient nền và căn giữa profile */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #ffffff;
    }
    
    /* Thiết kế thẻ Profile */
    .profile-card {
        text-align: center;
        padding: 20px;
    }
    
    .avatar-img {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #8b5cf6;
        box-shadow: 0px 8px 20px rgba(139, 92, 246, 0.4);
        margin-bottom: 15px;
    }
    
    .profile-name {
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 5px;
        color: #ffffff;
    }
    
    .profile-bio {
        font-size: 15px;
        color: #cbd5e1;
        margin-bottom: 25px;
    }

    /* Styling nút link mạng xã hội dạng danh sách */
    .social-btn {
        display: block;
        width: 100%;
        padding: 14px 20px;
        margin: 10px 0;
        background: rgba(255, 255, 255, 0.07);
        color: #ffffff !important;
        text-decoration: none !important;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .social-btn:hover {
        background: rgba(139, 92, 246, 0.3);
        border-color: #8b5cf6;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# 2. THÔNG TIN PROFILE CỦA BẠN (Chỉnh sửa thông tin tại đây)
# -------------------------------------------------------------------
NAME = "Nguyễn Văn A"
BIO = "Architecture Student @ HUCE 🏛️ | Gamer 🎮 | Photography Enthusiast 📸"

# Link ảnh đại diện (Có thể thay bằng link online hoặc file avatar.jpg)
AVATAR_URL = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500"

# Danh sách Liên kết Mạng xã hội
SOCIAL_LINKS = [
    {"title": "📘 Facebook Profile", "url": "https://facebook.com"},
    {"title": "💬 Discord Community", "url": "https://discord.com"},
    {"title": "▶️ Youtube Channel", "url": "https://youtube.com"},
    {"title": "📷 Instagram Portfolio", "url": "https://instagram.com"},
]

# -------------------------------------------------------------------
# 3. HIỂN THỊ PROFILE
# -------------------------------------------------------------------
# Ảnh đại diện, Tên & Mô tả
st.markdown(f"""
    <div class="profile-card">
        <img src="{AVATAR_URL}" class="avatar-img" alt="Avatar">
        <div class="profile-name">{NAME}</div>
        <div class="profile-bio">{BIO}</div>
    </div>
""", unsafe_allow_html=True)

# Danh sách nút link Mạng xã hội
for link in SOCIAL_LINKS:
    st.markdown(f"""
        <a href="{link['url']}" target="_blank" class="social-btn">
            {link['title']}
        </a>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# 4. NHẠC NỀN & NÚT PAUSE NHỎ NẰM GÓC DƯỚI BÊN PHẢI
# -------------------------------------------------------------------
MUSIC_FILE = "bg_music.mp3"  # Đặt file nhạc MP3 của bạn cùng thư mục với script này

audio_src = ""
if os.path.exists(MUSIC_FILE):
    with open(MUSIC_FILE, "rb") as f:
        audio_bytes = f.read()
        audio_src = f"data:audio/mp3;base64,{base64.b64encode(audio_bytes).decode()}"

if audio_src:
    player_html = f"""
    <audio id="bg-audio" loop autoplay src="{audio_src}"></audio>

    <button id="music-toggle-btn" onclick="toggleAudio()" title="Bật / Tắt Nhạc" style="
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 99999;
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background-color: #8b5cf6;
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.2);
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        font-size: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease-in-out;
    ">⏸️</button>

    <script>
    function toggleAudio() {{
        var audio = document.getElementById("bg-audio");
        var btn = document.getElementById("music-toggle-btn");
        if (audio.paused) {{
            audio.play();
            btn.innerHTML = "⏸️";
            btn.style.backgroundColor = "#8b5cf6";
        }} else {{
            audio.pause();
            btn.innerHTML = "▶️";
            btn.style.backgroundColor = "#334155";
        }}
    }}
    </script>
    """
    st.components.v1.html(player_html, height=0)
