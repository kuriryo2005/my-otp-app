import streamlit as st
import base64
import os

# ==========================================
# 🛠️ 最小構成オーディオ機能
# ==========================================
def get_audio_player_html(file_name):
    # 1. ファイルチェック
    if not os.path.exists(file_name):
        st.error(f"❌ '{file_name}' が見つかりません。")
        return ""
    
    # 2. データをBase64化
    with open(file_name, "rb") as f:
        b64_audio = base64.b64encode(f.read()).decode()

    # 3. HTML & JS (ボタンとロジックのみ)
    return f"""
    <style>
    .audio-btn {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: #333;
        color: white;
        font-size: 24px;
        font-weight: bold;
        cursor: pointer;
        margin: 50px auto;
        border: 4px solid #555;
        transition: background 0.3s;
        user-select: none;
    }}
    .audio-btn:hover {{ background: #444; }}
    .audio-btn.playing {{
        background: #2ecc71; /* 緑色 */
        border-color: #27ae60;
        box-shadow: 0 0 30px #2ecc71;
    }}
    </style>

    <div id="simple-btn" class="audio-btn" onclick="toggleSimpleAudio()">
        ▶ PLAY
    </div>

    <script>
    // 1. 音楽プレイヤーをウィンドウ領域に常駐させる (リロード対策)
    if (!window.simpleAudio) {{
        console.log("Audio initialized");
        window.simpleAudio = new Audio("data:audio/mp3;base64,{b64_audio}");
        window.simpleAudio.loop = true;
        window.simpleAudio.volume = 0.5;
    }}

    // 2. ボタンの状態を更新する関数
    function updateButtonState() {{
        var btn = document.getElementById("simple-btn");
        if (!btn) return;
        
        if (!window.simpleAudio.paused) {{
            btn.classList.add("playing");
            btn.innerHTML = "⏸ STOP";
        }} else {{
            btn.classList.remove("playing");
            btn.innerHTML = "▶ PLAY";
        }}
    }}

    // 3. クリック時の動作
    window.toggleSimpleAudio = function() {{
        var btn = document.getElementById("simple-btn");
        
        if (window.simpleAudio.paused) {{
            window.simpleAudio.play()
                .then(() => {{ updateButtonState(); }})
                .catch(e => {{ alert("再生エラー: " + e); }});
        }} else {{
            window.simpleAudio.pause();
            updateButtonState();
        }}
    }}

    // 4. 読み込み時にボタンの状態を復元
    // (Streamlitが画面を再描画しても、再生中なら緑色に戻す)
    setTimeout(updateButtonState, 100);
    </script>
    """

# ==========================================
# 🚀 MAIN
# ==========================================
def main():
    st.set_page_config(page_title="Audio Test", layout="centered")
    st.title("🎵 Audio Isolation Test")
    st.write("ボタンを押して音楽が鳴るか確認してください。")
    
    # プレイヤーの表示
    html = get_audio_player_html("bgm.mp3")
    st.components.v1.html(html, height=400)

if __name__ == "__main__":
    main()