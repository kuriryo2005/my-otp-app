import streamlit as st
import pyotp
import time
import base64
import os
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
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 💎 SVG ICONS (From original code)
# ==========================================
# Apple風デザインに合わせて色味を微調整（視認性向上）
ICON_MATH = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#007aff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>"""
ICON_GRAPH = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#34c759" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>"""
ICON_CODE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>"""
ICON_ERROR = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#ff3b30" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>"""
ICON_DIMENSION = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#af52de" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>"""
ICON_POLISH = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#ff2d55" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>"""

# ==========================================
# 🔊 AUDIO COMPONENT (Top Right)
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
        body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; display: flex; justify-content: flex-end; align-items: center; height: 80px; }}
        .audio-btn {{
            display: flex; align-items: center; justify-content: center;
            width: 50px; height: 50px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 0, 0, 0.05);
            color: #1d1d1f; cursor: pointer;
            transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin-right: 20px;
        }}
        .audio-btn:hover {{ transform: scale(1.08); background: #ffffff; box-shadow: 0 8px 30px rgba(0,0,0,0.12); }}
        .audio-btn.playing {{
            background: #007aff; border-color: #007aff; color: #fff;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{ 
            0% {{ box-shadow: 0 0 0 0 rgba(0, 122, 255, 0.4); }} 
            70% {{ box-shadow: 0 0 0 10px rgba(0, 122, 255, 0); }} 
            100% {{ box-shadow: 0 0 0 0 rgba(0, 122, 255, 0); }} 
        }}
        svg {{ width: 18px; height: 18px; }}
    </style>
    </head>
    <body>
        <audio id="player" loop>
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        </audio>
        <div id="btn" class="audio-btn" onclick="toggle()">
            {ICON_PLAY}
        </div>
        <script>
            var audio = document.getElementById("player");
            var btn = document.getElementById("btn");
            var isPlaying = false;
            var svgPlay = `{ICON_PLAY}`;
            var svgPause = `{ICON_PAUSE}`;

            function toggle() {{
                if (isPlaying) {{
                    audio.pause();
                    btn.innerHTML = svgPlay;
                    btn.classList.remove("playing");
                    isPlaying = false;
                }} else {{
                    audio.volume = 0.4;
                    audio.play().then(() => {{
                        btn.innerHTML = svgPause;
                        btn.classList.add("playing");
                        isPlaying = true;
                    }}).catch(e => console.log(e));
                }}
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=100)

# ==========================================
# 🎨 MAIN CONTENT (Apple Design + Full Tips)
# ==========================================
# Tipsの内容をすべてHTML文字列に埋め込みます
MAIN_SITE_HTML = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Sans JP', sans-serif;
            background-color: #f5f5f7;
            color: #1d1d1f;
            overflow-x: hidden;
            margin: 0; padding: 0;
        }}
        .reveal {{
            opacity: 0; transform: translateY(40px);
            transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .reveal.active {{ opacity: 1; transform: translateY(0); }}
        
        .text-gradient {{
            background: linear-gradient(90deg, #007aff, #a855f7);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        
        /* カードのデザイン調整 */
        .bento-card {{
            background: #ffffff;
            border-radius: 24px;
            padding: 32px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 380px;
            border: 1px solid rgba(0,0,0,0.03);
        }}
        .bento-card:hover {{
            transform: scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        }}
        .icon-box svg {{ width: 40px; height: 40px; margin-bottom: 24px; }}
        
        /* プロンプトコマンドボックスのデザイン */
        .cmd-box {{
            background: #f5f5f7;
            color: #6e6e73;
            font-family: monospace;
            font-size: 13px;
            padding: 16px;
            border-radius: 12px;
            margin-top: auto;
            border: 1px solid #e5e5e5;
        }}
        .cmd-box::before {{
            content: "> ";
            color: #007aff;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <section class="min-h-screen flex flex-col justify-center items-center text-center px-6 pt-10 pb-20">
        <div class="reveal active space-y-6 max-w-4xl">
            <h2 class="text-xl md:text-3xl font-bold text-gray-400">Engineering Intelligence</h2>
            <h1 class="text-5xl md:text-8xl font-black tracking-tighter leading-tight">
                工学部のための、<br><span class="text-gradient">究極のサバイバルツール。</span>
            </h1>
            <p class="text-lg md:text-xl text-gray-600 mt-6 max-w-2xl mx-auto">
                実験、レポート、解析。すべてのプロセスを加速させる6つのTips。
            </p>
        </div>
    </section>

    <section class="py-20 bg-[#f5f5f7]">
        <div class="max-w-7xl mx-auto px-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                
                <div class="bento-card reveal">
                    <div>
                        <div class="icon-box">{ICON_MATH}</div>
                        <h3 class="text-2xl font-bold mb-2">Math Vision</h3>
                        <p class="text-gray-500 font-medium">板書の数式を、一瞬でLaTeXに。</p>
                    </div>
                    <div class="cmd-box">この画像をLaTeXにして</div>
                </div>

                <div class="bento-card reveal">
                    <div>
                        <div class="icon-box">{ICON_GRAPH}</div>
                        <h3 class="text-2xl font-bold mb-2">Graph Reverse</h3>
                        <p class="text-gray-500 font-medium">論文のグラフから、データを復元。</p>
                    </div>
                    <div class="cmd-box">このグラフをCSVにして</div>
                </div>

                <div class="bento-card reveal">
                    <div>
                        <div class="icon-box">{ICON_CODE}</div>
                        <h3 class="text-2xl font-bold mb-2">Polyglot</h3>
                        <p class="text-gray-500 font-medium">MATLABを、Pythonへ書き換え。</p>
                    </div>
                    <div class="cmd-box">Pythonに書き換えて</div>
                </div>

                <div class="bento-card reveal">
                    <div>
                        <div class="icon-box">{ICON_ERROR}</div>
                        <h3 class="text-2xl font-bold mb-2">Error Analysis</h3>
                        <p class="text-gray-500 font-medium">面倒な誤差伝播を、自動計算。</p>
                    </div>
                    <div class="cmd-box">誤差伝播を計算して</div>
                </div>

                <div class="bento-card reveal">
                    <div>
                        <div class="icon-box">{ICON_DIMENSION}</div>
                        <h3 class="text-2xl font-bold mb-2">Dimensions</h3>
                        <p class="text-gray-500 font-medium">物理式の次元整合性をチェック。</p>
                    </div>
                    <div class="cmd-box">次元解析をして</div>
                </div>

                <div class="bento-card reveal">
                    <div>
                        <div class="icon-box">{ICON_POLISH}</div>
                        <h3 class="text-2xl font-bold mb-2">Refine</h3>
                        <p class="text-gray-500 font-medium">レポートを論文クオリティへ。</p>
                    </div>
                    <div class="cmd-box">学術的にリライトして</div>
                </div>

            </div>
        </div>
    </section>
    
    <script>
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) entry.target.classList.add('active');
            }});
        }}, {{ threshold: 0.1 }});
        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
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
        .hero-section {{
            text-align: center;
            padding: 100px 20px 120px 20px;
            background: #fff;
            border-top: 1px solid #eaeaea;
        }}
        .otp-display {{
            font-family: 'SF Pro Display', sans-serif;
            font-size: 140px;
            font-weight: 700;
            letter-spacing: -6px;
            margin: 10px 0;
            background: linear-gradient(135deg, #1d1d1f 0%, #4a4a4a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.1;
        }}
        .otp-label {{
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 0.15em;
            color: #86868b;
            text-transform: uppercase;
            margin-bottom: 20px;
        }}
        .progress-container {{
            width: 200px;
            height: 6px;
            background: #f0f0f0;
            margin: 40px auto;
            border-radius: 3px;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            background: #007aff;
            transition: width 1s linear;
        }}
        .warning {{ background: #ff453a !important; }}
    </style>
    <div class="hero-section">
        <div class="otp-label">Secure Access</div>
        <div class="otp-display">{code}</div>
        <div class="progress-container">
            <div class="progress-fill {bar_class}" style="width: {progress}%;"></div>
        </div>
        <div style="color: #86868b; font-size: 14px; font-weight: 500;">
            Code updates in <span style="color: #1d1d1f;">{remaining}</span>s
        </div>
    </div>
    """

# ==========================================
# 🚀 MAIN APP EXECUTION
# ==========================================
def main():
    # 1. CSS調整 (Streamlitのデフォルト余白削除 & 音楽プレーヤー固定)
    st.markdown("""
    <style>
        iframe[title="streamlit.components.v1.html"] {
            position: fixed !important;
            top: 20px !important;
            right: 20px !important;
            width: 100px !important;
            height: 100px !important;
            z-index: 9999 !important;
            border: none !important;
        }
        .block-container { padding-top: 0rem; padding-bottom: 0rem; max-width: 100%; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

    # 2. 音楽プレーヤー
    render_audio_player("bgm.mp3")

    # 3. メインWebサイト（Tips含む）
    # Tipsが6つあるため、高さ(height)を少し広めに確保します
    components.html(MAIN_SITE_HTML, height=1800, scrolling=False)

    # 4. OTP (最下部で更新)
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