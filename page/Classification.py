# Import thư viện
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
import graphviz
from assets.table.Dataframe_to_Table import draw_table

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
    st.graphviz_chart(graphviz.Source(dot_data),use_container_width =1)

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
        st.markdown("✨ **:blue[Dự đoán:]**")
        st.info(f" **Lớp '{class_label}'**")
    except Exception as e:
        st.error(f"Lỗi: {e}")

# Ứng dụng chính
def app():
    st.subheader("1️⃣. Chọn tệp tin:")
    uploaded_file = st.file_uploader("Tải file dữ liệu (CSV):", type=["csv"])
    if uploaded_file:
        with st.container(border=1):
            data = pd.read_csv(uploaded_file)
            st.info("Dữ liệu đã tải lên:")
            draw_table(data)

        # Vẽ cây quyết định
        st.subheader("2️⃣. Vẽ cây quyết định:")
        with st.container(border=1):
            algorithm = st.selectbox("Chọn thuật toán", ["None", "Thuật toán ID3"])
            if algorithm == "Thuật toán ID3":
                measure = st.radio("Chọn độ đo:", ["Độ lợi thông tin", "Chỉ số Gini"])
            if st.button("Tạo cây quyết định"):
                draw_decision_tree(data, measure)

        # Phân lớp mẫu
        st.subheader("3️⃣. Phân lớp cho mẫu:")
        with st.container(border=1):
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
        st.warning("✨ Vui lòng tải file CSV để tiếp tục! ✨")
