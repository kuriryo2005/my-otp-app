import streamlit as st
import pyotp
import time
import base64
import os
import mimetypes # ファイル形式を正確に判定するライブラリ

# ==========================================
# ⚙️ SETTINGS
# ==========================================
try:
    TEAM_SECRET_KEY = st.secrets["TEAM_SECRET_KEY"]
except:
    TEAM_SECRET_KEY = "ARHXCWTVFU54ITHIXS4Q76SVCDFLC5TU"

# ==========================================
# 💎 SVG ICONS
# ==========================================
ICON_MATH = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>"""
ICON_GRAPH = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>"""
ICON_CODE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>"""
ICON_ERROR = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>"""
ICON_DIMENSION = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>"""
ICON_POLISH = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#ec4899" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>"""

ICON_PLAY = """<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="currentColor" stroke="none"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>"""
ICON_PAUSE = """<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="currentColor" stroke="none"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>"""

# ==========================================
# 🔊 AUDIO SYSTEM (Absolute Path & MIME Check)
# ==========================================
def get_audio_html(file_name):
    # 現在のディレクトリからの絶対パスを取得（確実に見つけるため）
    abs_path = os.path.abspath(file_name)
    
    if not os.path.exists(abs_path):
        st.error(f"⚠️ サーバー上にファイルが見つかりません: {file_name}")
        return ""
    
    with open(abs_path, "rb") as f:
        audio_bytes = f.read()
    
    # ファイルサイズが小さすぎる場合は警告
    if len(audio_bytes) < 1000:
        st.warning("⚠️ 音楽ファイルのサイズが異常に小さいです（中身が壊れている可能性があります）")

    # 正しいMIMEタイプ（audio/mpegなど）を自動判定
    mime_type, _ = mimetypes.guess_type(abs_path)
    if mime_type is None: mime_type = "audio/mp3" # フォールバック

    b64_audio = base64.b64encode(audio_bytes).decode()
    
    return f"""
    <audio id="bgm-player" loop preload="auto">
        <source src="data:{mime_type};base64,{b64_audio}" type="{mime_type}">
    </audio>
    
    <div id="fab-btn" class="sound-fab">
        <div id="fab-icon">{ICON_PLAY}</div>
    </div>

    <script>
    (function() {{
        var audio = document.getElementById("bgm-player");
        var btn = document.getElementById("fab-btn");
        var iconBox = document.getElementById("fab-icon");
        var isPlaying = false;
        
        var svgPlay = `{ICON_PLAY}`;
        var svgPause = `{ICON_PAUSE}`;

        // グローバル変数で再生状態を保持（リロード対策）
        if(window.isGlobalPlaying) {{
            // 既に再生中なら状態を復元しない（二重再生防止のため今回はリセット）
        }}

        if(btn) {{
            btn.onclick = function() {{
                if (isPlaying) {{
                    audio.pause();
                    iconBox.innerHTML = svgPlay;
                    btn.classList.remove("is-active");
                    isPlaying = false;
                    window.isGlobalPlaying = false;
                }} else {{
                    // ユーザーアクションによる再生開始
                    audio.volume = 0.4;
                    var promise = audio.play();
                    
                    if (promise !== undefined) {{
                        promise.then(_ => {{
                            iconBox.innerHTML = svgPause;
                            btn.classList.add("is-active");
                            isPlaying = true;
                            window.isGlobalPlaying = true;
                        }}).catch(error => {{
                            alert("再生エラー: " + error);
                        }});
                    }}
                }}
            }};
        }}
    }})();
    </script>
    """

# ==========================================
# 🎨 CSS STYLES (Reliable Animation)
# ==========================================
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=SF+Pro+Display&display=swap');

/* --- Global --- */
.stApp { background-color: #000; background: #050507; color: #f5f5f7; font-family: "SF Pro Display", sans-serif; overflow-x: hidden; }
header, footer { visibility: hidden; }
.block-container { padding-top: 4rem; padding-bottom: 10rem; max-width: 1000px; }

/* --- Animation Keyframes --- */
@keyframes floatUp { 
    0% { opacity: 0; transform: translateY(40px); } 
    100% { opacity: 1; transform: translateY(0); } 
}
@keyframes pulseGreen { 
    0% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7); } 
    70% { box-shadow: 0 0 0 20px rgba(46, 204, 113, 0); } 
    100% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); } 
}

/* --- Sound FAB --- */
.sound-fab {
    position: fixed; bottom: 40px; right: 40px; width: 70px; height: 70px;
    background: rgba(30, 30, 30, 0.8); backdrop-filter: blur(15px);
    border: 2px solid rgba(255, 255, 255, 0.2); border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; z-index: 2147483647 !important; 
    color: #fff; transition: all 0.2s ease;
    box-shadow: 0 10px 40px rgba(0,0,0,0.6);
}
.sound-fab:hover { transform: scale(1.1); background: rgba(50, 50, 50, 0.9); border-color: #fff; }
.sound-fab:active { transform: scale(0.95); }
.sound-fab.is-active {
    background: #2ecc71; border-color: #27ae60; color: #000; 
    animation: pulseGreen 2s infinite;
}

/* --- Hero Section --- */
.hero-section { 
    text-align: center; margin-bottom: 120px; padding: 60px 20px; 
    /* ページを開いたら自動で浮き上がる */
    animation: floatUp 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}
.otp-display { font-size: 160px; font-weight: 700; letter-spacing: -6px; margin: 20px 0; background: linear-gradient(135deg, #fff 0%, #8a8a8e 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; color: #e0e0e0; }
.otp-label { font-size: 14px; font-weight: 600; letter-spacing: 0.2em; color: #d59464; margin-bottom: 10px; }
.progress-container { width: 240px; height: 4px; background: #333; margin: 40px auto; border-radius: 2px; overflow: hidden; }
.progress-fill { height: 100%; background: #fff; transition: width 1s linear; }
.warning { background: #ff453a !important; }

/* --- Grid Section --- */
.section-header { 
    margin-top: 80px; margin-bottom: 60px; padding: 0 20px; 
    opacity: 0; /* 初期は見えない */
    animation: floatUp 1s cubic-bezier(0.2, 0.8, 0.2, 1) 0.3s forwards; /* 遅れて登場 */
}
.text-headline { font-size: 56px; font-weight: 600; margin-bottom: 20px; }
.text-subhead { font-size: 28px; color: #86868b; }

.bento-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; padding: 0 20px; }

.bento-card { 
    background: #101010; border-radius: 30px; padding: 40px 36px; height: 450px; 
    display: flex; flex-direction: column; justify-content: space-between; 
    border: 1px solid #1d1d1f; 
    opacity: 0; /* 初期は見えない */
    animation: floatUp 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}
.bento-card:hover { transform: scale(1.02); background: #151515; border-color: #333; transition: transform 0.3s ease; }

/* Stagger Delays (カードが順番に出る) */
.delay-1 { animation-delay: 0.4s; } .delay-2 { animation-delay: 0.5s; } .delay-3 { animation-delay: 0.6s; }
.delay-4 { animation-delay: 0.7s; } .delay-5 { animation-delay: 0.8s; } .delay-6 { animation-delay: 0.9s; }

.card-icon-box { width: 60px; height: 60px; margin-bottom: 25px; background: rgba(255,255,255,0.05); border-radius: 16px; display: flex; align-items: center; justify-content: center; }
.card-icon-box svg { width: 32px; height: 32px; }
.card-title { font-size: 28px; font-weight: 700; color: #f5f5f7; margin-bottom: 12px; }
.card-desc { font-size: 17px; line-height: 1.5; color: #86868b; }
.card-cmd { margin-top: auto; font-family: monospace; font-size: 13px; color: #fff; background: rgba(255,255,255,0.1); padding: 16px; border-radius: 16px; }
</style>
"""

# ==========================================
# 🧱 COMPONENTS
# ==========================================
def create_card(svg_icon, title, desc, cmd, delay_class):
    return f"""<div class="bento-card {delay_class}"><div><div class="card-icon-box">{svg_icon}</div><div class="card-title">{title}</div><div class="card-desc">{desc}</div></div><div class="card-cmd">"{cmd}"</div></div>"""

def get_static_content():
    cards = [
        create_card(ICON_MATH, "Math Vision", "板書の数式を、一瞬でLaTeXに。", "この画像をLaTeXにして", "delay-1"),
        create_card(ICON_GRAPH, "Graph Reverse", "論文のグラフから、データを復元。", "このグラフをCSVにして", "delay-2"),
        create_card(ICON_CODE, "Polyglot", "MATLABを、Pythonへ。", "Pythonに書き換えて", "delay-3"),
        create_card(ICON_ERROR, "Error Analysis", "誤差伝播を、自動計算。", "誤差伝播を計算して", "delay-4"),
        create_card(ICON_DIMENSION, "Dimensions", "物理式の整合性を、検算。", "次元解析をして", "delay-5"),
        create_card(ICON_POLISH, "Refine", "文章を、論文のクオリティへ。", "学術的にリライトして", "delay-6")
    ]
    cards_html = "".join(cards)
    
    # オーディオシステム（ファイル名指定）
    audio_html = get_audio_html("bgm.mp3")
    
    return f"""
    {audio_html}
    <div class="section-header"><div class="text-headline">Engineering Intelligence.</div><div class="text-subhead">機械工学科のための<br>究極のサバイバルツール。</div></div><div class="bento-grid">{cards_html}</div><div style="text-align:center; padding: 100px 0; color: #444; font-size: 12px;">Designed in Yokohama.</div>
    """

def get_hero_content(code, progress, bar_class, remaining):
    return f"""<div class="hero-section"><div class="otp-label">TITANIUM SECURITY</div><div class="otp-display">{code}</div><div class="progress-container"><div class="progress-fill {bar_class}" style="width: {progress}%;"></div></div><div style="color: #666; font-size: 14px; font-weight: 500;">Updating in <span style="color: #fff;">{remaining}</span>s</div></div>"""

# ==========================================
# 🚀 MAIN APP
# ==========================================
def main():
    st.set_page_config(page_title="iPhone 17 Pro Auth", page_icon="", layout="wide")
    st.markdown(STYLES, unsafe_allow_html=True)

    if not TEAM_SECRET_KEY or "ARHX" not in TEAM_SECRET_KEY:
        st.error("⚠️ Secrets Error")
        return

    hero_placeholder = st.empty()
    st.markdown(get_static_content(), unsafe_allow_html=True)

    try:
        totp = pyotp.TOTP(TEAM_SECRET_KEY)
        while True:
            current_code = totp.now()
            time_remaining = totp.interval - (time.time() % totp.interval)
            progress_percent = (time_remaining / 30.0) * 100
            display_code = f"{current_code[:3]} {current_code[3:]}"
            bar_class = "warning" if time_remaining <= 5 else ""
            
            hero_placeholder.markdown(
                get_hero_content(display_code, progress_percent, bar_class, int(time_remaining)),
                unsafe_allow_html=True
            )
            time.sleep(0.1)

    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()