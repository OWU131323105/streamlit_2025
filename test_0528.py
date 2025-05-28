import streamlit as st

st.title("第7回 Streamlit フォーム演習 - テンプレート")
st.caption("st.form を使ってサークル入会申し込みフォームを作成しましょう。")

st.markdown("---")
st.subheader("演習: サークル入会申し込みフォーム")
st.write("**課題**: フォームを使って、サークル入会の申し込み情報をまとめて処理するアプリを作成する。")

# ここに演習のコードを記述してください
# ヒント: with st.form("フォーム名"): でフォームを作成し、st.form_submit_button() で送信ボタンを設置
with st.form("circle_application_form"):
    st.write("サークル入会申し込みフォーム")

    # ユーザー情報入力
    name = st.text_input("名前", key="name")
    grade = st.selectbox("学年", ["1年", "2年", "3年", "4年"], key="grade")
    activity = st.selectbox("好きな活動", ["スポーツ", "音楽", "アート", "その他"], key="activity")
    enthusiasm = st.text_area("意気込み", "サークル活動に対する意気込みを入力してください", key="enthusiasm")

    if st.form_submit_button("申し込む"):
        # フォーム送信時の処理
        st.success(f"申し込みが完了しました！")
        st.write(f"名前: {name}")
        st.write(f"学年: {grade}")
        st.write(f"好きな活動: {activity}")
        st.write(f"意気込み: {enthusiasm}")

st.markdown("---")
st.info("💡 全ての項目を入力してから「申し込む」ボタンを押すと、まとめて処理されることを確認してください。") 
