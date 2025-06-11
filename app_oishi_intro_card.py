import streamlit as st
from datetime import date

st.title("推し紹介カード作成ツール")
st.caption("あなたの推しを紹介するためのカードを簡単に作成できるアプリです。")

st.markdown("---")
st.subheader("推し紹介カードを作成しよう")
st.write("フォームに情報を入力して、推し紹介カードを作成してください。")

# カード情報を保存するリスト
if "cards" not in st.session_state:
    st.session_state.cards = []

# 編集モードの状態を保存
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# フォームで推し情報を入力
with st.form("profile_form"):
    st.subheader("推し情報を入力してください")
    
    # 基本情報
    name = st.text_input("推しの名前", placeholder="山田 太郎")
    nickname = st.text_input("推しのニックネーム", placeholder="たろちゃん")
    
    # 推しの詳細情報
    category_options = [
        "アイドル",
        "俳優",
        "声優",
        "アーティスト",
        "その他"
    ]
    selected_category = st.selectbox("推しのカテゴリ", category_options)

    # 「その他」が選ばれたとき用の入力欄（常に表示）
    custom_category = st.text_input("カテゴリ名（「その他」を選んだ場合のみ入力）", placeholder="例：スポーツ選手、作家 など")

    # 実際に使うカテゴリ名を決定
    category = custom_category if selected_category == "その他" else selected_category

    # 推し始めた日（ここを推し歴の代わりに表示）
    start_date = st.date_input("推し始めた日", value=date.today())

    # 推しの魅力
    hobbies = st.text_area("推しの魅力・好きなところ", placeholder="歌が上手い、演技が素晴らしい、笑顔が素敵など")
    memories = st.text_area("推しとの思い出", placeholder="初めてライブに行った日、握手会でのエピソードなど")
    
    # SNS情報の追加（順番をここに移動）
    st.markdown("#### 推しのSNSアカウント（任意）")
    twitter = st.text_input("X（旧Twitter）", placeholder="@oshiname")
    instagram = st.text_input("Instagram", placeholder="@oshiname")
    youtube = st.text_input("YouTube", placeholder="チャンネル名やURL")
    
    # 推しの画像
    icon_image = st.file_uploader(
        "推しの画像をアップロード（任意）", 
        type=['png', 'jpg', 'jpeg'],
        help="PNG、JPG、JPEG形式の画像をアップロードできます"
    )
    
    # カスタマイズオプション
    col1, col2 = st.columns(2)
    with col1:
        card_color = st.color_picker("テーマカラー１", "#FFE6F2")  # デフォルトをピンクに変更
    with col2:
        favorite_color = st.color_picker("テーマカラー２", "#FF69B4")  # デフォルトをピンクに変更

    # フォーム送信ボタン
    submitted = st.form_submit_button("推し紹介カードを作成！", use_container_width=True)

# カード表示エリア
st.markdown("---")
st.subheader("完成した推し紹介カード")

if submitted:
    if not name:
        st.error("推しの名前は必須項目です。入力してください。")
    else:
        # カード情報を保存
        st.session_state.cards.append({
            "name": name,
            "nickname": nickname,
            "category": category,
            "hobbies": hobbies,
            "memories": memories,
            "icon_image": icon_image,
            "card_color": card_color,
            "favorite_color": favorite_color,
            "twitter": twitter,
            "instagram": instagram,
            "youtube": youtube,
            "start_date": start_date
        })
        st.success("推し紹介カードが作成されました！")

# 検索機能
st.markdown("---")
st.subheader("カード検索")
search_name = st.text_input("名前で検索", placeholder="例: 山田 太郎")
search_category = st.selectbox("カテゴリで検索", ["すべて"] + [
    "アイドル", "俳優", "声優", "アーティスト", "その他"
])

# 検索結果をフィルタリング
filtered_cards = [
    card for card in st.session_state.cards
    if (not search_name or search_name in card["name"]) and
       (search_category == "すべて" or search_category == card["category"])
]

# 保存されたカードを順番に表示
for index, card in enumerate(filtered_cards):
    if st.session_state.edit_index == index:
        # 編集フォームを表示
        with st.form(f"edit_form_{index}"):
            st.subheader(f"{card['name']} のカードを編集")
            
            # 編集用の入力項目
            name = st.text_input("推しの名前", value=card["name"])
            nickname = st.text_input("推しのニックネーム", value=card["nickname"])
            category_options = [
                "アイドル",
                "俳優",
                "声優",
                "アーティスト",
                "その他"
            ]
            selected_category = st.selectbox("推しのカテゴリ", category_options, index=category_options.index(card["category"]) if card["category"] in category_options else len(category_options) - 1)
            custom_category = st.text_input("カテゴリ名（「その他」を選んだ場合のみ入力）", value=card["category"] if selected_category == "その他" else "")
            category = custom_category if selected_category == "その他" else selected_category
            start_date = st.date_input("推し始めた日", value=card["start_date"])
            hobbies = st.text_area("推しの魅力・好きなところ", value=card["hobbies"])
            memories = st.text_area("推しとの思い出", value=card["memories"])
            twitter = st.text_input("X（旧Twitter）", value=card["twitter"])
            instagram = st.text_input("Instagram", value=card["instagram"])
            youtube = st.text_input("YouTube", value=card["youtube"])
            card_color = st.color_picker("テーマカラー１", value=card["card_color"])
            favorite_color = st.color_picker("テーマカラー２", value=card["favorite_color"])
            
            # 編集フォーム送信ボタン
            submitted = st.form_submit_button("保存する")
            cancel = st.form_submit_button("キャンセル")

        if submitted:
            # 更新されたカード情報を保存
            st.session_state.cards[index] = {
                "name": name,
                "nickname": nickname,
                "category": custom_category if selected_category == "その他" else selected_category,  # 修正箇所
                "hobbies": hobbies,
                "memories": memories,
                "icon_image": card["icon_image"],  # 画像は変更不可
                "card_color": card_color,
                "favorite_color": favorite_color,
                "twitter": twitter,
                "instagram": instagram,
                "youtube": youtube,
                "start_date": start_date
            }
            st.session_state.edit_index = None
            st.success(f"{name} のカードを更新しました！")
            st.experimental_rerun()

        if cancel:
            st.session_state.edit_index = None
            st.info("編集をキャンセルしました。")
            st.experimental_rerun()
    else:
        # 通常のカード表示
        st.markdown(f"""
        <div style="
            border: 3px solid {card['favorite_color']};
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            background: linear-gradient(135deg, {card['card_color']} 0%, {card['card_color']}88 100%);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        ">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if card["icon_image"] is not None:
                st.image(card["icon_image"], caption="推しの画像", use_container_width=True)
            else:
                st.markdown(f"""
                <div style="
                    width: 150px;
                    height: 150px;
                    background-color: {card['favorite_color']};
                    border-radius: 75px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 60px;
                    color: white;
                    margin: 10px auto;
                ">
                    ⭐
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            display_name = f"{card['name']} ({card['nickname']})" if card['nickname'] else card['name']
            st.markdown(f"""
            <h2 style="
                color: {card['favorite_color']};
                margin-bottom: 10px;
                font-size: 28px;
            ">
                {display_name}
            </h2>
            """, unsafe_allow_html=True)
            
            st.write(f"**🌟 カテゴリ**: {card['category']}")

            if card.get("start_date"):
                days = (date.today() - card["start_date"]).days
                st.write(f"**⏳ 推し始めた日**: {card['start_date'].strftime('%Y-%m-%d')}（{days}日目）")

            if card["hobbies"]:
                st.write(f"**💖 推しの魅力**: {card["hobbies"]}")
            
            if card["memories"]:
                st.write(f"**📖 推しとの思い出**: {card["memories"]}")
            
            sns_list = []
            if card.get("twitter"):
                sns_list.append(f"🐦 [X（旧Twitter）](https://twitter.com/{card['twitter'].lstrip('@')})")
            if card.get("instagram"):
                sns_list.append(f"📸 [Instagram](https://instagram.com/{card['instagram'].lstrip('@')})")
            if card.get("youtube"):
                sns_list.append(f"▶️ [YouTube]({card['youtube']})")
            if sns_list:
                st.write("**🔗 推しのSNS**: " + "　".join(sns_list))
        
        st.markdown("</div>", unsafe_allow_html=True)

        # 編集ボタンを追加
        if st.button(f"編集する", key=f"edit_{index}"):
            st.session_state.edit_index = index
            st.experimental_rerun()

        # 削除ボタンを追加
        if st.button(f"削除する", key=f"delete_{index}"):
            st.session_state.cards.pop(index)
            st.success(f"{card['name']} のカードを削除しました！")
            st.experimental_rerun()

else:
    st.info("上記フォームに情報を入力して「自己紹介カードを作成！」ボタンを押してください。")

st.markdown("---")
st.sidebar.header("このアプリについて")
st.sidebar.success(
    """
    このアプリでは、推しの情報を入力して紹介カードを作成できます。
    - `st.form` を使って複数の入力項目をまとめて処理します。
    - `st.file_uploader` で推しの画像をアップロードできます。
    - `st.columns` を使って画像とテキスト情報を2列レイアウトで表示します。
    - `st.color_picker` でカードの色をカスタマイズできます。
    - HTMLとCSSを使ってカードのデザインを装飾しています。
    """
)
