# Import thư viện
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
import graphviz

# Hàm encode dữ liệu
def encode_features(data, columns):
    le_dict = {}
    for col in columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        le_dict[col] = dict(zip(le.classes_, le.transform(le.classes_)))
    return data, le_dict

# Vẽ cây quyết định
def draw_decision_tree(data, measure):
    X = data.drop(columns=["Lớp"])
    y = data["Lớp"].map({'P': 1, 'N': 0})

    X, le_dict = encode_features(X, X.columns)
    criterion = "entropy" if measure == "Độ lợi thông tin" else "gini"

    clf = DecisionTreeClassifier(criterion=criterion)
    clf.fit(X, y)

    dot_data = export_graphviz(clf, out_file=None, feature_names=X.columns,
                               class_names=["N", "P"], filled=True, rounded=True)
    st.graphviz_chart(graphviz.Source(dot_data))

# Phân lớp mẫu
def classify_sample(data, method, features):
    X = data.drop(columns=['Lớp'])
    y = data['Lớp'].map({'P': 1, 'N': 0})

    X, le_dict = encode_features(X, X.columns)
    model = DecisionTreeClassifier(criterion="entropy") if method == "Cây quyết định" else GaussianNB()
    model.fit(X, y)

    try:
        user_input = [le_dict[col].get(features[col], -1) for col in X.columns]
        prediction = model.predict([user_input])
        class_label = 'P' if prediction[0] == 1 else 'N'
        st.success(f"Dự đoán: Lớp '{class_label}'")
    except Exception as e:
        st.error(f"Lỗi: {e}")

# Ứng dụng chính
def app():
    custom_data_table_css = """
        <style>
            .data-table-container {
                display: flex;
                justify-content: center; /* Căn giữa bảng */
                align-items: center;
                margin: 20px auto; /* Căn giữa bảng */
                max-width: 100%; /* Giới hạn chiều rộng */
                overflow-x: auto; /* Thêm cuộn ngang nếu bảng quá rộng */
            }
            .data-table {
                border-collapse: collapse;
                font-size: 16px; /* Kích thước chữ */
                font-family: Arial, sans-serif;
                width: 100%; /* Chiếm toàn bộ chiều rộng khung */
                text-align: center;
                border: 1px solid #ddd; /* Viền bảng */
                color: #023047;
            }
            .data-table th {
                background-color: #FFB703; /* Màu nền tiêu đề */
                color: #FFFFFF; /* Màu chữ tiêu đề */
                padding: 10px;
                text-align: center;
            }
            .data-table td {
                padding: 8px 10px;
                text-align: center;
            }
            .data-table tr:nth-child(even) {
                background-color: #f3f3f3; /* Màu nền dòng chẵn */
            }
            .data-table tr:nth-child(odd) {
                background-color: #ffffff; /* Màu nền dòng lẻ */
            }
            .data-table tr:hover {
                background-color: #8ECAE6; /* Màu nền khi hover */
                color: #000000; /* Màu chữ khi hover */
            }
        </style>
    """

    st.markdown(custom_data_table_css, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Tải file dữ liệu (CSV):", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.markdown("<div class='data-table-container'>" +
                    data.to_html(index=False, classes='data-table', border=0) + "</div>", 
                    unsafe_allow_html=True)

        # Vẽ cây quyết định
        st.subheader("Vẽ cây quyết định")
        algorithm = st.selectbox("Chọn thuật toán", ["None", "Thuật toán ID3"])
        if algorithm == "Thuật toán ID3":
            measure = st.radio("Chọn độ đo:", ["Độ lợi thông tin", "Chỉ số Gini"])
            if st.button("Tạo cây quyết định"):
                draw_decision_tree(data, measure)

        # Phân lớp mẫu
        st.subheader("Phân lớp cho mẫu")
        method = st.selectbox("Chọn thuật toán phân lớp", ["None", "Cây quyết định", "Naive Bayes"])
        if method != "None":
            features = {
                'Thời tiết': st.selectbox("Thời tiết", ['Nắng', 'U ám', 'Mưa']),
                'Nhiệt độ': st.selectbox("Nhiệt độ", ['Nóng', 'Ấm áp', 'Mát']),
                'Độ ẩm': st.selectbox("Độ ẩm", ['Cao', 'Vừa']),
                'Gió': st.selectbox("Gió", ['Có', 'Không'])
            }
            if st.button("Dự đoán"):
                classify_sample(data, method, features)
    else:
        st.success("✨ Vui lòng tải file CSV để tiếp tục! ✨")
