import streamlit as st
import streamlit.components.v1 as components

# ページ設定（ワイドモードにしてデザインを崩れにくくする）
st.set_page_config(
    page_title="GenAI for Engineers",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# HTML/CSS/JSコード全体を文字列として定義
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatGPT for Engineering Students</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Noto Sans JP', sans-serif;
            background-color: #f5f5f7; /* Apple Light Grey */
            color: #1d1d1f;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
        }
        
        /* スクロールアニメーション用のクラス */
        .reveal {
            opacity: 0;
            transform: translateY(50px);
            transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        .reveal.active {
            opacity: 1;
            transform: translateY(0);
        }

        .scale-reveal {
            opacity: 0;
            transform: scale(0.95);
            transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .scale-reveal.active {
            opacity: 1;
            transform: scale(1);
        }

        /* グラデーションテキスト */
        .text-gradient {
            background: linear-gradient(90deg, #007aff, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Streamlitのiframe内での表示調整 */
        section {
            box-sizing: border-box;
        }
    </style>
</head>
<body>

    <nav class="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-gray-200 transition-all duration-300" id="navbar">
        <div class="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">
            <span class="font-bold text-lg tracking-tight">GenAI <span class="text-gray-500">for Engineers</span></span>
            <a href="#" class="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-medium hover:bg-blue-700 transition">使ってみる</a>
        </div>
    </nav>

    <section class="min-h-screen flex flex-col justify-center items-center text-center px-6 pt-20">
        <div class="reveal active space-y-6 max-w-4xl">
            <h2 class="text-2xl md:text-4xl font-bold text-gray-500">工学部の学びを、<br class="md:hidden">もっと自由に。</h2>
            <h1 class="text-5xl md:text-8xl font-black tracking-tighter leading-tight">
                あなたの第2の脳。<br>
                <span class="text-gradient">ChatGPT</span>
            </h1>
            <p class="text-xl md:text-2xl text-gray-600 mt-4 max-w-2xl mx-auto">
                実験データの解析から、難解な物理法則の理解まで。<br>
                機械工学科での日々を、劇的に加速させるパートナー。
            </p>
        </div>
        
        <div class="mt-16 w-full max-w-5xl scale-reveal">
            <div class="relative aspect-video bg-gradient-to-br from-gray-100 to-gray-200 rounded-3xl shadow-2xl overflow-hidden flex items-center justify-center border border-white">
                <div class="text-center space-y-4">
                    <div class="text-9xl">🤖 ⚡️ ⚙️</div>
                    <p class="text-gray-400 font-bold tracking-widest uppercase">Engineering Intelligence</p>
                </div>
                <div class="absolute top-10 left-10 bg-white p-4 rounded-2xl shadow-lg animate-bounce" style="animation-duration: 3s;">
                    <code class="text-sm text-blue-600 font-mono">import numpy as np</code>
                </div>
                <div class="absolute bottom-20 right-10 bg-white p-4 rounded-2xl shadow-lg animate-bounce" style="animation-duration: 4s;">
                    <span class="text-xl font-serif italic">F = ma</span>
                </div>
            </div>
        </div>
    </section>

    <section class="py-32 bg-white">
        <div class="max-w-5xl mx-auto px-6">
            <div class="grid md:grid-cols-2 gap-16 items-center">
                <div class="reveal">
                    <h3 class="text-sm font-bold text-blue-600 uppercase tracking-widest mb-2">データ解析・可視化</h3>
                    <h2 class="text-4xl md:text-5xl font-bold mb-6">実験データ、<br>一瞬でグラフに。</h2>
                    <p class="text-lg text-gray-600 leading-relaxed">
                        CSVファイルをアップロードするだけ。「このデータの散布図を描いて」「近似曲線を求めて」と頼めば、Pythonコードごと出力。単位の換算ミスも、次元解析のチェックも、もう心配いりません。
                    </p>
                </div>
                <div class="scale-reveal relative group">
                    <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
                    <div class="relative bg-gray-900 rounded-2xl p-6 shadow-2xl text-white font-mono text-sm overflow-hidden">
                        <div class="flex space-x-2 mb-4">
                            <div class="w-3 h-3 rounded-full bg-red-500"></div>
                            <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                            <div class="w-3 h-3 rounded-full bg-green-500"></div>
                        </div>
                        <p class="text-green-400"># User Input</p>
                        <p class="mb-4">応力-ひずみ線図を作成し、ヤング率を求めて。</p>
                        <p class="text-blue-400"># ChatGPT Output</p>
                        <p>import pandas as pd<br>import matplotlib.pyplot as plt<br>...</p>
                        <div class="mt-4 h-32 bg-gray-800 rounded border border-gray-700 flex items-center justify-center text-gray-500">
                            [Graph Output Area]
                        </div>
                    </div>
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
                
                <div class="md:col-span-2 md:row-span-2 bg-white rounded-3xl p-8 shadow-sm hover:shadow-xl transition duration-500 scale-reveal flex flex-col justify-between overflow-hidden relative">
                    <div class="z-10">
                        <h3 class="text-3xl font-bold mb-2">難解な論文も、<br>3行で要約。</h3>
                        <p class="text-gray-600 mt-4 max-w-md">
                            英語の論文PDFをアップロード。「この論文の結論と、実験条件の限界を教えて」と聞くだけで、要点を抽出。先行研究の調査時間を大幅に短縮します。
                        </p>
                    </div>
                    <div class="absolute bottom-[-50px] right-[-50px] w-80 h-80 bg-blue-100 rounded-full blur-3xl opacity-50"></div>
                    <div style="background-color: #f3f4f6; color: #a1a1aa; height: 200px; width: 100%; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-top: 40px; transform: rotate(2deg);">
                        Paper Summary PDF
                    </div>
                </div>

                <div class="bg-white rounded-3xl p-8 shadow-sm hover:shadow-xl transition duration-500 scale-reveal flex flex-col justify-center items-center text-center">
                    <div class="text-5xl mb-4">🔬</div>
                    <h3 class="text-xl font-bold">レポート作成支援</h3>
                    <p class="text-sm text-gray-500 mt-2">
                        「考察の切り口を提案して」<br>
                        ※コピペは厳禁。思考の補助輪として。
                    </p>
                </div>

                <div class="bg-black text-white rounded-3xl p-8 shadow-sm hover:shadow-xl transition duration-500 scale-reveal flex flex-col justify-between">
                    <div>
                        <h3 class="text-xl font-bold text-purple-400">Code Assistant</h3>
                        <p class="text-sm text-gray-400 mt-2">Arduino, Python, MATLAB.<br>エラーの原因を一瞬で特定。</p>
                    </div>
                    <div class="mt-4 bg-gray-800 p-3 rounded-lg text-xs font-mono text-green-400">
                        > Error fixed.
                    </div>
                </div>

                <div class="md:col-span-3 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-3xl p-10 text-white shadow-lg scale-reveal flex flex-col md:flex-row items-center justify-between">
                    <div class="mb-6 md:mb-0">
                        <h3 class="text-3xl font-bold">アイデア出しの壁打ち相手。</h3>
                        <p class="text-indigo-100 mt-2">設計課題のブレーンストーミングや、プレゼンの構成案まで。</p>
                    </div>
                    <button class="bg-white text-indigo-600 px-8 py-3 rounded-full font-bold hover:bg-opacity-90 transition shadow-lg">
                        プロンプトを見る
                    </button>
                </div>

            </div>
        </div>
    </section>

    <section class="py-32 bg-white text-center">
        <div class="max-w-4xl mx-auto px-6 reveal">
            <p class="text-gray-500 font-medium mb-4">圧倒的な効率化</p>
            <h2 class="text-5xl md:text-7xl font-bold mb-16">もう、<br>単純作業に時間を割かない。</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 text-center">
                <div>
                    <div class="text-6xl font-black text-blue-600 mb-2">50<span class="text-3xl">%</span></div>
                    <p class="text-gray-600 font-medium">プログラミング時間の短縮</p>
                </div>
                <div>
                    <div class="text-6xl font-black text-blue-600 mb-2">10<span class="text-3xl">x</span></div>
                    <p class="text-gray-600 font-medium">アイデアの創出数</p>
                </div>
                <div>
                    <div class="text-6xl font-black text-blue-600 mb-2">∞</div>
                    <p class="text-gray-600 font-medium">いつでも質問可能なTAとして</p>
                </div>
            </div>
        </div>
    </section>

    <section class="py-20 bg-[#f5f5f7]">
        <div class="max-w-4xl mx-auto px-6 text-center reveal">
            <h2 class="text-3xl md:text-4xl font-bold mb-8">さあ、エンジニアリングをアップデートしよう。</h2>
            <div class="flex flex-col md:flex-row justify-center gap-4">
                <a href="https://chat.openai.com" target="_blank" class="bg-blue-600 text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-blue-700 transition shadow-lg transform hover:scale-105 duration-200">
                    ChatGPTを開く
                </a>
                <a href="#" class="bg-white text-black border border-gray-300 px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-50 transition shadow-sm">
                    プロンプト集を見る
                </a>
            </div>
            <p class="mt-8 text-xs text-gray-400">
                ※ 生成AIの回答には誤りが含まれる可能性があります。工学的な問題解決においては、必ず教科書や信頼できる文献で裏付け（4点検算）を行ってください。
            </p>
        </div>
    </section>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: "0px 0px -50px 0px"
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('active');
                    }
                });
            }, observerOptions);

            const revealElements = document.querySelectorAll('.reveal, .scale-reveal');
            revealElements.forEach(el => observer.observe(el));
        });
    </script>
</body>
</html>
"""

# HTMLをレンダリング（高さはコンテンツに合わせて調整してください）
# height=3500はページ全体の長さに応じて調整が必要な場合があります
components.html(html_code, height=3500, scrolling=True)