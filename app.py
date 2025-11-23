import streamlit as st
import os

st.title("🔊 Audio Test Bench")

# 1. ファイルの存在とサイズを確認
file_name = "bgm.mp3"
if os.path.exists(file_name):
    size = os.path.getsize(file_name)
    st.success(f"✅ ファイルを検出しました: {file_name} ({size} bytes)")
    
    if size < 1000:
        st.error("⚠️ ファイルサイズが小さすぎます。中身が空の可能性があります。")
    else:
        # 2. Streamlit標準のプレイヤー（一番確実な方法）
        st.write("### 1. Native Player")
        st.audio(file_name, format="audio/mp3")
        
        # 3. HTML5標準プレイヤー（ブラウザ機能）
        st.write("### 2. HTML5 Raw Player")
        st.markdown(f"""
            <audio controls>
                <source src="{file_name}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """, unsafe_allow_html=True)
        
else:
    st.error(f"🚨 エラー: '{file_name}' が見つかりません！GitHubにアップロードされていますか？")

st.write("---")
st.caption("もしこれでも音が鳴らない場合、PCの音量設定か、アップロードしたmp3ファイル自体が壊れています。")