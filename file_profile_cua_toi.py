# -*- coding: utf-8 -*-
import streamlit as st
import base64
import os
import re

st.set_page_config(page_title="Profile Của Tôi", page_icon="🔴", layout="wide")

NOTE_FILE = "data_notes.txt"
IMAGE_DIR = "uploaded_images"
YOUTUBE_FILE = "youtube_url.txt"

# 🔑 KHÓA BÍ MẬT TRÊN URL
SECRET_KEY = "17022006"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return ""

def extract_youtube_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else "jfKfPfyJRdk" # Video mặc định nếu link lỗi

image_path = '6fe31b6eb6ef60282b0e05dca6dd4418.jpg'
img_base64 = get_base64(image_path)

# Đọc link YouTube đã lưu
saved_yt_url = "https://www.youtube.com/watch?v=jfKfPfyJRdk"
if os.path.exists(YOUTUBE_FILE):
    with open(YOUTUBE_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content:
            saved_yt_url = content

yt_id = extract_youtube_id(saved_yt_url)

# Đọc ghi chú
saved_note = ""
if os.path.exists(NOTE_FILE):
    with open(NOTE_FILE, "r", encoding="utf-8") as f:
        saved_note = f.read()

# Đọc bộ sưu tập ảnh
saved_images_html = ""
image_list = sorted(os.listdir(IMAGE_DIR))
for img_name in image_list:
    img_p = os.path.join(IMAGE_DIR, img_name)
    b64 = get_base64(img_p)
    if b64:
        saved_images_html += f'<img src="data:image/png;base64,{b64}" class="img-card">'

# Kiểm tra quyền Admin từ URL (?key=17022006)
query_params = st.query_params
is_admin = query_params.get("key") == SECRET_KEY

if not is_admin:
    st.markdown(
        """
        <style>
            [data-testid="collapsedControl"] { display: none !important; }
            section[data-testid="stSidebar"] { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Rajdhani', sans-serif;
            background-color: #050000;
            margin: 0; padding: 20px 10px;
            color: #ff0000; overflow-x: hidden;
        }}
        #bg-canvas {{ position: fixed; top: 0; left: 0; z-index: -1; }}

        .container {{
            max-width: 900px; margin: auto;
            background: rgba(10, 0, 0, 0.96);
            padding: 40px; border: 2px solid #ff0000;
            box-shadow: 0 0 35px rgba(255, 0, 0, 0.6);
            text-align: center; position: relative;
            overflow: visible;
        }}

        #viz-canvas {{
            position: absolute; top: -40px; left: -40px;
            width: calc(100% + 80px); height: calc(100% + 80px);
            pointer-events: none; z-index: 5;
        }}

        .star {{
            position: absolute; background: #ff0000; border-radius: 50%; opacity: 0.6;
            animation: blink 1.5s infinite ease-in-out;
            box-shadow: 0 0 8px #ff0000;
        }}
        @keyframes blink {{ 0%, 100% {{ opacity: 0.3; transform: scale(0.8); }} 50% {{ opacity: 1; transform: scale(1.2); }} }}

        .welcome-img {{
            max-width: 100%; border: 2px solid #ff0000;
            box-shadow: 0 0 35px #ff0000; margin-bottom: 30px; position: relative; z-index: 2;
        }}

        .section {{ margin-top: 30px; text-align: center; position: relative; z-index: 2; }}

        .note-box {{
            width: 100%; height: 120px; padding: 15px;
            background: rgba(30, 0, 0, 0.85); border: 2px solid #ff0000;
            color: #ff0000; font-family: 'Times New Roman', Times, serif;
            text-align: center; font-size: 19px; box-sizing: border-box;
            box-shadow: inset 0 0 15px rgba(255,0,0,0.3);
            display: flex; align-items: center; justify-content: center;
        }}

        .yt-player-container {{
            background: rgba(30, 0, 0, 0.9);
            border: 2px solid #ff0000;
            padding: 15px;
            margin-top: 20px;
            box-shadow: 0 0 25px rgba(255, 0, 0, 0.5);
            position: relative; z-index: 3;
        }}

        .video-responsive {{
            overflow: hidden;
            padding-bottom: 56.25%;
            position: relative;
            height: 0;
        }}

        .video-responsive iframe {{
            left: 0; top: 0;
            height: 100%; width: 100%;
            position: absolute;
            border: none;
        }}

        .track-name {{
            font-family: 'Orbitron', sans-serif;
            font-size: 14px;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #ff0000;
            text-shadow: 0 0 5px #ff0000;
        }}

        #gallery {{ display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; margin-top: 20px; }}
        .img-card {{ width: 180px; height: 180px; object-fit: cover; border: 2px solid #ff0000; }}
    </style>
</head>
<body>
    <canvas id="bg-canvas"></canvas>
    <div class="container" id="mainContainer">
        <canvas id="viz-canvas"></canvas>
        <img src="data:image/jpeg;base64,{img_base64}" class="welcome-img">

        <div class="section">
            <div class="note-box">{saved_note if saved_note else "CHƯA CÓ GHI CHÚ NÀO ĐƯỢC LƯU..."}</div>
        </div>

        <div class="section">
            <div class="yt-player-container">
                <div class="track-name">🎬 Cyberpunk Youtube Player</div>
                <div class="video-responsive">
                    <iframe 
                        src="https://www.youtube.com/embed/{yt_id}?enablejsapi=1&autoplay=0&rel=0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                    </iframe>
                </div>
            </div>
        </div>

        <div class="section">
            <div id="gallery">
                {saved_images_html}
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        const vCanvas = document.getElementById('viz-canvas');
        const vCtx = vCanvas.getContext('2d');
        let particles = [];
        let phase = 0;

        function initCanvas() {{
            canvas.width = window.innerWidth; canvas.height = window.innerHeight;
            vCanvas.width = vCanvas.offsetWidth; vCanvas.height = vCanvas.offsetHeight;
        }}
        window.addEventListener('resize', initCanvas); initCanvas();

        function drawCurvedWave(points, color, width, glow) {{
            vCtx.save();
            vCtx.strokeStyle = color;
            vCtx.lineWidth = width;
            vCtx.shadowBlur = glow;
            vCtx.shadowColor = '#ff0000';
            vCtx.beginPath();
            vCtx.moveTo(points[0].x, points[0].y);

            for (let i = 0; i < points.length - 1; i++) {{
                let xc = (points[i].x + points[i + 1].x) / 2;
                let yc = (points[i].y + points[i + 1].y) / 2;
                vCtx.quadraticCurveTo(points[i].x, points[i].y, xc, yc);
            }}
            vCtx.lineTo(points[points.length - 1].x, points[points.length - 1].y);
            vCtx.stroke();
            vCtx.restore();
        }}

        function visualize() {{
            requestAnimationFrame(visualize);
            phase += 0.05;

            vCtx.clearRect(0, 0, vCanvas.width, vCanvas.height);

            const offset = 40;
            const w = vCanvas.width - offset * 2;
            const h = vCanvas.height - offset * 2;
            const len = 32;

            let topPts = [], botPts = [], leftPts = [], rightPts = [];

            for (let i = 0; i <= len; i++) {{
                let amp = Math.sin(phase + i * 0.35) * 12 + Math.cos(phase * 1.5 + i * 0.2) * 8;

                topPts.push({{ x: offset + (i / len) * w, y: offset - amp }});
                botPts.push({{ x: offset + (i / len) * w, y: offset + h + amp }});
                leftPts.push({{ x: offset - amp, y: offset + (i / len) * h }});
                rightPts.push({{ x: offset + w + amp, y: offset + (i / len) * h }});
            }}

            drawCurvedWave(topPts, '#ff0000', 3, 20);
            drawCurvedWave(botPts, '#ff0000', 3, 20);
            drawCurvedWave(leftPts, '#ff0000', 3, 20);
            drawCurvedWave(rightPts, '#ff0000', 3, 20);

            let topPtsSub = topPts.map(p => ({{ x: p.x, y: p.y - 5 }}));
            let botPtsSub = botPts.map(p => ({{ x: p.x, y: p.y + 5 }}));
            drawCurvedWave(topPtsSub, 'rgba(255, 50, 50, 0.4)', 1.5, 10);
            drawCurvedWave(botPtsSub, 'rgba(255, 50, 50, 0.4)', 1.5, 10);
        }}
        visualize();

        class P {{
            constructor() {{ this.reset(); }}
            reset() {{
                this.x = Math.random()*canvas.width; this.y = Math.random()*canvas.height;
                this.vx = (Math.random()-0.5)*1.2; this.vy = (Math.random()-0.5)*1.2;
                this.s = Math.random()*3 + 1; this.opacity = Math.random() * 0.5 + 0.3;
            }}
            u() {{
                this.x += this.vx; this.y += this.vy;
                if(this.x<0||this.x>canvas.width||this.y<0||this.y>canvas.height) this.reset();
            }}
            d() {{
                ctx.shadowBlur = 10; ctx.shadowColor = '#ff0000';
                ctx.fillStyle = `rgba(255, 0, 0, ${{this.opacity}})`;
                ctx.beginPath(); ctx.arc(this.x,this.y,this.s,0,Math.PI*2); ctx.fill();
                ctx.shadowBlur = 0;
            }}
        }}

        for(let i=0;i<300;i++) particles.push(new P());
        function anim() {{
            ctx.fillStyle = 'rgba(5, 0, 0, 0.15)'; ctx.fillRect(0,0,canvas.width,canvas.height);
            particles.forEach(p=>{{p.u();p.d();}});
            requestAnimationFrame(anim);
        }}
        anim();

        for(let i=0; i<60; i++) {{
            let star = document.createElement('div'); star.className = 'star';
            let size = Math.random()*4 + 'px';
            star.style.width = size; star.style.height = size;
            star.style.top = Math.random()*100 + '%'; star.style.left = Math.random()*100 + '%';
            document.getElementById('mainContainer').appendChild(star);
        }}
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=1050, scrolling=True)

# --- KHU VỰC ADMIN TRÊN SIDEBAR ---
if is_admin:
    st.sidebar.title("👑 Chế độ Admin")
    st.sidebar.success("Đã mở khóa quyền quản trị!")
    st.sidebar.markdown("---")

    # 1. Quản lý Link YouTube
    st.sidebar.subheader("📺 Cập nhật Video YouTube")
    new_yt_url = st.sidebar.text_input("Dán link YouTube mới:", value=saved_yt_url)
    if st.sidebar.button("Đổi Video / Nhạc"):
        with open(YOUTUBE_FILE, "w", encoding="utf-8") as f:
            f.write(new_yt_url.strip())
        st.sidebar.success("Đã cập nhật Video mới!")
        st.rerun()

    st.sidebar.markdown("---")

    # 2. Quản lý Ghi chú
    st.sidebar.subheader("📝 Quản lý ghi chú")
    new_note = st.sidebar.text_area("Cập nhật ghi chú mới:", value=saved_note)
    if st.sidebar.button("Lưu Ghi Chú"):
        with open(NOTE_FILE, "w", encoding="utf-8") as f:
            f.write(new_note)
        st.sidebar.success("Đã cập nhật ghi chú!")
        st.rerun()

    st.sidebar.markdown("---")

    # 3. Quản lý Bộ sưu tập & Xoá Ảnh
    st.sidebar.subheader("🖼️ Quản lý hình ảnh")
    uploaded_files = st.sidebar.file_uploader("Thêm ảnh mới:", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    if st.sidebar.button("Tải Ảnh Lên"):
        if uploaded_files:
            for u_file in uploaded_files:
                save_path = os.path.join(IMAGE_DIR, u_file.name)
                with open(save_path, "wb") as f:
                    f.write(u_file.getbuffer())
            st.sidebar.success("Đã đăng tải ảnh!")
            st.rerun()

    if image_list:
        st.sidebar.markdown("**Danh sách ảnh hiện tại (Xoá):**")
        for img_name in image_list:
            col_img, col_btn = st.sidebar.columns([3, 1])
            col_img.caption(img_name)
            if col_btn.button("❌", key=f"del_{img_name}"):
                os.remove(os.path.join(IMAGE_DIR, img_name))
                st.sidebar.success(f"Đã xoá {img_name}")
                st.rerun()
