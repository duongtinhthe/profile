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
    if not url:
        return "jfKfPfyJRdk"
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be\/([0-9A-Za-z_-]{11})',
        r'embed\/([0-9A-Za-z_-]{11})',
        r'shorts\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    if len(url.strip()) == 11 and re.match(r'^[0-9A-Za-z_-]{11}$', url.strip()):
        return url.strip()
    return "jfKfPfyJRdk"

image_path = '6fe31b6eb6ef60282b0e05dca6dd4418.jpg'
img_base64 = get_base64(image_path)

saved_yt_url = "https://www.youtube.com/watch?v=jfKfPfyJRdk"
if os.path.exists(YOUTUBE_FILE):
    with open(YOUTUBE_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content:
            saved_yt_url = content

yt_id = extract_youtube_id(saved_yt_url)

saved_note = ""
if os.path.exists(NOTE_FILE):
    with open(NOTE_FILE, "r", encoding="utf-8") as f:
        saved_note = f.read()

saved_images_html = ""
image_list = sorted(os.listdir(IMAGE_DIR))
for img_name in image_list:
    img_p = os.path.join(IMAGE_DIR, img_name)
    b64 = get_base64(img_p)
    if b64:
        saved_images_html += f'<div class="img-card-wrapper"><img src="data:image/png;base64,{b64}" class="img-card"></div>'

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

        /* 🌟 HIỆU ỨNG VIỀN QUÉT SÁNG DẠNG NEON CHO CÁC KHUNG */
        @keyframes neonGlowPulse {{
            0% {{
                border-color: #ff0000;
                box-shadow: 0 0 15px rgba(255, 0, 0, 0.6), inset 0 0 10px rgba(255, 0, 0, 0.4);
            }}
            50% {{
                border-color: #ff5555;
                box-shadow: 0 0 30px rgba(255, 30, 30, 0.9), inset 0 0 20px rgba(255, 30, 30, 0.6);
            }}
            100% {{
                border-color: #ff0000;
                box-shadow: 0 0 15px rgba(255, 0, 0, 0.6), inset 0 0 10px rgba(255, 0, 0, 0.4);
            }}
        }}

        /* Ảnh Welcome chính */
        .welcome-img-wrapper {{
            position: relative;
            display: inline-block;
            margin-bottom: 30px;
            z-index: 2;
        }}
        
        .welcome-img {{
            max-width: 100%;
            border: 2px solid #ff0000;
            animation: neonGlowPulse 2.5s infinite ease-in-out;
            display: block;
        }}

        .section {{ margin-top: 30px; text-align: center; position: relative; z-index: 2; }}

        /* Ô Ghi chú sáng động */
        .note-box {{
            width: 100%; height: 120px; padding: 15px;
            background: rgba(25, 0, 0, 0.9);
            border: 2px solid #ff0000;
            color: #ff3333; font-family: 'Times New Roman', Times, serif;
            text-align: center; font-size: 19px; box-sizing: border-box;
            display: flex; align-items: center; justify-content: center;
            animation: neonGlowPulse 3s infinite ease-in-out;
            transition: transform 0.3s ease;
        }}
        .note-box:hover {{
            transform: scale(1.01);
            color: #ffffff;
            text-shadow: 0 0 8px #ff0000;
        }}

        /* Ô Trình phát YouTube sáng động */
        .yt-player-container {{
            background: rgba(25, 0, 0, 0.92);
            border: 2px solid #ff0000;
            padding: 18px;
            margin-top: 20px;
            animation: neonGlowPulse 2.8s infinite ease-in-out;
            position: relative; z-index: 3;
            transition: transform 0.3s ease;
        }}
        .yt-player-container:hover {{
            transform: translateY(-3px);
        }}

        .video-responsive {{
            overflow: hidden;
            padding-bottom: 56.25%;
            position: relative;
            height: 0;
            background: #000;
            border: 1px solid rgba(255,0,0,0.8);
            box-shadow: 0 0 15px rgba(255,0,0,0.5);
        }}

        .video-responsive iframe, .video-responsive div#player {{
            left: 0; top: 0;
            height: 100%; width: 100%;
            position: absolute;
            border: none;
        }}

        .track-name {{
            font-family: 'Orbitron', sans-serif;
            font-size: 15px;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #ff3333;
            text-shadow: 0 0 8px #ff0000;
        }}

        /* Khung bộ sưu tập & Thẻ ảnh rực rỡ */
        #gallery {{ display: flex; flex-wrap: wrap; gap: 18px; justify-content: center; margin-top: 20px; }}
        
        .img-card-wrapper {{
            position: relative;
            padding: 2px;
            background: rgba(20, 0, 0, 0.8);
        }}
        
        .img-card {{ 
            width: 180px; 
            height: 180px; 
            object-fit: cover; 
            border: 2px solid #ff0000; 
            animation: neonGlowPulse 3.5s infinite ease-in-out;
            transition: all 0.3s ease;
            display: block;
        }}

        .img-card:hover {{
            transform: scale(1.08);
            border-color: #ffffff;
            box-shadow: 0 0 25px #ff0000, 0 0 40px #ff0000;
            z-index: 10;
        }}
    </style>
</head>
<body>
    <canvas id="bg-canvas"></canvas>
    <div class="container" id="mainContainer">
        <canvas id="viz-canvas"></canvas>
        
        <div class="welcome-img-wrapper">
            <img src="data:image/jpeg;base64,{img_base64}" class="welcome-img">
        </div>

        <div class="section">
            <div class="note-box">{saved_note if saved_note else "CHƯA CÓ GHI CHÚ NÀO ĐƯỢC LƯU..."}</div>
        </div>

        <div class="section">
            <div class="yt-player-container">
                <div class="track-name">⚡ Cyberpunk Youtube Player ⚡</div>
                <div class="video-responsive">
                    <div id="player"></div>
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
        // Load YouTube IFrame API
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        const vCanvas = document.getElementById('viz-canvas');
        const vCtx = vCanvas.getContext('2d');
        let particles = [];
        let phase = 0;
        let isPlaying = false;

        function initCanvas() {{
            canvas.width = window.innerWidth; canvas.height = window.innerHeight;
            vCanvas.width = vCanvas.offsetWidth; vCanvas.height = vCanvas.offsetHeight;
        }}
        window.addEventListener('resize', initCanvas); initCanvas();

        let player;
        function onYouTubeIframeAPIReady() {{
            player = new YT.Player('player', {{
                height: '100%',
                width: '100%',
                videoId: '{yt_id}',
                playerVars: {{
                    'autoplay': 0,
                    'controls': 1,
                    'rel': 0,
                    'enablejsapi': 1
                }},
                events: {{
                    'onStateChange': onPlayerStateChange
                }}
            }});
        }}

        function onPlayerStateChange(event) {{
            if (event.data === YT.PlayerState.PLAYING) {{
                isPlaying = true;
            }} else {{
                isPlaying = false;
            }}
        }}

        function drawLightning(x1, y1, x2, y2, intensity) {{
            vCtx.strokeStyle = `rgba(255, 30, 30, ${{intensity}})`;
            vCtx.lineWidth = 2 + Math.random() * 2;
            vCtx.shadowBlur = 20; vCtx.shadowColor = '#ff0000';
            vCtx.beginPath();
            vCtx.moveTo(x1, y1);
            let steps = 6;
            for(let i=1; i<=steps; i++) {{
                let tx = x1 + (x2-x1)*(i/steps) + (Math.random()-0.5)*25*intensity;
                let ty = y1 + (y2-y1)*(i/steps) + (Math.random()-0.5)*25*intensity;
                vCtx.lineTo(tx, ty);
            }}
            vCtx.stroke();
        }}

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
            vCtx.clearRect(0, 0, vCanvas.width, vCanvas.height);

            const offset = 40;
            const w = vCanvas.width - offset * 2;
            const h = vCanvas.height - offset * 2;
            const len = 32;

            if (isPlaying) {{
                phase += 0.12;
            }} else {{
                phase += 0.02;
            }}

            let topPts = [], botPts = [], leftPts = [], rightPts = [];

            for (let i = 0; i <= len; i++) {{
                let amp = 0;
                if (isPlaying) {{
                    let bass = Math.sin(phase * 2.5) * 18;
                    let freq = Math.sin(phase + i * 0.4) * 20 + Math.cos(phase * 1.8 + i * 0.3) * 12;
                    amp = Math.abs(bass + freq);
                }} else {{
                    amp = Math.sin(phase + i * 0.2) * 4;
                }}

                topPts.push({{ x: offset + (i / len) * w, y: offset - amp }});
                botPts.push({{ x: offset + (i / len) * w, y: offset + h + amp }});
                leftPts.push({{ x: offset - amp, y: offset + (i / len) * h }});
                rightPts.push({{ x: offset + w + amp, y: offset + (i / len) * h }});
            }}

            drawCurvedWave(topPts, '#ff0000', 3, 20);
            drawCurvedWave(botPts, '#ff0000', 3, 20);
            drawCurvedWave(leftPts, '#ff0000', 3, 20);
            drawCurvedWave(rightPts, '#ff0000', 3, 20);

            let topPtsSub = topPts.map(p => ({{ x: p.x, y: p.y - 6 }}));
            let botPtsSub = botPts.map(p => ({{ x: p.x, y: p.y + 6 }}));
            drawCurvedWave(topPtsSub, 'rgba(255, 50, 50, 0.4)', 1.5, 10);
            drawCurvedWave(botPtsSub, 'rgba(255, 50, 50, 0.4)', 1.5, 10);

            if (isPlaying && Math.random() > 0.7) {{
                let intensity = Math.random() * 0.8 + 0.2;
                drawLightning(offset, offset, offset + w, offset, intensity);
                drawLightning(offset + w, offset, offset + w, offset + h, intensity);
            }}
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
            let star = document.getElementById('mainContainer');
            if(star) {{
                let s = document.createElement('div'); s.className = 'star';
                let size = Math.random()*4 + 'px';
                s.style.width = size; s.style.height = size;
                s.style.top = Math.random()*100 + '%'; s.style.left = Math.random()*100 + '%';
                star.appendChild(s);
            }}
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
