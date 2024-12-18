import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, OneHotEncoder

# CSS tùy chỉnh để làm đẹp giao diện
st.markdown(
    """
    <style>
        .main-header {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #FFB703;
            padding: 20px;
        }
            /* Tiêu đề */
        .container {
            width: 704px; 
            height: 101px;
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.52);
            border-radius: 60px;
            margin: 50px auto;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }
                
        .container h1 {
            font-size: 40px;  /* Chỉnh cỡ chữ tiêu đề lớn hơn */
            font-weight: 800px;
            text-align: center;
            margin: 0;
            color: white;
        }
        .data-header {
            text-align: left;
            font-size: 20px;
            font-weight: bold;
            color: #219EBC;
            padding: 10px;
        }
        .step-title {
            font-size: 18px;
            font-weight: bold;
            color: #023047;
            margin-top: 10px;
        }
        .css-button {
            background: linear-gradient(90deg, #126782, #219EBC);
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .css-button:hover {
            background: #FFB703;
            color: black;
        }
        .uploaded-file {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            font-size: 14px;
        }
        
    </style>
    """,
    unsafe_allow_html=True
)
# CSS tùy chỉnh cho bảng Dữ liệu đã tải lên
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

# Hàm xử lý dữ liệu
def identify_data_types(df):
    st.markdown("<div class='step-title'>1. Xác định loại thuộc tính</div>", unsafe_allow_html=True)
    data_types = {}
    for col in df.columns:
        if df[col].dtype == 'object':
            unique_vals = df[col].nunique()
            data_types[col] = "Categorical" if unique_vals > 2 else "Binary"
        elif df[col].dtype in ['int64', 'float64']:
            data_types[col] = "Numerical"
        else:
            data_types[col] = "Other"
    st.write(data_types)
    return data_types

def fill_missing_values(df):
    st.markdown("<div class='step-title'>2. Xử lý dữ liệu bị thiếu</div>", unsafe_allow_html=True)
    method = st.selectbox("Chọn phương pháp xử lý dữ liệu bị thiếu", ["Mean", "Median", "Mode"], key="missing_method")
    for col in df.columns:
        if df[col].isnull().any():
            if df[col].dtype in ['int64', 'float64']:
                if method == "Mean":
                    df[col].fillna(df[col].mean(), inplace=True)
                elif method == "Median":
                    df[col].fillna(df[col].median(), inplace=True)
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)
                # Chuyển DataFrame thành HTML với class để hiển thị bảng
    data_html = df.to_html(
        index=False,
        classes='data-table',  # Thêm class để áp dụng CSS
        border=0
    )
    # Hiển thị CSS và bảng HTML
    st.markdown(custom_data_table_css, unsafe_allow_html=True)
    st.markdown(
        f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)
    return df

def binning_and_smoothing(df, column):
    st.markdown("<div class='step-title'>3. Khử nhiễu bằng Binning và Smoothing</div>", unsafe_allow_html=True)
    bin_width = st.slider("Chọn độ rộng mỗi bin", min_value=5, max_value=20, value=20)
    bins = list(range(0, int(df[column].max()) + bin_width, bin_width))
    labels = [f"({bins[i]},{bins[i+1]}]" for i in range(len(bins)-1)]
    df["Binned_" + column] = pd.cut(df[column], bins=bins, labels=labels, include_lowest=True)
    smoothing_values = df.groupby("Binned_" + column)[column].mean()
    df["Smoothed_" + column] = df["Binned_" + column].map(smoothing_values)
                    # Chuyển DataFrame thành HTML với class để hiển thị bảng
    data_html = df[[column, "Binned_" + column, "Smoothed_" + column]].to_html(
        index=False,
        classes='data-table',  # Thêm class để áp dụng CSS
        border=0
    )
    # Hiển thị CSS và bảng HTML
    st.markdown(custom_data_table_css, unsafe_allow_html=True)
    st.markdown(
        f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)
    return df

def discretize_column(df, column):
    st.markdown("<div class='step-title'>4. Rời rạc hóa thuộc tính</div>", unsafe_allow_html=True)
    bins = st.slider("Số lượng bins", min_value=3, max_value=10, value=4)
    labels = [f"Group {i+1}" for i in range(bins)]
    df["Discretized_" + column] = pd.cut(df[column], bins=bins, labels=labels)
    
    data_html = df[[column, "Discretized_" + column]].to_html(
        index=False,
        classes='data-table',  # Thêm class để áp dụng CSS
        border=0
    )
    # Hiển thị CSS và bảng HTML
    st.markdown(custom_data_table_css, unsafe_allow_html=True)
    st.markdown(
        f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)
    return df

def one_hot_encoding(df, column):
    st.markdown("<div class='step-title'>5. One-hot Encoding cho thuộc tính</div>", unsafe_allow_html=True)
    encoder = OneHotEncoder(sparse=False)
    encoded = encoder.fit_transform(df[[column]])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out([column]))
    df = pd.concat([df, encoded_df], axis=1)
    
    st.dataframe(df, use_container_width=True)
    # Chuyển DataFrame thành HTML với class để hiển thị bảng
    # data_html = df.to_html(
    #     index=False,
    #     classes='data-table',  # Thêm class để áp dụng CSS
    #     border=0
    # )
    # # Hiển thị CSS và bảng HTML
    # st.markdown(custom_data_table_css, unsafe_allow_html=True)
    # st.markdown(
    #     f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)
    return df

def min_max_normalization(df, column):
    st.markdown("<div class='step-title'>6. Chuẩn hóa dữ liệu bằng Min-Max Normalization</div>", unsafe_allow_html=True)
    scaler = MinMaxScaler()
    df[column + "_Normalized"] = scaler.fit_transform(df[[column]])

    # Chuyển DataFrame thành HTML với class để hiển thị bảng
    data_html = df[[column, column + "_Normalized"]].to_html(
        index=False,
        classes='data-table',  # Thêm class để áp dụng CSS
        border=0
    )
    # Hiển thị CSS và bảng HTML
    st.markdown(custom_data_table_css, unsafe_allow_html=True)
    st.markdown(
        f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)
    return df


def app():

        # Header với CSS container

    uploaded_file = st.file_uploader("Tải file dữ liệu CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

                # Chuyển DataFrame thành HTML với class để hiển thị bảng
        data_html = df.to_html(
            index=False,
            classes='data-table',  # Thêm class để áp dụng CSS
            border=0
        )
        # Hiển thị CSS và bảng HTML
        st.markdown(custom_data_table_css, unsafe_allow_html=True)
        st.markdown(
            f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)

        # Thực hiện các bước xử lý
        step1 = st.checkbox("1. Xác định loại thuộc tính")
        if step1:
            identify_data_types(df)

        step2 = st.checkbox("2. Xử lý dữ liệu bị thiếu")
        if step2:
            df = fill_missing_values(df)

        step3 = st.checkbox("3. Khử nhiễu (Binning & Smoothing)")
        if step3:
            column = st.selectbox("Chọn cột dữ liệu số", df.select_dtypes(include=['int64', 'float64']).columns)
            df = binning_and_smoothing(df, column)

        step4 = st.checkbox("4. Rời rạc hóa dữ liệu")
        if step4:
            column = st.selectbox("Chọn cột để rời rạc hóa", df.select_dtypes(include=['int64', 'float64']).columns, key="discretize")
            df = discretize_column(df, column)

        step5 = st.checkbox("5. One-hot Encoding")
        if step5:
            column = st.selectbox("Chọn cột categorical để encoding", df.select_dtypes(include=['object']).columns)
            df = one_hot_encoding(df, column)

        step6 = st.checkbox("6. Chuẩn hóa dữ liệu")
        if step6:
            column = st.selectbox("Chọn cột để chuẩn hóa", df.select_dtypes(include=['int64', 'float64']).columns, key="normalize")
            df = min_max_normalization(df, column)

        # Tải xuống dữ liệu đã xử lý
        st.subheader("Tải xuống dữ liệu đã xử lý")
        processed_csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("Tải file CSV", data=processed_csv, file_name="processed_data.csv", mime="text/csv")
    else:
        st.markdown("<div class='uploaded-file'>Vui lòng tải file dữ liệu CSV để bắt đầu.</div>", unsafe_allow_html=True)