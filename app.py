import streamlit as st
import pyotp
import time
import textwrap  # <--- これを追加！魔法のライブラリです

# ==========================================
# ⚙️ SETTINGS
# ==========================================
try:
    TEAM_SECRET_KEY = st.secrets["TEAM_SECRET_KEY"]
except FileNotFoundError:
    TEAM_SECRET_KEY = "ARHXCWTVFU54ITHIXS4Q76SVCDFLC5TU"
# ==========================================

st.set_page_config(page_title="Auth Pro", page_icon="", layout="wide")

# ---  Apple-style Design System ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&family=SF+Pro+Display&display=swap');

.stApp {
    background-color: #000;
    background: radial-gradient(circle at 50% 0%, #2c2c2e 0%, #000000 70%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #f5f5f7;
}

header, footer {visibility: hidden;}
.block-container { padding-top: 3rem; max-width: 960px; }

.hero-container {
    text-align: center;
    margin-bottom: 60px;
    padding: 40px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 30px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}

.hero-label {
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #86868b;
    margin-bottom: 10px;
}

.hero-code {
    font-size: 8rem;
    font-weight: 700;
    letter-spacing: -2px;
    margin: 10px 0;
    background: linear-gradient(180deg, #ffffff 0%, #86868b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-variant-numeric: tabular-nums;
    transition: all 0.3s ease;
}

.progress-wrapper {
    width: 60%;
    height: 6px;
    background: #333;
    border-radius: 10px;
    margin: 0 auto 20px auto;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background: #fff;
    border-radius: 10px;
    transition: width 1s linear;
    box-shadow: 0 0 15px rgba(255,255,255,0.3);
}

.warning-mode {
    background: #ff453a !important;
    box-shadow: 0 0 15px rgba(255, 69, 58, 0.5);
}

.tips-header {
    font-size: 2rem;
    font-weight: 700;
    margin-top: 60px;
    margin-bottom: 20px;
    text-align: center;
    background: linear-gradient(90deg, #fff, #86868b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.feature-card {
    background: #1c1c1e;
    border-radius: 20px;
    padding: 25px;
    height: 100%;
    transition: transform 0.3s ease;
    border: 1px solid #333;
}
.feature-card:hover {
    transform: scale(1.02);
    background: #2c2c2e;
    border-color: #fff;
}

.feature-icon { font-size: 2rem; margin-bottom: 15px; }
.feature-title { font-weight: 700; font-size: 1.1rem; color: #fff; margin-bottom: 8px; }
.feature-desc { font-size: 0.9rem; color: #86868b; line-height: 1.4; }
.feature-cmd {
    display: inline-block;
    margin-top: 10px;
    font-family: monospace;
    font-size: 0.8rem;
    color: #0a84ff;
    background: rgba(10, 132, 255, 0.1);
    padding: 4px 8px;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

def main():
    if not TEAM_SECRET_KEY or "ARHX" not in TEAM_SECRET_KEY:
        st.error("⚠️ TEAM_SECRET_KEY Error")
        return

    try:
        totp = pyotp.TOTP(TEAM_SECRET_KEY)
        main_placeholder = st.empty()
        
        while True:
            current_code = totp.now()
            time_remaining = totp.interval - (time.time() % totp.interval)
            progress_percent = (time_remaining / 30.0) * 100
            
            display_code = f"{current_code[:3]} {current_code[3:]}"
            bar_class = "progress-bar warning-mode" if time_remaining <= 5 else "progress-bar"
            
            # ★ここが修正ポイント！ textwrap.dedent で空白を除去します
            html = textwrap.dedent(f"""
            <div class="hero-container">
                <div class="hero-label">Shared Access Token</div>
                <div class="hero-code">{display_code}</div>
                <div class="progress-wrapper">
                    <div class="{bar_class}" style="width: {progress_percent}%;"></div>
                </div>
                <div style="color: #86868b; font-size: 0.8rem;">
                    Auto-refreshing in {int(time_remaining)}s
                </div>
            </div>
            
            <div class="tips-header">Campus Hacks</div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                <div class="feature-card">
                    <div class="feature-icon">📸</div>
                    <div class="feature-title">Math Vision</div>
                    <div class="feature-desc">手書き数式や教科書の写真を撮影してアップロード。一瞬でLaTeXコードに変換します。</div>
                    <div class="feature-cmd">Prompt: "これをLaTeXにして"</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">Graph Reverse</div>
                    <div class="feature-desc">論文のグラフ画像から、プロットデータ(CSV)を復元・抽出。実験データの比較検討に最適。</div>
                    <div class="feature-cmd">Prompt: "このグラフをCSVにして"</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⚙️</div>
                    <div class="feature-title">Code Converter</div>
                    <div class="feature-desc">授業のMATLABコードをPython(NumPy)へ移植。デバッグも同時に完了。</div>
                    <div class="feature-cmd">Prompt: "MATLABをPythonにして"</div>
                </div>
            </div>
            """)
            
            main_placeholder.markdown(html, unsafe_allow_html=True)
            time.sleep(0.1)

    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()