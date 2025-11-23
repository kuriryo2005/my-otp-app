import streamlit as st
import pyotp
import time
import base64
import os

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

# ==========================================
# 🔊 AUDIO ENGINE (Base64 Embedding)
# ==========================================
def get_audio_html(file_name):
    if not os.path.exists(file_name):
        return ""
    
    # ファイルをバイナリとして読み込んでBase64化
    with open(file_name, "rb") as f:
        b64_audio = base64.b64encode(f.read()).decode()
    
    return f"""
    <audio id="bgm-player" loop>
        <source src="data:audio/mpeg;base64,{b64_audio}" type="audio/mpeg">
    </audio>
    
    <div id="fab-btn" class="sound-fab">
        <div id="fab-icon">{ICON_PLAY}</div>
    </div>

    <script>
    // Streamlitの再描画に強いイベントリスナー設定
    (function() {{
        var audio = document.getElementById("bgm-player");
        var btn = document.getElementById("fab-btn");
        var iconBox = document.getElementById("fab-icon");
        var isPlaying = false;
        
        var svgPlay = `{ICON_PLAY}`; 
        var svgPause = `{ICON_PAUSE}`;

        if(btn) {{
            btn.addEventListener("click", function() {{
                if (isPlaying) {{
                    audio.pause();
                    iconBox.innerHTML = svgPlay;
                    btn.classList.remove("is-active");
                    isPlaying = false;
                }} else {{
                    audio.volume = 0.4;
                    audio.play().then(() => {{
                        iconBox.innerHTML = svgPause;
                        btn.classList.add("is-active");
                        isPlaying = true;
                    }}).catch(e => {{
                        alert("再生エラー: " + e.message);
                    }});
                }}
            }});
        }}
    }})();
    </script>
    """


# ==========================================
# 🎨 CSS STYLES
# ==========================================
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=SF+Pro+Display&display=swap');

.stApp { background-color: #000; background: #050507; color: #f5f5f7; font-family: "SF Pro Display", sans-serif; overflow-x: hidden; }
header, footer { visibility: hidden; }
.block-container { padding-top: 4rem; padding-bottom: 10rem; max-width: 1000px; }

@keyframes floatUp { 
    0% { opacity: 0; transform: translateY(40px); } 
    100% { opacity: 1; transform: translateY(0); } 
}
@keyframes pulseGreen { 
    0% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7); } 
    70% { box-shadow: 0 0 0 15px rgba(46, 204, 113, 0); } 
    100% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); } 
}

.sound-fab {
    position: fixed; bottom: 40px; right: 40px; width: 64px; height: 64px;
    background: rgba(40, 40, 40, 0.8); backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; z-index: 2147483647; color: #fff; 
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.sound-fab:hover { transform: scale(1.1); background: rgba(60, 60, 60, 0.9); }
.sound-fab.is-active {
    background: #2ecc71; color: #000; border-color: #2ecc71;
    animation: pulseGreen 2s infinite;
}

.hero-section { 
    text-align: center; margin-bottom: 120px; padding: 60px 20px; 
    animation: floatUp 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}
.otp-display { 
    font-size: 160px; font-weight: 700; letter-spacing: -6px; margin: 20px 0; 
    background: linear-gradient(135deg, #fff 0%, #8a8a8e 100%); 
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    color: #e0e0e0; 
}

.section-header { margin-top: 80px; margin-bottom: 60px; padding: 0 20px; opacity: 0; animation: floatUp 1s cubic-bezier(0.2, 0.8, 0.2, 1) 0.3s forwards; }
.text-headline { font-size: 56px; font-weight: 600; margin-bottom: 20px; }
.text-subhead { font-size: 28px; color: #86868b; }
.bento-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; padding: 0 20px; }
.bento-card { 
    background: #101010; border-radius: 30px; padding: 40px 36px; height: 450px; 
    display: flex; flex-direction: column; justify-content: space-between; 
    border: 1px solid #1d1d1f; opacity: 0; 
    animation: floatUp 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}
.bento-card:hover { transform: scale(1.02); background: #151515; border-color: #333; }
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
    
    audio_html = get_audio_html("bgm.mp3")
    
    return f"""
    {audio_html}
    <div class="section-header"><div class="text-headline">Engineering Intelligence.</div><div class="text-subhead">機械工学科のための<br>究極のサバイバルツール。</div></div><div class="bento-grid">{cards_html}</div><div style="text-align:center; padding: 100px 0; color: #444; font-size: 12px;">Designed in Yokohama.</div>
    """

def main():
    st.set_page_config(page_title="Engineering Tools", page_icon="📐", layout="wide")
    st.markdown(STYLES, unsafe_allow_html=True)
    st.markdown(get_static_content(), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
