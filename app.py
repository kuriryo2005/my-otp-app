import streamlit as st
import pyotp
import time

# ==========================================
# 🔑 シークレットキー設定
# ==========================================
# ↓ クォーテーション "" で囲まれているか確認してください！
TEAM_SECRET_KEY = "ARHXCWTVFU54ITHIXS4Q76SVCDFLC5TU" 
# ==========================================

st.set_page_config(page_title="Flux Authenticator", page_icon="💎", layout="wide")

# --- 🎨 CSS Animations & Styles ---
# ここからデザイン設定（長いですが、途中で切らないように！）
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');

/* 背景アニメーション */
@keyframes gradient-bg {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 光の脈動アニメーション */
@keyframes glow-pulse {
    0% { text-shadow: 0 0 10px rgba(255,255,255,0.1); opacity: 0.9; }
    50% { text-shadow: 0 0 30px rgba(0, 243, 255, 0.6), 0 0 60px rgba(0, 243, 255, 0.4); opacity: 1; }
    100% { text-shadow: 0 0 10px rgba(255,255,255,0.1); opacity: 0.9; }
}

/* 全体設定 */
.stApp {
    background: linear-gradient(-45deg, #000000, #1a1a2e, #16213e, #0f3460);
    background-size: 400% 400%;
    animation: gradient-bg 15s ease infinite;
    color: #fff;
    font-family: 'Rajdhani', sans-serif;
    overflow: hidden;
}

header, footer {visibility: hidden;}
.block-container { padding-top: 10vh; max-width: 800px; }

/* カードデザイン */
.flux-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 30px;
    padding: 60px 20px;
    text-align: center;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    position: relative;
    overflow: hidden;
}

.label-text {
    font-size: 1.2rem;
    letter-spacing: 3px;
    color: rgba(255,255,255,0.5);
    text-transform: uppercase;
    margin-bottom: 10px;
}

.code-text {
    font-size: 7rem;
    font-weight: 700;
    letter-spacing: 10px;
    margin: 20px 0;
    color: #fff;
    animation: glow-pulse 3s infinite ease-in-out;
}

/* プログレスバー */
.progress-container {
    width: 80%;
    height: 8px;
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    margin: 0 auto;
    overflow: hidden;
    box-shadow: inset 0 0 5px rgba(0,0,0,0.5);
}

.progress-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #00f3ff, #0066ff);
    box-shadow: 0 0 20px #00f3ff;
    transition: width 0.5s linear, background 0.5s ease;
}

.warning-fill {
    background: linear-gradient(90deg, #ff0055, #ff5500) !important;
    box-shadow: 0 0 20px #ff0055 !important;
}

.footer-info {
    margin-top: 30px;
    font-size: 0.9rem;
    color: rgba(255,255,255,0.4);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
}

.live-dot {
    width: 8px;
    height: 8px;
    background-color: #00f3ff;
    border-radius: 50%;
    box-shadow: 0 0 10px #00f3ff;
    animation: glow-pulse 1s infinite;
}
</style>
""", unsafe_allow_html=True) 
# ↑ ここまでがCSSです！この行の """ と ) を絶対に消さないでください！

def main():
    # キー設定チェック
    if "ARHX" not in TEAM_SECRET_KEY:
         st.error("⚠️ エラー: ソースコード内の TEAM_SECRET_KEY が正しく設定されていません。")
         return

    try:
        totp = pyotp.TOTP(TEAM_SECRET_KEY)
        placeholder = st.empty()
        
        while True:
            current_code = totp.now()
            time_remaining = totp.interval - (time.time() % totp.interval)
            progress_percent = (time_remaining / 30.0) * 100
            
            # 色の切り替え
            bar_class = "progress-fill"
            if time_remaining <= 5:
                bar_class = "progress-fill warning-fill"
            
            display_code = f"{current_code[:3]} {current_code[3:]}"

            html = f"""
            <div class="flux-card">
                <div class="label-text">Secure Access Token</div>
                <div class="code-text">{display_code}</div>
                <div class="progress-container">
                    <div class="{bar_class}" style="width: {progress_percent}%;"></div>
                </div>
                <div class="footer-info">
                    <div class="live-dot"></div>
                    <span>SYNCING: {int(time_remaining)}s</span>
                </div>
            </div>
            """
            
            placeholder.markdown(html, unsafe_allow_html=True)
            time.sleep(0.1)

    except Exception as e:
        st.error(f"System Error: {e}")

if __name__ == "__main__":
    main()

# --- コード終了 ---