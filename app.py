import streamlit as st
import pyotp
import time
import base64
import os
import io
from PIL import Image
import streamlit.components.v1 as components

# ==========================================
# ⚙️ SETTINGS & SECRETS
# ==========================================
try:
    TEAM_SECRET_KEY = st.secrets["TEAM_SECRET_KEY"]
except:
    TEAM_SECRET_KEY = "ARHXCWTVFU54ITHIXS4Q76SVCDFLC5TU"

st.set_page_config(
    page_title="GenAI for Engineers",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 🖼️ IMAGE HELPER (Memory Safe)
# ==========================================
def get_img_tag(file_path, class_name="", max_width=600):
    """
    画像を読み込み、HTMLタグを返す。
    メモリ不足を防ぐため、PILでリサイズしてからBase64化する。
    """
    if not os.path.exists(file_path):
        return f'<div class="{class_name} bg-gray-200 flex items-center justify-center text-gray-500" style="min-height: 200px;">Image not found</div>'
    
    try:
        img = Image.open(file_path)
        # リサイズ処理 (アスペクト比維持)
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height))
        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG", optimize=True)
        data = base64.b64encode(buffered.getvalue()).decode()
        return f'<img src="data:image/png;base64,{data}" class="{class_name}" alt="Embedded Image">'
        
    except Exception:
        return f'<div class="{class_name} bg-red-50">Image Error</div>'

# ==========================================
# 🔊 AUDIO COMPONENT (Bottom Right)
# ==========================================
def render_audio_player(file_name):
    b64_audio = ""
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            b64_audio = base64.b64encode(f.read()).decode()
    
    ICON_PLAY = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="none"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>"""
    ICON_PAUSE = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="none"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>"""

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        /* コンテナ自体のスタイル: 右下に配置しやすいよう調整 */
        body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 80px; width: 80px; }}
        
        .audio-btn {{
            display: flex; align-items: center; justify-content: center;
            width: 56px; height: 56px; /* 少し大きめに */
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.8); /* ガラス感 */
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            color: #333; cursor: pointer;
            transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15); /* 浮遊感を強調 */
        }}
        .audio-btn:hover {{ 
            transform: translateY(-4px) scale(1.05); /* ホバーで少し浮く */
            background: #ffffff;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        }}
        .audio-btn.playing {{
            background: #007aff; border-color: #007aff; color: #fff;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(0, 122, 255, 0.6); }} 70% {{ box-shadow: 0 0 0 16px rgba(0, 122, 255, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(0, 122, 255, 0); }} }}
        svg {{ width: 24px; height: 24px; }}
    </style>
    </head>
    <body>
        <audio id="player" loop><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>
        <div id="btn" class="audio-btn" onclick="toggle()">{ICON_PLAY}</div>
        <script>
            var audio = document.getElementById("player");
            var btn = document.getElementById("btn");
            var isPlaying = false;
            var svgPlay = `{ICON_PLAY}`;
            var svgPause = `{ICON_PAUSE}`;
            function toggle() {{
                if (isPlaying) {{ audio.pause(); btn.innerHTML = svgPlay; btn.classList.remove("playing"); isPlaying = false; }}
                else {{ audio.volume = 0.4; audio.play().then(() => {{ btn.innerHTML = svgPause; btn.classList.add("playing"); isPlaying = true; }}).catch(e => console.log(e)); }}
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=80)

# ==========================================
# 🎨 HTML GENERATOR (Full Content via f-string)
# ==========================================
def get_site_html(stress_img_tag, paper_img_tag):
    return f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatGPT for Engineering Students</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Sans JP', sans-serif;
            background-color: #f5f5f7;
            color: #1d1d1f;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
        }}
        .reveal {{ opacity: 0; transform: translateY(50px); transition: all 1s cubic-bezier(0.16, 1, 0.3, 1); }}
        .reveal.active {{ opacity: 1; transform: translateY(0); }}
        .scale-reveal {{ opacity: 0; transform: scale(0.95); transition: all 1s cubic-bezier(0.16, 1, 0.3, 1); }}
        .scale-reveal.active {{ opacity: 1; transform: scale(1); }}
        .text-gradient {{ background: linear-gradient(90deg, #007aff, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        section {{ box-sizing: border-box; }}
    </style>
</head>
<body>

    <nav class="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-gray-200 transition-all duration-300" id="navbar">
        <div class="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">
            <span class="font-bold text-lg tracking-tight">GenAI <span class="text-gray-500">for Engineers</span></span>
            <a href="#" class="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-medium hover:bg-blue-700 transition">使ってみる</a>
        </div>
    </nav>

    <section class="min-h-screen flex flex-col justify-center items-center text-center px-6 pt-20">
        <div class="reveal active space-y-6 max-w-4xl">
            <h2 class="text-2xl md:text-4xl font-bold text-gray-500">工学部の学びを、<br class="md:hidden">もっと自由に。</h2>
            <h1 class="text-5xl md:text-8xl font-black tracking-tighter leading-tight">
                あなたの第2の脳。<br>
                <span class="text-gradient">ChatGPT</span>
            </h1>
            <p class="text-xl md:text-2xl text-gray-600 mt-4 max-w-2xl mx-auto">
                実験データの解析から、難解な物理法則の理解まで。<br>
                機械工学科での日々を、劇的に加速させるパートナー。
            </p>
        </div>
        
        <div class="mt-16 w-full max-w-5xl scale-reveal">
            <div class="relative aspect-video bg-gradient-to-br from-gray-100 to-gray-200 rounded-3xl shadow-2xl overflow-hidden flex items-center justify-center border border-white">
                <div class="text-center space-y-4">
                    <div class="text-9xl">🤖 ⚡️ ⚙️</div>
                    <p class="text-gray-400 font-bold tracking-widest uppercase">Engineering Intelligence</p>
                </div>
                <div class="absolute top-10 left-10 bg-white p-4 rounded-2xl shadow-lg animate-bounce" style="animation-duration: 3s;">
                    <code class="text-sm text-blue-600 font-mono">import numpy as np</code>
                </div>
                <div class="absolute bottom-20 right-10 bg-white p-4 rounded-2xl shadow-lg animate-bounce" style="animation-duration: 4s;">
                    <span class="text-xl font-serif italic">F = ma</span>
                </div>
            </div>
        </div>
    </section>

    <section class="py-32 bg-white">
        <div class="max-w-5xl mx-auto px-6">
            <div class="grid md:grid-cols-2 gap-16 items-center">
                <div class="reveal">
                    <h3 class="text-sm font-bold text-blue-600 uppercase tracking-widest mb-2">データ解析・可視化</h3>
                    <h2 class="text-4xl md:text-5xl font-bold mb-6">実験データ、<br>一瞬でグラフに。</h2>
                    <p class="text-lg text-gray-600 leading-relaxed">
                        CSVファイルをアップロードするだけ。「このデータの散布図を描いて」「近似曲線を求めて」と頼めば、Pythonコードごと出力。単位の換算ミスも、次元解析のチェックも、もう心配いりません。
                    </p>
                </div>
                <div class="scale-reveal relative group">
                    <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
                    <div class="relative bg-gray-900 rounded-2xl p-6 shadow-2xl text-white font-mono text-sm overflow-hidden">
                        <div class="flex space-x-2 mb-4">
                            <div class="w-3 h-3 rounded-full bg-red-500"></div>
                            <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                            <div class="w-3 h-3 rounded-full bg-green-500"></div>
                        </div>
                        <p class="text-green-400"># User Input</p>
                        <p class="mb-4">応力-ひずみ線図を作成し、ヤング率を求めて。</p>
                        <p class="text-blue-400"># ChatGPT Output</p>
                        <p>import pandas as pd<br>import matplotlib.pyplot as plt<br>...</p>
                        
                        <div class="mt-4 bg-white rounded border border-gray-700 overflow-hidden">
                            {stress_img_tag}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="py-32 bg-[#f5f5f7]">
        <div class="max-w-6xl mx-auto px-6">
            <div class="text-center mb-20 reveal">
                <h2 class="text-4xl md:text-6xl font-bold">あらゆる課題を、<br>シンプルに解決。</h2>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 h-auto md:h-[800px]">
                
                <div class="md:col-span-2 md:row-span-2 bg-white rounded-3xl p-8 shadow-sm hover:shadow-xl transition duration-500 scale-reveal flex flex-col justify-between overflow-hidden relative">
                    <div class="z-10">
                        <h3 class="text-3xl font-bold mb-2">難解な論文も、<br>3行で要約。</h3>
                        <p class="text-gray-600 mt-4 max-w-md">
                            英語の論文PDFをアップロード。「この論文の結論と、実験条件の限界を教えて」と聞くだけで、要点を抽出。先行研究の調査時間を大幅に短縮します。
                        </p>
                    </div>
                    <div class="absolute bottom-[-50px] right-[-50px] w-80 h-80 bg-blue-100 rounded-full blur-3xl opacity-50"></div>
                    
                    {paper_img_tag}
                </div>

                <div class="bg-white rounded-3xl p-8 shadow-sm hover:shadow-xl transition duration-500 scale-reveal flex flex-col justify-center items-center text-center">
                    <div class="text-5xl mb-4">🔬</div>
                    <h3 class="text-xl font-bold">レポート作成支援</h3>
                    <p class="text-sm text-gray-500 mt-2">
                        「考察の切り口を提案して」<br>
                        ※コピペは厳禁。思考の補助輪として。
                    </p>
                </div>

                <div class="bg-black text-white rounded-3xl p-8 shadow-sm hover:shadow-xl transition duration-500 scale-reveal flex flex-col justify-between">
                    <div>
                        <h3 class="text-xl font-bold text-purple-400">Code Assistant</h3>
                        <p class="text-sm text-gray-400 mt-2">Arduino, Python, MATLAB.<br>エラーの原因を一瞬で特定。</p>
                    </div>
                    <div class="mt-4 bg-gray-800 p-3 rounded-lg text-xs font-mono text-green-400">
                        > Error fixed.
                    </div>
                </div>

                <div class="md:col-span-3 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-3xl p-10 text-white shadow-lg scale-reveal flex flex-col md:flex-row items-center justify-between">
                    <div class="mb-6 md:mb-0">
                        <h3 class="text-3xl font-bold">アイデア出しの壁打ち相手。</h3>
                        <p class="text-indigo-100 mt-2">設計課題のブレーンストーミングや、プレゼンの構成案まで。</p>
                    </div>
                    <button class="bg-white text-indigo-600 px-8 py-3 rounded-full font-bold hover:bg-opacity-90 transition shadow-lg">
                        プロンプトを見る
                    </button>
                </div>

            </div>
        </div>
    </section>

    <section class="py-32 bg-white text-center">
        <div class="max-w-4xl mx-auto px-6 reveal">
            <p class="text-gray-500 font-medium mb-4">圧倒的な効率化</p>
            <h2 class="text-5xl md:text-7xl font-bold mb-16">もう、<br>単純作業に時間を割かない。</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 text-center">
                <div>
                    <div class="text-6xl font-black text-blue-600 mb-2">50<span class="text-3xl">%</span></div>
                    <p class="text-gray-600 font-medium">プログラミング時間の短縮</p>
                </div>
                <div>
                    <div class="text-6xl font-black text-blue-600 mb-2">10<span class="text-3xl">x</span></div>
                    <p class="text-gray-600 font-medium">アイデアの創出数</p>
                </div>
                <div>
                    <div class="text-6xl font-black text-blue-600 mb-2">∞</div>
                    <p class="text-gray-600 font-medium">いつでも質問可能なTAとして</p>
                </div>
            </div>
        </div>
    </section>

    <section class="py-20 bg-[#f5f5f7]">
        <div class="max-w-4xl mx-auto px-6 text-center reveal">
            <h2 class="text-3xl md:text-4xl font-bold mb-8">さあ、エンジニアリングをアップデートしよう。</h2>
            <div class="flex flex-col md:flex-row justify-center gap-4">
                <a href="https://chat.openai.com" target="_blank" class="bg-blue-600 text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-blue-700 transition shadow-lg transform hover:scale-105 duration-200">
                    ChatGPTを開く
                </a>
                <a href="#" class="bg-white text-black border border-gray-300 px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-50 transition shadow-sm">
                    プロンプト集を見る
                </a>
            </div>
            <p class="mt-8 text-xs text-gray-400">
                ※ 生成AIの回答には誤りが含まれる可能性があります。工学的な問題解決においては、必ず教科書や信頼できる文献で裏付け（4点検算）を行ってください。
            </p>
        </div>
    </section>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const observerOptions = {{
                threshold: 0.1,
                rootMargin: "0px 0px -50px 0px"
            }};

            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.classList.add('active');
                    }}
                }});
            }}, observerOptions);

            const revealElements = document.querySelectorAll('.reveal, .scale-reveal');
            revealElements.forEach(el => observer.observe(el));
        }});
    </script>
</body>
</html>
"""

# ==========================================
# 🔐 OTP HTML GENERATOR (Bottom)
# ==========================================
def get_otp_html(code, progress, bar_class, remaining):
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@700&display=swap');
        .otp-section {{
            text-align: center;
            padding: 60px 20px 80px 20px;
            background: #ffffff;
            border-top: 1px solid #e5e5e5;
            font-family: 'SF Pro Display', sans-serif;
        }}
        .otp-display {{
            font-size: 100px;
            font-weight: 700;
            letter-spacing: -4px;
            margin: 10px 0;
            background: linear-gradient(135deg, #1d1d1f 0%, #4a4a4a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .otp-label {{
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 0.2em;
            color: #86868b;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        .progress-container {{
            width: 240px;
            height: 4px;
            background: #e5e5e5;
            margin: 30px auto;
            border-radius: 2px;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            background: #007aff;
            transition: width 1s linear;
        }}
        .warning {{ background: #ff453a !important; }}
    </style>
    <div class="otp-section">
        <div class="otp-label">Secure Access Token</div>
        <div class="otp-display">{code}</div>
        <div class="progress-container">
            <div class="progress-fill {bar_class}" style="width: {progress}%;"></div>
        </div>
        <div style="color: #86868b; font-size: 12px; font-weight: 500;">
            Code updates in <span style="color: #1d1d1f;">{remaining}</span>s
        </div>
    </div>
    """

# ==========================================
# 🚀 MAIN APP EXECUTION
# ==========================================
def main():
    # CSS Adjustments: 音楽プレイヤーを右下(bottom: 20px, right: 20px)に固定
    st.markdown("""
    <style>
        iframe[title="streamlit.components.v1.html"] {
            position: fixed !important;
            bottom: 20px !important;
            right: 20px !important;
            width: 80px !important;
            height: 80px !important;
            z-index: 9999 !important;
            border: none !important;
        }
        .block-container { padding-top: 0rem; padding-bottom: 0rem; max-width: 100%; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

    # 1. Audio Player (bgm.mp3)
    render_audio_player("bgm.mp3")

    # 2. Images (Resize & Encode)
    stress_img_tag = get_img_tag(
        "simwiki-stress-strain-shape-evolution.png.webp", 
        class_name="w-full h-auto object-cover opacity-90 hover:opacity-100 transition duration-300",
        max_width=600
    )
    
    paper_img_tag = get_img_tag(
        "papersumary.png", 
        class_name="mt-4 rounded-xl shadow-lg transform rotate-2 translate-y-4 hover:translate-y-2 transition duration-500 w-full object-cover border border-gray-100",
        max_width=600
    )

    # 3. HTML Construction (using f-string to prevent MemoryError)
    final_html = get_site_html(stress_img_tag, paper_img_tag)
    
    # Render Main Site
    components.html(final_html, height=3500, scrolling=True)

    # 4. OTP Loop
    otp_placeholder = st.empty()

    try:
        totp = pyotp.TOTP(TEAM_SECRET_KEY)
        while True:
            current_code = totp.now()
            time_remaining = totp.interval - (time.time() % totp.interval)
            progress_percent = (time_remaining / 30.0) * 100
            
            display_code = f"{current_code[:3]} {current_code[3:]}"
            bar_class = "warning" if time_remaining <= 5 else ""
            
            otp_placeholder.markdown(
                get_otp_html(display_code, progress_percent, bar_class, int(time_remaining)),
                unsafe_allow_html=True
            )
            time.sleep(0.1)

    except Exception as e:
        st.error(f"System Error: {e}")

if __name__ == "__main__":
    main()