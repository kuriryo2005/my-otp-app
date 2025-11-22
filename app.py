import streamlit as st
import pyotp
import time
import base64

# ==========================================
# ⚙️ SETTINGS
# ==========================================
try:
    TEAM_SECRET_KEY = st.secrets["TEAM_SECRET_KEY"]
except FileNotFoundError:
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
# 🎨 CSS & JS ENGINE
# ==========================================
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=SF+Pro+Display&display=swap');

/* Global */
.stApp { background-color: #000; background: #050507; color: #f5f5f7; font-family: "SF Pro Display", sans-serif; overflow-x: hidden; }
header, footer { visibility: hidden; }
.block-container { padding-top: 4rem; padding-bottom: 10rem; max-width: 1000px; }

/* Animations */
/* JSがクラスをつけるまで隠しておく */
.reveal-on-scroll {
    opacity: 0;
    transform: translateY(50px);
    transition: all 1.0s cubic-bezier(0.16, 1, 0.3, 1);
}
/* JSがこのクラスをつけたら表示される */
.reveal-on-scroll.is-visible {
    opacity: 1;
    transform: translateY(0);
}

/* Hero Section */
.hero-section { text-align: center; margin-bottom: 150px; padding: 60px 20px; }
.otp-display { 
    font-size: 160px; font-weight: 700; letter-spacing: -6px; margin: 20px 0; 
    background: linear-gradient(135deg, #fff 0%, #8a8a8e 100%); 
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.progress-container { width: 240px; height: 4px; background: #333; margin: 40px auto; border-radius: 2px; overflow: hidden; }
.progress-fill { height: 100%; background: #fff; transition: width 1s linear; }
.warning { background: #ff453a !important; }

/* Bento Grid */
.section-header { margin-top: 100px; margin-bottom: 60px; padding: 0 20px; }
.text-headline { font-size: 56px; font-weight: 600; margin-bottom: 20px; }
.text-subhead { font-size: 28px; color: #86868b; }

.bento-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; padding: 0 20px; }
.bento-card { 
    background: #101010; border-radius: 30px; padding: 40px 36px; height: 450px; 
    display: flex; flex-direction: column; justify-content: space-between; 
    border: 1px solid #1d1d1f;
}
.bento-card:hover { transform: scale(1.02); background: #151515; border-color: #333; transition: transform 0.3s ease; }

.card-icon-box { width: 60px; height: 60px; margin-bottom: 25px; background: rgba(255,255,255,0.05); border-radius: 16px; display: flex; align-items: center; justify-content: center; }
.card-icon-box svg { width: 32px; height: 32px; }
.card-title { font-size: 28px; font-weight: 700; color: #f5f5f7; margin-bottom: 12px; }
.card-desc { font-size: 17px; line-height: 1.5; color: #86868b; }
.card-cmd { margin-top: auto; font-family: monospace; font-size: 13px; color: #fff; background: rgba(255,255,255,0.1); padding: 16px; border-radius: 16px; }
</style>

<script>
// Streamlitの再描画タイミングでも確実に動くようにするObserver
function setupObserver() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, { threshold: 0.15 });

    // 監視対象を見つける
    const targets = document.querySelectorAll('.reveal-on-scroll');
    targets.forEach((el) => observer.observe(el));
}

// 初回実行
setupObserver();

// Streamlitの画面更新時にも再実行するハック
window.addEventListener('load', setupObserver);
</script>
"""

# ==========================================
# 🧱 COMPONENTS
# ==========================================
def create_card(svg_icon, title, desc, cmd):
    # クラスに 'reveal-on-scroll' を追加して、初期状態を透明にする
    return f"""<div class="bento-card reveal-on-scroll"><div><div class="card-icon-box">{svg_icon}</div><div class="card-title">{title}</div><div class="card-desc">{desc}</div></div><div class="card-cmd">"{cmd}"</div></div>"""

def get_static_content():
    cards = [
        create_card(ICON_MATH, "Math Vision", "板書の数式を、一瞬でLaTeXに。", "この画像をLaTeXにして"),
        create_card(ICON_GRAPH, "Graph Reverse", "論文のグラフから、データを復元。", "このグラフをCSVにして"),
        create_card(ICON_CODE, "Polyglot", "MATLABを、Pythonへ。", "Pythonに書き換えて"),
        create_card(ICON_ERROR, "Error Analysis", "誤差伝播を、自動計算。", "誤差伝播を計算して"),
        create_card(ICON_DIMENSION, "Dimensions", "物理式の整合性を、検算。", "次元解析をして"),
        create_card(ICON_POLISH, "Refine", "文章を、論文のクオリティへ。", "学術的にリライトして")
    ]
    
    cards_html = "".join(cards)
    
    # ヘッダーにも 'reveal-on-scroll' をつける
    return f"""<div class="section-header reveal-on-scroll"><div class="text-headline">Engineering Intelligence.</div><div class="text-subhead">機械工学科のための<br>究極のサバイバルツール。</div></div><div class="bento-grid">{cards_html}</div><div style="text-align:center; padding: 100px 0; color: #444; font-size: 12px;">Designed in Yokohama.</div>"""

def get_hero_content(code, progress, bar_class, remaining):
    # ヒーローセクションは最初から見えていてほしいので 'reveal-on-scroll' はつけない（または別のアニメーションにする）
    # ここではフェードインだけCSSでかける
    return f"""<div class="hero-section" style="animation: fadeIn 1.5s ease forwards;"><div style="font-size: 14px; font-weight: 600; letter-spacing: 0.2em; color: #d59464; margin-bottom: 10px;">TITANIUM SECURITY</div><div class="otp-display">{code}</div><div class="progress-container"><div class="progress-fill {bar_class}" style="width: {progress}%;"></div></div><div style="color: #666; font-size: 14px; font-weight: 500;">Updating in <span style="color: #fff;">{remaining}</span>s</div></div>"""

# ==========================================
# 🚀 MAIN APP
# ==========================================
def main():
    st.set_page_config(page_title="iPhone 17 Pro Auth", page_icon="", layout="wide")
    
    # JSを含むスタイルを注入 (unsafe_allow_html=Trueが必須)
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