# -*- coding: utf-8 -*-
import streamlit as st
import base64
import os

st.set_page_config(page_title="Profile Của Tôi", page_icon="🔴", layout="wide")

NOTE_FILE = "data_notes.txt"
IMAGE_DIR = "uploaded_images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return ""

image_path = '6fe31b6eb6ef60282b0e05dca6dd4418.jpg'
audio_path = 'Sơn Tùng M-TP x Tyga - Come My Way (Acigode Remix).mp3'

img_base64 = get_base64(image_path)
audio_base64 = get_base64(audio_path)

saved_note = ""
if os.path.exists(NOTE_FILE):
    with open(NOTE_FILE, "r", encoding="utf-8") as f:
        saved_note = f.read()

saved_images_html = ""
for img_name in sorted(os.listdir(IMAGE_DIR)):
    img_p = os.path.join(IMAGE_DIR, img_name)
    b64 = get_base64(img_p)
    if b64:
        saved_images_html += f'<img src="data:image/png;base64,{b64}" class="img-card">'

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
            position: absolute; top: -30px; left: -30px;
            width: calc(100% + 60px); height: calc(100% + 60px);
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

        .audio-player-container {{
            background: rgba(30, 0, 0, 0.9);
            border: 2px solid #ff0000;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 0 25px rgba(255, 0, 0, 0.5);
        }}
        audio {{
            width: 100%;
            filter: invert(100%) hue-rotate(180deg) brightness(1.5);
        }}
        .track-name {{
            font-family: 'Orbitron', sans-serif;
            font-size: 14px;
            margin-bottom: 10px;
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
            <div class="audio-player-container">
                <div class="track-name">Now Playing: Come My Way (Remix)</div>
                <audio id="audioPlayer" controls crossorigin="anonymous">
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
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

        function initCanvas() {{
            canvas.width = window.innerWidth; canvas.height = window.innerHeight;
            vCanvas.width = vCanvas.offsetWidth; vCanvas.height = vCanvas.offsetHeight;
        }}
        window.addEventListener('resize', initCanvas); initCanvas();

        const audio = document.getElementById('audioPlayer');
        const mainContainer = document.getElementById('mainContainer');
        let audioCtx, analyser, dataArray;

        audio.onplay = () => {{
            if (!audioCtx) {{
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const source = audioCtx.createMediaElementSource(audio);
                analyser = audioCtx.createAnalyser();
                source.connect(analyser); analyser.connect(audioCtx.destination);
                analyser.fftSize = 128; 
                dataArray = new Uint8Array(analyser.frequencyBinCount);
                visualize();
            }}
        }};

        function drawLightning(x1, y1, x2, y2, intensity) {{
            vCtx.strokeStyle = `rgba(255, 0, 50, ${{intensity}})`;
            vCtx.lineWidth = 2 + Math.random() * 2;
            vCtx.shadowBlur = 20; vCtx.shadowColor = '#ff0033';
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

        function visualize() {{
            if (!analyser) return;
            requestAnimationFrame(visualize);
            analyser.getByteFrequencyData(dataArray);

            let sum = 0; 
            for(let i = 0; i < 15; i++) sum += dataArray[i];
            let avg = sum / 15;

            // Đổi hiệu ứng phát sáng khung theo nhịp Bass
            let glow = 30 + (avg / 2);
            mainContainer.style.boxShadow = `0 0 ${{glow}}px rgba(255, 0, 0, ${{0.5 + avg/200}})`;

            vCtx.clearRect(0, 0, vCanvas.width, vCanvas.height);

            const offset = 30; // Khoảng cách tới mép viền
            const w = vCanvas.width - offset * 2;
            const h = vCanvas.height - offset * 2;
            const numBars = dataArray.length;

            vCtx.fillStyle = '#ff0000';
            vCtx.shadowBlur = 15;
            vCtx.shadowColor = '#ff0000';

            // Vẽ Equalizer Bars nhảy múa 4 CẠNH VIỀN
            for (let i = 0; i < numBars; i++) {{
                let val = dataArray[i] / 255.0; // Giá trị từ 0.0 - 1.0
                let barLen = val * 55; // Chiều cao sóng tối đa 55px

                // 1. Viền Trên
                let xTop = offset + (i / numBars) * w;
                vCtx.fillRect(xTop, offset - barLen, w / numBars - 2, barLen);

                // 2. Viền Dưới
                let xBot = offset + (i / numBars) * w;
                vCtx.fillRect(xBot, offset + h, w / numBars - 2, barLen);

                // 3. Viền Trái
                let yLeft = offset + (i / numBars) * h;
                vCtx.fillRect(offset - barLen, yLeft, barLen, h / numBars - 2);

                // 4. Viền Phải
                let yRight = offset + (i / numBars) * h;
                vCtx.fillRect(offset + w, yRight, barLen, h / numBars - 2);
            }}

            // Phát tia sét xung quanh viền khi nhạc chạm Bass mạnh
            if(avg > 140) {{
                let intensity = (avg - 140) / 115;
                if(Math.random() > 0.3) drawLightning(offset, offset, offset + w, offset, intensity);
                if(Math.random() > 0.3) drawLightning(offset + w, offset, offset + w, offset + h, intensity);
                if(Math.random() > 0.3) drawLightning(offset + w, offset + h, offset, offset + h, intensity);
                if(Math.random() > 0.3) drawLightning(offset, offset + h, offset, offset, intensity);
            }}
        }}

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
            mainContainer.appendChild(star);
        }}
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=950, scrolling=True)

st.markdown("---")
st.subheader("⚙️ Quản lý nội dung trang Web (Admin Panel)")

col1, col2 = st.columns(2)

with col1:
    st.write("📝 **Cập nhật Ghi chú:**")
    new_note = st.text_area("Nhập nội dung ghi chú mới:", value=saved_note)
    if st.button("Lưu Ghi Chú"):
        with open(NOTE_FILE, "w", encoding="utf-8") as f:
            f.write(new_note)
        st.success("Đã lưu ghi chú vĩnh viễn!")
        st.rerun()

with col2:
    st.write("🖼️ **Thêm hình ảnh vào Bộ sưu tập:**")
    uploaded_files = st.file_uploader("Chọn ảnh cần tải lên:", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    if st.button("Tải Ảnh Lên Web"):
        if uploaded_files:
            for u_file in uploaded_files:
                save_path = os.path.join(IMAGE_DIR, u_file.name)
                with open(save_path, "wb") as f:
                    f.write(u_file.getbuffer())
            st.success("Đã tải ảnh lên và lưu vĩnh viễn!")
            st.rerun()
