# -*- coding: utf-8 -*-
import streamlit as st
import base64
import os

st.set_page_config(page_title="Profile Của Tôi", page_icon="🔴", layout="wide")

NOTE_FILE = "data_notes.txt"
IMAGE_DIR = "uploaded_images"

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
        let phase = 0;

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
                analyser.fftSize = 256; 
                dataArray = new Uint8Array(analyser.frequencyBinCount);
                visualize();
            }}
        }};

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

        // Hàm vẽ đường sóng mềm mại dựa trên Bezier Curves
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
            if (!analyser) return;
            requestAnimationFrame(visualize);
            analyser.getByteFrequencyData(dataArray);

            phase += 0.08;
            let sum = 0; 
            for(let i = 0; i < 20; i++) sum += dataArray[i];
            let avg = sum / 20;

            let glow = 30 + (avg / 2);
            mainContainer.style.boxShadow = `0 0 ${{glow}}px rgba(255, 0, 0, ${{0.5 + avg/200}})`;

            vCtx.clearRect(0, 0, vCanvas.width, vCanvas.height);

            const offset = 40;
            const w = vCanvas.width - offset * 2;
            const h = vCanvas.height - offset * 2;
            const len = 32; // Số điểm sóng

            let topPts = [], botPts = [], leftPts = [], rightPts = [];

            for (let i = 0; i <= len; i++) {{
                let freq = dataArray[i % dataArray.length] / 255.0;
                let amp = freq * 45 + Math.sin(phase + i * 0.3) * 8; 

                // Viền Trên (Top Wave)
                topPts.push({{ x: offset + (i / len) * w, y: offset - amp }});
                // Viền Dưới (Bottom Wave)
                botPts.push({{ x: offset + (i / len) * w, y: offset + h + amp }});
                // Viền Trái (Left Wave)
                leftPts.push({{ x: offset - amp, y: offset + (i / len) * h }});
                // Viền Phải (Right Wave)
                rightPts.push({{ x: offset + w + amp, y: offset + (i / len) * h }});
            }}

            // Vẽ dải sóng chính sáng ngời
            drawCurvedWave(topPts, '#ff0000', 3, 20);
            drawCurvedWave(botPts, '#ff0000', 3, 20);
            drawCurvedWave(leftPts, '#ff0000', 3, 20);
            drawCurvedWave(rightPts, '#ff0000', 3, 20);

            // Vẽ lớp sóng mờ phụ phía sau tạo hiệu ứng chiều sâu (Cyber Motion Blur)
            let topPtsSub = topPts.map(p => ({{ x: p.x, y: p.y - 6 }}));
            let botPtsSub = botPts.map(p => ({{ x: p.x, y: p.y + 6 }}));
            drawCurvedWave(topPtsSub, 'rgba(255, 50, 50, 0.4)', 1.5, 10);
            drawCurvedWave(botPtsSub, 'rgba(255, 50, 50, 0.4)', 1.5, 10);

            // Bật tia sét khi gặp nhịp Bass dồn
            if(avg > 135) {{
                let intensity = (avg - 135) / 120;
                if(Math.random() > 0.25) drawLightning(offset, offset, offset + w, offset, intensity);
                if(Math.random() > 0.25) drawLightning(offset + w, offset, offset + w, offset + h, intensity);
                if(Math.random() > 0.25) drawLightning(offset + w, offset + h, offset, offset + h, intensity);
                if(Math.random() > 0.25) drawLightning(offset, offset + h, offset, offset, intensity);
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

# --- KHU VỰC ADMIN CHỈ HIỆN KHI CÓ URL BÍ MẬT ---
if is_admin:
    st.sidebar.title("👑 Chế độ Admin")
    st.sidebar.success("Đã mở khóa quyền quản trị!")
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Quản lý nội dung")

    new_note = st.sidebar.text_area("Cập nhật ghi chú mới:", value=saved_note)
    if st.sidebar.button("Lưu Ghi Chú"):
        with open(NOTE_FILE, "w", encoding="utf-8") as f:
            f.write(new_note)
        st.sidebar.success("Đã cập nhật ghi chú!")
        st.rerun()

    st.sidebar.markdown("---")

    uploaded_files = st.sidebar.file_uploader("Thêm ảnh vào bộ sưu tập:", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    if st.sidebar.button("Tải Ảnh Lên"):
        if uploaded_files:
            for u_file in uploaded_files:
                save_path = os.path.join(IMAGE_DIR, u_file.name)
                with open(save_path, "wb") as f:
                    f.write(u_file.getbuffer())
            st.sidebar.success("Đã đăng tải ảnh!")
            st.rerun()
