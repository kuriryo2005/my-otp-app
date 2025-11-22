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
except FileNotFoundError:
    TEAM_SECRET_KEY = "ARHXCWTVFU54ITHIXS4Q76SVCDFLC5TU"

# ==========================================
# 🖼️ IMAGE LOADER (Base64 Encoder)
# ==========================================
def get_image_base64(path):
    """ローカル画像をBase64文字列に変換してHTMLに埋め込めるようにする関数"""
    if not os.path.exists(path):
        # ファイルがない場合のダミー（赤い四角）
        return "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjZmY0NTNhIi8+PC9zdmc+"
    
    with open(path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    
    # 拡張子に応じてMIMEタイプを判定
    ext = path.split('.')[-1].lower()
    mime_type = "image/png" if ext == "png" else "image/jpeg"
    
    return f"data:{mime_type};base64,{encoded}"

# ==========================================
# 🎨 CSS STYLES (Apple Pro Design System)
# ==========================================
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=SF+Pro+Display&display=swap');

/* --- 1. Global Reset --- */
.stApp {
    background-color: #000000;
    background: #050507; /* iPhone Pro Black */
    color: #f5f5f7;
    font-family: "SF Pro Display", -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
    overflow-x: hidden;
}
header, footer {visibility: hidden;}
.block-container { 
    padding-top: 4rem; 
    padding-bottom: 10rem; 
    max-width: 1000px; 
}

/* --- 2. Typography --- */
.text-headline {
    font-size: 56px; line-height: 1.07; font-weight: 600;
    letter-spacing: -0.005em; margin-bottom: 20px;
}
.text-subhead {
    font-size: 28px; line-height: 1.14; font-weight: 600;
    color: #86868b; margin-bottom: 50px;
}

/* --- 3. Hero Section --- */
.hero-section {
    text-align: center; margin-bottom: 150px; padding: 60px 20px;
    animation: fadeIn 1.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}
.otp-display {
    font-size: 160px; line-height: 1; font-weight: 700; letter-spacing: -6px;
    font-variant-numeric: tabular-nums; margin: 20px 0;
    background: linear-gradient(135deg, #fff 0%, #d0d0d0 40%, #8a8a8e 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 30px rgba(255,255,255,0.1));
}
.otp-label {
    font-size: 14px; font-weight: 600; letter-spacing: 0.2em;
    text-transform: uppercase; color: #d59464; margin-bottom: 10px;
}
.progress-container {
    width: 240px; height: 4px; background: #333;
    border-radius: 2px; margin: 40px auto; overflow: hidden;
}
.progress-fill {
    height: 100%; background: #fff;
    border-radius: 2px; transition: width 1s linear;
}
.warning { background: #ff453a !important; }

/* --- 4. Bento Grid & Images --- */
.section-header {
    margin-top: 100px; margin-bottom: 60px; padding: 0 20px;
    opacity: 0; transform: translateY(50px);
    transition: all 1.0s cubic-bezier(0.16, 1, 0.3, 1);
}
.bento-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 24px; padding: 0 20px;
}
.bento-card {
    background: #101010; border-radius: 30px; padding: 40px 36px;
    height: 500px; display: flex; flex-direction: column;
    justify-content: space-between; border: 1px solid #1d1d1f;
    overflow: hidden; position: relative;
    opacity: 0; transform: translateY(50px);
    transition: all 1.0s cubic-bezier(0.16, 1, 0.3, 1);
}
.bento-card:hover { transform: scale(1.02); background: #151515; }

/* 画像コンテナのスタイル調整 */
.card-icon-container {
    width: 80px;  /* アイコンの枠サイズ */
    height: 80px;
    margin-bottom: 25px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
}
/* 実際の画像のスタイル */
.card-image {
    width: auto;
    height: 100%; /* 高さを枠に合わせる */
    max-width: 100%; /* 幅ははみ出さない */
    object-fit: contain; /* アスペクト比を維持して収める */
    border-radius: 12px; /* 少し角丸に */
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2)); /* 僅かな影で浮遊感 */
}

.card-title {
    font-size: 32px; font-weight: 700; line-height: 1.1;
    color: #f5f5f7; margin-bottom: 12px;
}
.card-desc {
    font-size: 19px; line-height: 1.4; color: #86868b; font-weight: 500;
}
.card-cmd {
    margin-top: auto; font-family: 'SF Mono', monospace; font-size: 13px;
    color: #fff; background: rgba(255,255,255,0.1);
    padding: 16px; border-radius: 16px; backdrop-filter: blur(10px);
}

.is-visible { opacity: 1 !important; transform: translateY(0) !important; }
@keyframes fadeIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
</style>
"""

# ==========================================
# 📜 JAVASCRIPT (Scroll Observer)
# ==========================================
SCROLL_JS = """
<script>
document.addEventListener('DOMContentLoaded', function () {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, { threshold: 0.15 });
    const targets = document.querySelectorAll('.section-header, .bento-card');
    targets.forEach((el) => observer.observe(el));
});
</script>
"""

# ==========================================
# 🧱 HTML COMPONENTS
# ==========================================
def create_bento_card(image_path, title, desc, cmd):
    # 画像をBase64文字列に変換
    img_src = get_image_base64(image_path)
    
    return f"""
    <div class="bento-card">
        <div>
            <div class="card-icon-container">
                <img src="{img_src}" class="card-image" alt="icon">
            </div>
            <div class="card-title">{title}</div>
            <div class="card-desc">{desc}</div>
        </div>
        <div class="card-cmd">"{cmd}"</div>
    </div>
    """

def get_static_content():
    # ここで画像ファイル名を指定します
    cards = [
        # LaTeXロゴ
        create_bento_card("icon_latex.png", "Math Vision.", "板書の数式を、一瞬でLaTeXに。", "この画像をLaTeXにして"),
        # グラフの画像
        create_bento_card("icon_graph.png", "Graph Reverse.", "論文のグラフから、データを復元。", "このグラフをCSVにして"),
        # Javaコードの画像（Polyglotの象徴として）
        create_bento_card("icon_code.png", "Polyglot.", "MATLABを、Pythonへ。", "Pythonに書き換えて"),
        # ダッシュボード/エラーの画像
        create_bento_card("icon_error.png", "Error Analysis.", "誤差伝播を、自動計算。", "誤差伝播を計算して"),
        # 図形の画像（次元解析）
        create_bento_card("icon_dimension.png", "Dimensions.", "物理式の整合性を、検算。", "次元解析をして"),
        # フローチャートの画像（推敲プロセス）
        create_bento_card("icon_polish.png", "Refine.", "文章を、論文のクオリティへ。", "学術的にリライトして")
    ]
    
    return f"""
    <div class="section-header">
        <div class="text-headline">Engineering Intelligence.</div>
        <div class="text-subhead">機械工学科のための<br>究極のサバイバルツール。</div>
    </div>
    <div class="bento-grid">
        {"".join(cards)}
    </div>
    <div style="text-align:center; padding: 100px 0; color: #444; font-size: 12px;">
        Designed in Yokohama.
    </div>
    {SCROLL_JS}
    """

def get_hero_content(code, progress, bar_class, remaining):
    return f"""
    <div class="hero-section">
        <div class="otp-label">TITANIUM SECURITY</div>
        <div class="otp-display">{code}</div>
        <div class="progress-container">
            <div class="progress-fill {bar_class}" style="width: {progress}%;"></div>
        </div>
        <div style="color: #666; font-size: 14px; font-weight: 500;">
            Updating in <span style="color: #fff;">{remaining}</span>s
        </div>
    </div>
    """

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
    # 静的コンテンツ（画像入りグリッド）を描画
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