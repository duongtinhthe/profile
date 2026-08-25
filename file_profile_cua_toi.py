# -*- coding: utf-8 -*-
import streamlit as st
import base64
import os
import json

st.set_page_config(page_title="Profile Của Tôi", page_icon="🔴", layout="wide")

NOTE_FILE = "data_notes.txt"
IMAGE_DIR = "uploaded_images"
SOCIAL_FILE = "social_links.json"
AUDIO_FILE = "bg_music.mp3"

# 🔑 KHÓA BÍ MẬT TRÊN URL
SECRET_KEY = "17022006"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return ""

image_path = '6fe31b6eb6ef60282b0e05dca6dd4418.jpg'
img_base64 = get_base64(image_path)
audio_base64 = get_base64(AUDIO_FILE)

# Đọc / Ghi Social Links
default_socials = {
    "facebook": "https://facebook.com",
    "youtube": "https://youtube.com",
    "tiktok": "https://tiktok.com"
}

if os.path.exists(SOCIAL_FILE):
    try:
        with open(SOCIAL_FILE, "r", encoding="utf-8") as f:
            social_data = json.load(f)
            default_socials.update(social_data)
    except Exception:
        pass

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

audio_src = f"data:audio/mp3;base64,{audio_base64}" if audio_base64 else ""

html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Rajdhani', sans-serif;
            background-color: #050000;
            margin: 0; 
            padding: 10px 5px;
            color: #ff0000; 
            overflow-x: hidden;
        }}
        #bg-canvas {{ position: fixed; top: 0; left: 0; z-index: -1; width: 100%; height: 100%; }}

        .container {{
            width: 100%;
            max-width: 900px; 
            margin: auto;
            background: rgba(10, 0, 0, 0.96);
            padding: 30px 20px; 
            border: 2px solid #ff0000;
            box-shadow: 0 0 35px rgba(255, 0, 0, 0.6);
            text-align: center; 
            position: relative;
            overflow: visible;
        }}

        #viz-canvas {{
            position: absolute; 
            top: -20px; 
            left: -20px;
            width: calc(100% + 40px); 
            height: calc(100% + 40px);
            pointer-events: none; 
            z-index: 5;
        }}

        .star {{
            position: absolute; background: #ff0000; border-radius: 50%; opacity: 0.6;
            animation: blink 1.5s infinite ease-in-out;
            box-shadow: 0 0 8px #ff0000;
        }}
        @keyframes blink {{ 0%, 100% {{ opacity: 0.3; transform: scale(0.8); }} 50% {{ opacity: 1; transform: scale(1.2); }} }}

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

        .welcome-img-wrapper {{
            position: relative;
            display: inline-block;
            margin-bottom: 25px;
            width: 100%;
            z-index: 2;
        }}
        
        .welcome-img {{
            max-width: 100%;
            height: auto;
            border: 2px solid #ff0000;
            animation: neonGlowPulse 2.5s infinite ease-in-out;
            display: block;
            margin: 0 auto;
        }}

        .section {{ margin-top: 25px; text-align: center; position: relative; z-index: 2; width: 100%; }}

        /* Ô Ghi chú */
        .note-box {{
            width: 100%; 
            min-height: 100px; 
            padding: 15px;
            background: rgba(25, 0, 0, 0.9);
            border: 2px solid #ff0000;
            color: #ff3333; 
            font-family: 'Times New Roman', Times, serif;
            text-align: center; 
            font-size: 18px; 
            box-sizing: border-box;
            display: flex; 
            align-items: center; 
            justify-content: center;
            animation: neonGlowPulse 3s infinite ease-in-out;
            transition: transform 0.3s ease;
            word-break: break-word;
        }}
        .note-box:hover {{
            transform: scale(1.01);
            color: #ffffff;
            text-shadow: 0 0 8px #ff0000;
        }}

        /* 🌟 KHUNG LOGO MXH CYBERPUNK */
        .social-container {{
            background: rgba(25, 0, 0, 0.92);
            border: 2px solid #ff0000;
            padding: 20px 15px;
            margin-top: 15px;
            animation: neonGlowPulse 2.8s infinite ease-in-out;
            position: relative; 
            z-index: 3;
            width: 100%;
        }}

        .social-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 16px;
            margin-bottom: 18px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #ff3333;
            text-shadow: 0 0 8px #ff0000;
        }}

        .social-icons {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 30px;
        }}

        .social-btn {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 65px;
            height: 65px;
            border-radius: 50%;
            background: rgba(10, 0, 0, 0.8);
            border: 2px solid #ff0000;
            color: #ff3333;
            font-size: 28px;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
            cursor: pointer;
        }}

        .social-btn:hover {{
            transform: translateY(-5px) scale(1.1);
            color: #ffffff;
            border-color: #ffffff;
            box-shadow: 0 0 25px #ff0000, inset 0 0 10px #ff0000;
            background: #ff0000;
        }}

        /* Khung bộ sưu tập */
        #gallery {{ 
            display: flex; 
            flex-wrap: wrap; 
            gap: 12px; 
            justify-content: center; 
            margin-top: 15px; 
            width: 100%;
        }}
        
        .img-card-wrapper {{
            position: relative;
            padding: 2px;
            background: rgba(20, 0, 0, 0.8);
        }}
        
        .img-card {{ 
            width: 160px; 
            height: 160px; 
            object-fit: cover; 
            border: 2px solid #ff0000; 
            animation: neonGlowPulse 3.5s infinite ease-in-out;
            transition: all 0.3s ease;
            display: block;
        }}

        .img-card:hover {{
            transform: scale(1.05);
            border-color: #ffffff;
            box-shadow: 0 0 25px #ff0000;
            z-index: 10;
        }}

        @media (max-width: 768px) {{
            body {{ padding: 5px 0; }}
            .container {{ padding: 15px 10px; border-width: 1.5px; }}
            #viz-canvas {{
                top: -10px; left: -10px;
                width: calc(100% + 20px); height: calc(100% + 20px);
            }}
            .note-box {{ font-size: 15px; padding: 10px; min-height: 80px; }}
            .social-container {{ padding: 15px 10px; }}
            .social-title {{ font-size: 13px; margin-bottom: 12px; }}
            .social-icons {{ gap: 20px; }}
            .social-btn {{ width: 50px; height: 50px; font-size: 22px; }}
            #gallery {{ gap: 8px; }}
            .img-card {{
                width: calc(50vw - 25px); max-width: 160px;
                height: calc(50vw - 25px); max-height: 160px;
            }}
        }}
    </style>
</head>
<body>
    <canvas id="bg-canvas"></canvas>
    
    <!-- Audio ẩn phát file nhạc MP3 nội bộ -->
    <audio id="bg-audio" src="{audio_src}" loop preload="auto"></audio>

    <div class="container" id="mainContainer">
        <canvas id="viz-canvas"></canvas>
        
        <div class="welcome-img-wrapper">
            <img src="data:image/jpeg;base64,{img_base64}" class="welcome-img">
        </div>

        <div class="section">
            <div class="note-box">{saved_note if saved_note else "CHƯA CÓ GHI CHÚ NÀO ĐƯỢC LƯU..."}</div>
        </div>

        <!-- 🌟 MẠNG XÃ HỘI -->
        <div class="section">
            <div class="social-container">
                <div class="social-title">⚡ KẾT NỐI MẠNG XÃ HỘI ⚡</div>
                <div class="social-icons">
                    <a href="{default_socials['facebook']}" target="_blank" class="social-btn" title="Facebook">
                        <i class="fab fa-facebook-f"></i>
                    </a>
                    <a href="{default_socials['youtube']}" target="_blank" class="social-btn" title="YouTube">
                        <i class="fab fa-youtube"></i>
                    </a>
                    <a href="{default_socials['tiktok']}" target="_blank" class="social-btn" title="TikTok">
                        <i class="fab fa-tiktok"></i>
                    </a>
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
        const audio = document.getElementById('bg-audio');

        let particles = [];
        let phase = 0;
        let audioCtx, analyser, dataArray;
        let isAudioSetup = false;

        function initCanvas() {{
            canvas.width = window.innerWidth; 
            canvas.height = window.innerHeight;
            vCanvas.width = vCanvas.offsetWidth; 
            vCanvas.height = vCanvas.offsetHeight;
        }}
        window.addEventListener('resize', initCanvas); 
        initCanvas();

        function setupAudioContext() {{
            if (isAudioSetup || !audio.src) return;
            try {{
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                analyser = audioCtx.createAnalyser();
                const source = audioCtx.createMediaElementSource(audio);
                source.connect(analyser);
                analyser.connect(audioCtx.destination);
                analyser.fftSize = 64;
                dataArray = new Uint8Array(analyser.frequencyBinCount);
                isAudioSetup = true;
            }} catch (e) {{
                console.log("Audio Context Error: ", e);
            }}
        }}

        function playAudio() {{
            if (!audio.src) return;
            setupAudioContext();
            if (audioCtx && audioCtx.state === 'suspended') {{
                audioCtx.resume();
            }}
            audio.play().catch(e => console.log("Auto-play blocked:", e));
        }}

        window.addEventListener('click', playAudio, {{ once: true }});
        window.addEventListener('touchstart', playAudio, {{ once: true }});

        function drawLightning(x1, y1, x2, y2, intensity) {{
            vCtx.strokeStyle = `rgba(255, 30, 30, ${{intensity}})`;
            vCtx.lineWidth = 2 + Math.random() * 2;
            vCtx.shadowBlur = 15; vCtx.shadowColor = '#ff0000';
            vCtx.beginPath();
            vCtx.moveTo(x1, y1);
            let steps = 6;
            for(let i=1; i<=steps; i++) {{
                let tx = x1 + (x2-x1)*(i/steps) + (Math.random()-0.5)*15*intensity;
                let ty = y1 + (y2-y1)*(i/steps) + (Math.random()-0.5)*15*intensity;
                vCtx.lineTo(tx, ty);
            }}
            vCtx.stroke();
        }}

        function drawCurvedWave(points, color, width, glow) {{
            if (!points || points.length === 0) return;
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

            const isMobile = window.innerWidth <= 768;
            const offset = isMobile ? 10 : 20;
            const w = vCanvas.width - offset * 2;
            const h = vCanvas.height - offset * 2;
            const len = isMobile ? 20 : 32;

            if (w <= 0 || h <= 0) return;

            let avgAmp = 0;
            if (isAudioSetup && analyser && !audio.paused) {{
                analyser.getByteFrequencyData(dataArray);
                let sum = 0;
                for (let i = 0; i < dataArray.length; i++) {{
                    sum += dataArray[i];
                }}
                avgAmp = sum / dataArray.length;
            }}

            let isPlaying = !audio.paused && avgAmp > 5;

            if (isPlaying) {{
                phase += 0.12;
            }} else {{
                phase += 0.03;
            }}

            let topPts = [], botPts = [], leftPts = [], rightPts = [];

            for (let i = 0; i <= len; i++) {{
                let amp = 0;
                if (isPlaying) {{
                    let freqVal = dataArray ? (dataArray[i % dataArray.length] / 255.0) : 0.5;
                    let bass = Math.sin(phase * 2.5) * (isMobile ? 12 : 22) * freqVal;
                    let freq = Math.sin(phase + i * 0.4) * (isMobile ? 10 : 18) + Math.cos(phase * 1.8 + i * 0.3) * 8;
                    amp = Math.abs(bass + freq);
                }} else {{
                    amp = Math.sin(phase + i * 0.2) * (isMobile ? 3 : 5);
                }}

                topPts.push({{ x: offset + (i / len) * w, y: offset - amp }});
                botPts.push({{ x: offset + (i / len) * w, y: offset + h + amp }});
                leftPts.push({{ x: offset - amp, y: offset + (i / len) * h }});
                rightPts.push({{ x: offset + w + amp, y: offset + (i / len) * h }});
            }}

            drawCurvedWave(topPts, '#ff0000', isMobile ? 2 : 3, 15);
            drawCurvedWave(botPts, '#ff0000', isMobile ? 2 : 3, 15);
            drawCurvedWave(leftPts, '#ff0000', isMobile ? 2 : 3, 15);
            drawCurvedWave(rightPts, '#ff0000', isMobile ? 2 : 3, 15);

            let topPtsSub = topPts.map(p => ({{ x: p.x, y: p.y - 4 }}));
            let botPtsSub = botPts.map(p => ({{ x: p.x, y: p.y + 4 }}));
            drawCurvedWave(topPtsSub, 'rgba(255, 50, 50, 0.4)', 1, 8);
            drawCurvedWave(botPtsSub, 'rgba(255, 50, 50, 0.4)', 1, 8);

            if (isPlaying && Math.random() > 0.65) {{
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
                this.s = Math.random()*2 + 1; this.opacity = Math.random() * 0.5 + 0.3;
            }}
            u() {{
                this.x += this.vx; this.y += this.vy;
                if(this.x<0||this.x>canvas.width||this.y<0||this.y>canvas.height) this.reset();
            }}
            d() {{
                ctx.shadowBlur = 8; ctx.shadowColor = '#ff0000';
                ctx.fillStyle = `rgba(255, 0, 0, ${{this.opacity}})`;
                ctx.beginPath(); ctx.arc(this.x,this.y,this.s,0,Math.PI*2); ctx.fill();
                ctx.shadowBlur = 0;
            }}
        }}

        const particleCount = window.innerWidth <= 768 ? 120 : 250;
        for(let i=0; i<particleCount; i++) particles.push(new P());
        
        function anim() {{
            ctx.fillStyle = 'rgba(5, 0, 0, 0.15)'; 
            ctx.fillRect(0,0,canvas.width,canvas.height);
            particles.forEach(p=>{{p.u();p.d();}});
            requestAnimationFrame(anim);
        }}
        anim();

        for(let i=0; i<40; i++) {{
            let star = document.getElementById('mainContainer');
            if(star) {{
                let s = document.createElement('div'); s.className = 'star';
                let size = Math.random()*3 + 'px';
                s.style.width = size; s.style.height = size;
                s.style.top = Math.random()*100 + '%'; s.style.left = Math.random()*100 + '%';
                star.appendChild(s);
            }}
        }}
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=900, scrolling=True)

# --- KHU VỰC ADMIN TRÊN SIDEBAR ---
if is_admin:
    st.sidebar.title("👑 Chế độ Admin")
    st.sidebar.success("Đã mở khóa quyền quản trị!")
    st.sidebar.markdown("---")

    # 1. Tải nhạc MP3 từ máy tính lên
    st.sidebar.subheader("🎵 Tải nhạc MP3 từ máy tính")
    uploaded_audio = st.sidebar.file_uploader("Chọn file MP3 từ máy:", type=['mp3'])
    if st.sidebar.button("Lưu File Nhạc"):
        if uploaded_audio is not None:
            with open(AUDIO_FILE, "wb") as f:
                f.write(uploaded_audio.getbuffer())
            st.sidebar.success("Đã lưu file MP3 mới thành công!")
            st.rerun()

    if os.path.exists(AUDIO_FILE):
        st.sidebar.caption("✅ Đã có file MP3 lưu trên hệ thống.")

    st.sidebar.markdown("---")

    # 2. Quản lý Link Mạng Xã Hội
    st.sidebar.subheader("🔗 Cập nhật Link MXH")
    fb_link = st.sidebar.text_input("Link Facebook:", value=default_socials.get("facebook", ""))
    yt_link = st.sidebar.text_input("Link YouTube:", value=default_socials.get("youtube", ""))
    tiktok_link = st.sidebar.text_input("Link TikTok:", value=default_socials.get("tiktok", ""))

    if st.sidebar.button("Lưu Link MXH"):
        new_data = {
            "facebook": fb_link.strip(),
            "youtube": yt_link.strip(),
            "tiktok": tiktok_link.strip()
        }
        with open(SOCIAL_FILE, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        st.sidebar.success("Đã cập nhật liên kết mới!")
        st.rerun()

    st.sidebar.markdown("---")

    # 3. Quản lý Ghi chú
    st.sidebar.subheader("📝 Quản lý ghi chú")
    new_note = st.sidebar.text_area("Cập nhật ghi chú mới:", value=saved_note)
    if st.sidebar.button("Lưu Ghi Chú"):
        with open(NOTE_FILE, "w", encoding="utf-8") as f:
            f.write(new_note)
        st.sidebar.success("Đã cập nhật ghi chú!")
        st.rerun()

    st.sidebar.markdown("---")

    # 4. Quản lý Bộ sưu tập & Xoá Ảnh
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
