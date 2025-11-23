import streamlit as st
from pathlib import Path


def load_image(image_path: Path):
    """Read image file into bytes for display."""
    return image_path.read_bytes()


def main():
    st.set_page_config(
        page_title="ChatGPTの便利な使い方", page_icon="🤖", layout="wide"
    )

    # Load assets
    base_dir = Path(__file__).resolve().parent
    hero_img = load_image(base_dir / "b94d9ec5-df2d-479a-9e70-9fc08847c458.png")

    # Sidebar navigation
    page = st.sidebar.selectbox(
        "ナビゲーション",
        [
            "ホーム",
            "機械工学科向け",
            "一般大学生向け",
            "ガイドラインと注意点",
            "まとめ",
        ],
    )

    # Common styles injected via markdown
    st.markdown(
        """
        <style>
        /* Global typography and colours inspired by Apple's clean aesthetic */
        body, html {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        .hero {
            position: relative;
            width: 100%;
            height: 70vh;
            overflow: hidden;
        }
        .hero img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: brightness(0.6);
        }
        .hero-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            text-align: center;
            animation: fadeInUp 1.5s ease-out forwards;
            opacity: 0;
        }
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translate3d(-50%, -40%, 0);
            }
            to {
                opacity: 1;
                transform: translate3d(-50%, -50%, 0);
            }
        }
        .section {
            padding: 3rem 1rem;
            margin: 0 auto;
            max-width: 900px;
        }
        .section h2 {
            margin-bottom: 1rem;
        }
        .section p {
            line-height: 1.6;
        }
        /* Responsive text */
        h1, h2, h3 {
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if page == "ホーム":
        # Hero section with image and overlayed text
        st.markdown(
            f"""
            <div class="hero">
                <img src="data:image/png;base64,{hero_img.hex()}" alt="hero background" />
                <div class="hero-text">
                    <h1>ChatGPTの便利な使い方</h1>
                    <h2>機械工学科・大学生</h2>
                    <p>未来の学習をAIで</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("\n")
        # Introduction section
        with st.container():
            st.subheader("はじめに")
            st.write(
                """
                ChatGPTはOpenAIによって開発された対話型AIで、自然な文章を生成する能力を持ちます。本サイトでは、機械システム工学科の学生や一般的な大学生が
                ChatGPTを学習や研究に役立てるための具体的な方法を紹介します。簡単な質問から専門的な解説まで、幅広い活用方法を体験しながら学んでください。
                """
            )
            # Trigger a small animation on the home page
            st.balloons()

    elif page == "機械工学科向け":
        st.header("機械工学科の学生のためのChatGPT活用法")
        st.write(
            """
            機械設計や加工、実験に携わる学生にとって、ChatGPTは補助的なツールとして様々な場面で役立ちます。以下にその例を示します：
            """
        )
        # Use bullet points with icons
        st.markdown(
            """
            - **設計アイデアの発想支援**：プロンプトに条件や制約を入力すると、設計の方向性や考え方を提案してくれます。\
              ChatGPTは例えば材料の組み合わせや構造の特徴を列挙することでアイデア出しをサポートします。
            - **技術文献の要約**：英語の論文や技術資料を貼り付けると、主要なポイントを日本語で要約してくれるので、研究の背景調査が効率化します。
            - **計算やプログラミング補助**：PythonやMATLABの簡単なコード例を提示させることで、数値解析やシミュレーションの出発点を得ることができます。\
              ただし、数式の具体的な計算では誤りが含まれる可能性があるため必ず手計算や既存の教科書で検証してください【{}†L63-L70】。
            - **設計報告書の構成案**：報告書やレポートの章立てを提案してもらい、自分の考えを整理する手助けにします。
            - **CAD・CAEのコマンドや用語の理解**：専門的なソフトウェアの操作に関する基本的な質問に答えてくれますが、最新バージョンの仕様は常に公式ドキュメントで確認しましょう。
            """.format(
                "402173064024730"
            ),
            unsafe_allow_html=True,
        )
        st.info(
            "AIを利用して回答を得た場合でも、結果を鵜呑みにせず、必ず自分で検証する姿勢が重要です。"
        )

    elif page == "一般大学生向け":
        st.header("一般大学生のためのChatGPT活用法")
        st.write(
            """
            理系・文系を問わず、大学生にとってChatGPTは学習を効率化する強力なアシスタントです。以下はその具体例です：
            """
        )
        st.markdown(
            """
            - **講義や試験勉強のリサーチ**：授業で分からないキーワードや概念を自然言語で質問し、情報収集の手間を削減できます【{}†L85-L91】。
            - **英語記事の要約・翻訳**：英語文献を貼り付けると要約や翻訳を生成し、国際的な文献を素早く理解できます【{}†L90-L94】。
            - **文章添削と改善**：自分が書いた英文や日本語の文章を添削させ、読みやすい表現に改善できます【{}†L95-L100】。
            - **アイデア出し**：レポートや研究テーマ、サークル活動の企画などで複数のアイデアを提案してもらえます【{}†L100-L104】。
            - **プログラミングサポート**：特定の課題を伝えることで、簡単なスクリプトやアルゴリズムの例を得ることができます【{}†L107-L110】。
            """.format(
                "510223605288538",
                "510223605288538",
                "510223605288538",
                "510223605288538",
                "510223605288538",
            ),
            unsafe_allow_html=True,
        )
        st.info(
            "ChatGPTの回答は完璧ではありません。信頼性を確認しながら活用し、同じ質問でもプロンプトを変えて比較検討することが重要です。"
        )

    elif page == "ガイドラインと注意点":
        st.header("大学での生成AI利用のガイドライン")
        st.write(
            """
            文部科学省は大学・高専における生成AIの取り扱いについてガイドラインを示しており、ChatGPTの利用が効果的とされる場面と留意すべき点を挙げています【{}†L116-L135】。
            """.format("793708520506121"),
        )
        st.markdown(
            """
            **推奨される活用場面**：
            
            - ブレインストーミングや論点の洗い出しによる学習支援
            - 情報収集・文章構成・翻訳・プログラミング補助などの学びの補助
            - 教員による教材開発や大学事務の効率化
            
            **留意点**：
            
            - 学習活動との関係や成績評価をどう扱うか
            - 生成物の虚偽情報や著作権侵害に注意する
            - 個人情報や機密情報の取り扱いに十分配慮する
            
            これらのポイントを踏まえ、ChatGPTを「学びを深める道具」として利用し、自身の考えを整理する助けとすることが重要です【{}†L33-L48】。
            """.format("793708520506121", "432405058487231"),
            unsafe_allow_html=True,
        )
        st.info(
            "どの学科でも、生成AIの技術的限界や倫理的課題を理解したうえで、主体的に利用していくことが求められます。"
        )

    else:  # まとめ
        st.header("まとめ")
        st.write(
            """
            ChatGPTは、機械工学や他の分野の学生にとって大きな助けとなるツールです。情報収集やアイデア出しの時間を短縮し、学習効率を高める一方で、
            生成される情報の信頼性や倫理面への配慮も欠かせません。常に元となる資料で確認し、自分の言葉でまとめる姿勢を心がけてください。
            """
        )
        # Concluding animation for fun
        if st.button("🎉 お疲れさまでした！クリックしてお祝い"):
            st.snow()
            st.write("ご覧いただきありがとうございました！")


if __name__ == "__main__":
    main()