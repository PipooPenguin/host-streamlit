import streamlit as st
def draw_table(df):
    data_html = df.to_html(
        index=False,
        classes='data-table',  # Thêm class để áp dụng CSS
        border=0
    )
    # Hiển thị CSS và bảng HTML
    with st.container(height=500, border=0):
        st.markdown(
            f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)