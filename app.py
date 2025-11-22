import streamlit as st
import pyotp
import time

# ==========================================
# ⚙️ SETTINGS
# ==========================================
try:
    TEAM_SECRET_KEY = st.secrets["TEAM_SECRET_KEY"]
except FileNotFoundError:
    TEAM_SECRET_KEY = "ARHXCWTVFU54ITHIXS4Q76SVCDFLC5TU"

# ==========================================
# 🎨 CSS STYLES (Static)
# ==========================================
# CSSをループの外に出して、読み込みを安定させます
CSS_CODE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400&display=swap');

.stApp {
    background-color: #000;
    background: radial-gradient(circle at 50% 0%, #1c1c1e 0%, #000000 85%);
    font-family: 'Inter', sans-serif;
    color: #f5f5f7;
    overflow-x: hidden;
}

header, footer {visibility: hidden;}
.block-container { padding-top: 2rem; max-width: 1200px; }

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero-container {
    text-align: center;
    margin-bottom: 80px;
    padding: 60px 40px;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(40px);
    -webkit-backdrop-filter: blur(40px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 32px;
    box-shadow: 0 30px 60px rgba(0,0,0,0.7);
    animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

.hero-label {
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #86868b;
    margin-bottom: 20px;
}

.hero-code {
    font-size: 9rem;
    font-weight: 800;
    letter-spacing: -4px;
    line-height: 1;
    margin: 20px 0;
    background: linear-gradient(180deg, #ffffff 10%, #555555 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-variant-numeric: tabular-nums;
    filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));
}

.progress-wrapper {
    width: 50%;
    height: 8px;
    background: #222;
    border-radius: 100px;
    margin: 0 auto 25px auto;
    overflow: hidden;
    border: 1px solid #333;
}

.progress-bar {
    height: 100%;
    background: #fff;
    border-radius: 100px;
    transition: width 1s linear;
    box-shadow: 0 0 20px rgba(255,255,255,0.5);
}

.warning-mode {
    background: #ff3b30 !important;
    box-shadow: 0 0 25px rgba(255, 59, 48, 0.8);
}

.grid-header {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 10px;
    text-align: left;
    color: #f5f5f7;
    letter-spacing: -1px;
    opacity: 0;
    animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.2s forwards;
}
.grid-sub {
    font-size: 1.3rem;
    color: #86868b;
    font-weight: 400;
    margin-bottom: 50px;
    max-width: 600px;
    line-height: 1.5;
    opacity: 0;
    animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.3s forwards;
}

.bento-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
    gap: 25px;
    padding-bottom: 100px;
}

.feature-card {
    background: #151516;
    border-radius: 28px;
    padding: 35px;
    height: 100%;
    border: 1px solid rgba(255,255,255,0.05);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    opacity: 0;
    animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

.delay-1 { animation-delay: 0.4s; }
.delay-2 { animation-delay: 0.5s; }
.delay-3 { animation-delay: 0.6s; }
.delay-4 { animation-delay: 0.7s; }
.delay-5 { animation-delay: 0.8s; }
.delay-6 { animation-delay: 0.9s; }

.feature-card:hover {
    transform: scale(1.02) translateY(-5px);
    background: #1c1c1e;
    border-color: rgba(255,255,255,0.3);
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}

.feature-icon { 
    font-size: 2.5rem; 
    margin-bottom: 20px; 
    background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.02));
    width: 64px; height: 64px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.05);
}

.feature-title { font-weight: 700; font-size: 1.5rem; color: #fff; margin-bottom: 12px; }
.feature-desc { font-size: 1rem; color: #a1a1a6; line-height: 1.6; margin-bottom: 20px; }
.use-case {
    font-size: 0.85rem;
    color: #6e6e73;
    margin-bottom: 15px;
    padding-left: 10px;
    border-left: 2px solid #333;
}
.feature-cmd {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #64d2ff;
    background: rgba(100, 210, 255, 0.1);
    padding: 12px 15px;
    border-radius: 12px;
    border: 1px solid rgba(100, 210, 255, 0.15);
    word-break: break-all;
}
</style>
"""

# ==========================================
# 🏗️ HTML GENERATOR (Component)
# ==========================================
# 関数化することでインデント問題を完全に回避します
def get_dashboard_html(display_code, progress_percent, bar_class, time_remaining):
    return f"""
    <div class="hero-container">
        <div class="hero-label">Titanium Security Layer</div>
        <div class="hero-code">{display_code}</div>
        
        <div class="progress-wrapper">
            <div class="{bar_class}" style="width: {progress_percent}%;"></div>
        </div>
        
        <div style="color: #86868b; font-size: 0.9rem; font-weight: 500; letter-spacing: 0.5px;">
            SYNCING WITH SECURE ENCLAVE: <span style="color:#fff;">{int(time_remaining)}s</span>
        </div>
    </div>
    
    <div>
        <div class="grid-header">Engineering Intelligence.</div>
        <div class="grid-sub">
            機械工学科の課題・実験・研究をハックする6つのAIプロンプト。<br>
            授業で使える具体的なユースケースをプリセット。
        </div>
    </div>
    
    <div class="bento-grid">
        <div class="feature-card delay-1">
            <div>
                <div class="feature-icon">📸</div>
                <div class="feature-title">Math Vision to LaTeX</div>
                <div class="feature-desc">
                    板書や教科書の複雑な数式（積分・偏微分・行列）をスマホで撮影してアップロードするだけ。
                    一瞬でレポートに貼り付け可能なLaTeXコードに変換します。
                </div>
                <div class="use-case">
                    Use for: 流体力学のナビエ・ストークス方程式、熱力学の偏微分
                </div>
            </div>
            <div class="feature-cmd">"この画像を解析して、Overleafに貼れるLaTeXコードを出力して"</div>
        </div>
        
        <div class="feature-card delay-2">
            <div>
                <div class="feature-icon">📊</div>
                <div class="feature-title">Graph Reverse Eng.</div>
                <div class="feature-desc">
                    論文のPDFや参考書のグラフ画像を解析し、元のプロットデータ（CSV数値）を復元・抽出します。
                    先行研究と自分の実験データをExcelやPythonで重ね合わせたい時に。
                </div>
                <div class="use-case">
                    Use for: 材料力学のS-N曲線比較、エンジンのトルク線図
                </div>
            </div>
            <div class="feature-cmd">"このグラフ画像のプロットデータを抽出し、CSV形式で出力して"</div>
        </div>
        
        <div class="feature-card delay-3">
            <div>
                <div class="feature-icon">🐍</div>
                <div class="feature-title">Polyglot Converter</div>
                <div class="feature-desc">
                    授業で指定されたMATLABコードを、使い慣れたPython (NumPy/SciPy) に完全移植します。
                    C言語やFortranへの書き換えも可能。
                </div>
                <div class="use-case">
                    Use for: 制御工学演習、数値解析の課題
                </div>
            </div>
            <div class="feature-cmd">"このMATLABコードをPythonに変換し、ライブラリの依存関係も教えて"</div>
        </div>

        <div class="feature-card delay-4">
            <div>
                <div class="feature-icon">🧪</div>
                <div class="feature-title">Error Propagation</div>
                <div class="feature-desc">
                    実験レポート最大の難所「誤差伝播」の計算を自動化。
                    測定式と各変数の誤差範囲を入力すれば、偏微分を用いた最終的な誤差を算出します。
                </div>
                <div class="use-case">
                    Use for: 物理学実験、機械加工精度の測定
                </div>
            </div>
            <div class="feature-cmd">"この式の誤差伝播を計算して。測定値x=10±0.1, y=5±0.05とする"</div>
        </div>

        <div class="feature-card delay-5">
            <div>
                <div class="feature-icon">📐</div>
                <div class="feature-title">Dimensional Check</div>
                <div class="feature-desc">
                    複雑な物理式の左辺と右辺で、次元（単位）が整合しているかをAIが解析・検算します。
                    無次元数が正しく構成されているかのチェックにも。
                </div>
                <div class="use-case">
                    Use for: 伝熱工学の式変形チェック、流体解析の境界条件
                </div>
            </div>
            <div class="feature-cmd">"この式の両辺の次元解析を行い、物理的に正しいか検証して"</div>
        </div>

        <div class="feature-card delay-6">
            <div>
                <div class="feature-icon">📝</div>
                <div class="feature-title">Academic Polish</div>
                <div class="feature-desc">
                    書き殴った文章を、提出に耐えうる「学術的かつ論理的な日本語（である調）」に推敲・校正します。
                </div>
                <div class="use-case">
                    Use for: 最終レポートの「考察」、卒業論文の草稿
                </div>
            </div>
            <div class="feature-cmd">"この文章を、機械工学の実験レポートとして適切な学術的文章にリライトして"</div>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 80px; color: #333; font-size: 0.8rem; padding-bottom: 20px;">
        Designed for Mechanical Engineering Students. v5.0 Titanium Pro Max
    </div>
    """

# ==========================================
# 🚀 MAIN APP
# ==========================================
def main():
    st.set_page_config(page_title="Auth Pro Max", page_icon="", layout="wide")
    
    # CSSを注入（1回だけ）
    st.markdown(CSS_CODE, unsafe_allow_html=True)

    if not TEAM_SECRET_KEY or "ARHX" not in TEAM_SECRET_KEY:
        st.error("⚠️ Secrets Error")
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
            
            # HTMLを生成する関数を呼び出す（これでインデントが崩れません！）
            html_content = get_dashboard_html(display_code, progress_percent, bar_class, time_remaining)
            
            main_placeholder.markdown(html_content, unsafe_allow_html=True)
            time.sleep(0.1)

    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()