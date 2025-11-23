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
# 🔊 AUDIO COMPONENT (Modified for Top Position)
# ==========================================
def render_audio_player(file_name):
    # ファイルがない場合のダミー処理（エラー回避）
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
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 0, 0, 0.1);
            color: #333; cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-right: 10px;
        }}
        .audio-btn:hover {{ transform: scale(1.1); background: #fff; }}
        .audio-btn.playing {{
            background: #007aff; border-color: #007aff; color: #fff;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{ 
            0% {{ box-shadow: 0 0 0 0 rgba(0, 122, 255, 0.4); }} 
            70% {{ box-shadow: 0 0 0 10px rgba(0, 122, 255, 0); }} 
            100% {{ box-shadow: 0 0 0 0 rgba(0, 122, 255, 0); }} 
        }}
        svg {{ width: 20px; height: 20px; }}
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
    components.html(html_code, height=80)

# ==========================================
# 🎨 MAIN CSS & HTML CONTENT (Middle)
# ==========================================
# ここに前回のWebサイトのデザイン（Bento Grid含む）が入ります
MAIN_SITE_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Noto Sans JP', sans-serif;
            background-color: #f5f5f7;
            color: #1d1d1f;
            overflow-x: hidden;
            margin: 0; padding: 0;
        }
        .reveal {
            opacity: 0; transform: translateY(50px);
            transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .reveal.active { opacity: 1; transform: translateY(0); }
        .text-gradient {
            background: linear-gradient(90deg, #007aff, #a855f7);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
    </style>
</head>
<body>
    <section class="min-h-screen flex flex-col justify-center items-center text-center px-6 pt-20">
        <div class="reveal active space-y-6 max-w-4xl">
            <h2 class="text-2xl md:text-4xl font-bold text-gray-500">工学部の学びを、<br class="md:hidden">もっと自由に。</h2>
            <h1 class="text-5xl md:text-8xl font-black tracking-tighter leading-tight">
                あなたの第2の脳。<br><span class="text-gradient">ChatGPT</span>
            </h1>
        </div>
        <div class="mt-16 w-full max-w-5xl reveal">
            <div class="relative aspect-video bg-gradient-to-br from-gray-100 to-gray-200 rounded-3xl shadow-2xl overflow-hidden flex items-center justify-center border border-white">
                <div class="text-center space-y-4">
                    <div class="text-9xl">🤖 ⚡️ ⚙️</div>
                    <p class="text-gray-400 font-bold tracking-widest uppercase">Engineering Intelligence</p>
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
                <div class="md:col-span-2 md:row-span-2 bg-white rounded-3xl p-8 shadow-sm hover:shadow-xl transition duration-500 reveal flex flex-col justify-between overflow-hidden relative">
                    <div class="z-10">
                        <h3 class="text-3xl font-bold mb-2">難解な論文も、<br>3行で要約。</h3>
                        <p class="text-gray-600 mt-4 max-w-md">英語の論文PDFをアップロード。「この論文の結論と、実験条件の限界を教えて」と聞くだけ。</p>
                    </div>
                    <div class="absolute bottom-[-50px] right-[-50px] w-80 h-80 bg-blue-100 rounded-full blur-3xl opacity-50"></div>
                </div>
                <div class="bg-white rounded-3xl p-8 shadow-sm hover:shadow-xl transition duration-500 reveal flex flex-col justify-center items-center text-center">
                    <div class="text-5xl mb-4">🔬</div>
                    <h3 class="text-xl font-bold">レポート支援</h3>
                </div>
                <div class="bg-black text-white rounded-3xl p-8 shadow-sm hover:shadow-xl transition duration-500 reveal flex flex-col justify-between">
                    <div>
                        <h3 class="text-xl font-bold text-purple-400">Code Assistant</h3>
                        <p class="text-sm text-gray-400 mt-2">Python, MATLABのエラー修正。</p>
                    </div>
                </div>
                <div class="md:col-span-3 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-3xl p-10 text-white shadow-lg reveal flex items-center justify-between">
                    <div><h3 class="text-3xl font-bold">アイデア出しの壁打ち相手。</h3></div>
                </div>
            </div>
        </div>
    </section>
    
    <script>
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) entry.target.classList.add('active');
            });
        }, { threshold: 0.1 });
        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
    </script>
</body>
</html>
"""

# ==========================================
# 🔐 OTP HTML GENERATOR (Bottom)
# ==========================================
def get_otp_html(code, progress, bar_class, remaining):
    # デザインをWebサイトのライトテーマに合わせて調整
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@700&display=swap');
        .hero-section {{
            text-align: center;
            padding: 60px 20px 100px 20px;
            background: #fff;
            border-top: 1px solid #eaeaea;
        }}
        .otp-display {{
            font-family: 'SF Pro Display', sans-serif;
            font-size: 120px;
            font-weight: 700;
            letter-spacing: -4px;
            margin: 10px 0;
            background: linear-gradient(135deg, #1d1d1f 0%, #4a4a4a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .otp-label {{
            font-size: 14px;
            font-weight: 600;
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
    <div class="hero-section">
        <div class="otp-label">Secure Access</div>
        <div class="otp-display">{code}</div>
        <div class="progress-container">
            <div class="progress-fill {bar_class}" style="width: {progress}%;"></div>
        </div>
        <div style="color: #86868b; font-size: 14px;">
            Updating in <span style="color: #1d1d1f; font-weight:bold;">{remaining}</span>s
        </div>
    </div>
    """

# ==========================================
# 🚀 MAIN APP EXECUTION
# ==========================================
def main():
    # 1. 音楽プレイヤーCSSの適用（右上に固定）
    st.markdown("""
    <style>
        /* 音楽プレイヤーを右上に固定 */
        iframe[title="streamlit.components.v1.html"] {
            position: fixed !important;
            top: 20px !important;
            right: 20px !important;
            width: 80px !important;
            height: 80px !important;
            z-index: 9999 !important;
            border: none !important;
        }
        /* Streamlitのデフォルト余白を消す */
        .block-container { padding-top: 0rem; padding-bottom: 0rem; max-width: 100%; }
    </style>
    """, unsafe_allow_html=True)

    # 2. 音楽プレイヤーのレンダリング (bgm.mp3が必要)
    render_audio_player("bgm.mp3")

    # 3. メインWebサイトコンテンツの表示 (スクロール可能エリア)
    components.html(MAIN_SITE_HTML, height=2100, scrolling=False)

    # 4. OTPセクション (一番下で動的に更新)
    otp_placeholder = st.empty()

    try:
        totp = pyotp.TOTP(TEAM_SECRET_KEY)
        while True:
            current_code = totp.now()
            time_remaining = totp.interval - (time.time() % totp.interval)
            progress_percent = (time_remaining / 30.0) * 100
            
            # コードを見やすく整形 (123 456)
            display_code = f"{current_code[:3]} {current_code[3:]}"
            bar_class = "warning" if time_remaining <= 5 else ""
            
            # OTP部分のみを更新
            otp_placeholder.markdown(
                get_otp_html(display_code, progress_percent, bar_class, int(time_remaining)),
                unsafe_allow_html=True
            )
            time.sleep(0.1)

    except Exception as e:
        st.error(f"System Error: {e}")

if __name__ == "__main__":
    main()