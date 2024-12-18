import streamlit as st
from page import Classification, Cluster, FregItemset, Reduct, Preprocess
from pathlib import Path

THIS_DIR = Path(__file__).parent
# CSS tùy chỉnh để làm đẹp giao diện
# st.markdown(
#     """
#     <style>
#         /* Tổng thể nền */
#         body {
#             background: radial-gradient(circle at top, #126782, #000000);
#             color: white;
#             font-family: Arial, sans-serif;
#         }
#         /* Navigation bar */
#         .nav-container {
#             display: flex;
#             justify-content: space-around;
#             background: linear-gradient(90deg, #126782, #219EBC);
#             padding: 10px;
#             border-radius: 10px;
#             margin: 20px auto;
#             width: 80%;
#         }
#         .nav-link {
#             color: white;
#             font-size: 18px;
#             font-weight: bold;
#             text-decoration: none;
#             padding: 10px 20px;
#             border-radius: 5px;
#             cursor: pointer;
#             transition: background 0.3s ease;
#         }
#         .nav-link:hover, .nav-active {
#             background: #FFB703;
#             color: black;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Hiển thị header
st.set_page_config(page_title="Đồ án Data Mining", page_icon="🎁")
title = "IS252.P11 - Datamining"
st.markdown(f"<h1 style='text-align: center; color: #FFB703;'>{title}</h1>", unsafe_allow_html=True)

# Tạo navigation bar bằng cách sử dụng Streamlit
selected_tab = st.selectbox("Điều Hướng", [
    "Trang chủ",
    "Tiền xử lý dữ liệu",
    "Tập phổ biến và luật kết hợp",
    "Tập thô",
    "Phân lớp",
    "Gom cụm"
])

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

