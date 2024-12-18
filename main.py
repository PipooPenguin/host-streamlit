import streamlit as st
from page import Classification, Cluster, FregItemset, Reduct, Preprocess
from pathlib import Path
from assets.table.Dataframe_to_Table import draw_table

THIS_DIR = Path(__file__).parent
TABLE_CSS = THIS_DIR / "assets" / "table" / "table.css"

# Hiển thị
st.set_page_config(page_title="Đồ án Data Mining", page_icon="🎁")
title = "IS252.P11 - Datamining"
st.markdown(f"<h1 style='text-align: center; color: #70161e;'>{title}</h1>", unsafe_allow_html=True)





# Tạo navigation bar bằng cách sử dụng Streamlit
selected_tab = st.selectbox("Điều Hướng", [
    "Trang chủ",
    "Tiền xử lý dữ liệu",
    "Tập phổ biến và luật kết hợp",
    "Tập thô",
    "Phân lớp",
    "Gom cụm"
])
if TABLE_CSS.exists():
    with open(TABLE_CSS, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("CSS file not found!")

# Gọi hàm tương ứng dựa trên tab được chọn
if selected_tab == "Phân lớp":
    Classification.app()
elif selected_tab == "Gom cụm":
    Cluster.app()
elif selected_tab == "Tập phổ biến và luật kết hợp":
    FregItemset.app()
elif selected_tab == "Tập thô":
    Reduct.app()
elif selected_tab == "Tiền xử lý dữ liệu":
    Preprocess.app()
else:
    st.success("✨ Chọn một tính năng từ menu để bắt đầu! ✨")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

