import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, OneHotEncoder
from assets.table.Dataframe_to_Table import draw_table


# Hàm xử lý dữ liệu
def identify_data_types(df):
    st.markdown("<div class='step-title'>Xác định loại thuộc tính</div>", unsafe_allow_html=True)
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
    st.markdown("<div class='step-title'>Xử lý dữ liệu bị thiếu</div>", unsafe_allow_html=True)
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



    draw_table(df)
    return df

def binning_and_smoothing(df, column):
    st.markdown("<div class='step-title'>Khử nhiễu bằng Binning và Smoothing</div>", unsafe_allow_html=True)
    bin_width = st.slider("Chọn độ rộng mỗi bin", min_value=5, max_value=20, value=20)
    bins = list(range(0, int(df[column].max()) + bin_width, bin_width))
    labels = [f"({bins[i]},{bins[i+1]}]" for i in range(len(bins)-1)]
    df["Binned_" + column] = pd.cut(df[column], bins=bins, labels=labels, include_lowest=True)
    smoothing_values = df.groupby("Binned_" + column)[column].mean()
    df["Smoothed_" + column] = df["Binned_" + column].map(smoothing_values)
                    # Chuyển DataFrame thành HTML với class để hiển thị bảng
    draw_table(df[[column, "Binned_" + column, "Smoothed_" + column]])
    return df




def discretize_column(df, column):
    st.markdown("<div class='step-title'>Rời rạc hóa thuộc tính</div>", unsafe_allow_html=True)
    bins = st.slider("Số lượng bins", min_value=3, max_value=10, value=4)
    labels = [f"Group {i+1}" for i in range(bins)]
    df["Discretized_" + column] = pd.cut(df[column], bins=bins, labels=labels)

    draw_table(df[[column, "Discretized_" + column]])
    return df

def one_hot_encoding(df, column):
    st.markdown("<div class='step-title'>One-hot Encoding cho thuộc tính</div>", unsafe_allow_html=True)
    encoder = OneHotEncoder(sparse=False)
    encoded = encoder.fit_transform(df[[column]])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out([column]))
    df = pd.concat([df, encoded_df], axis=1)

    draw_table(df)
    return df

def min_max_normalization(df, column):
    st.markdown("<div class='step-title'>Chuẩn hóa dữ liệu bằng Min-Max Normalization</div>", unsafe_allow_html=True)
    scaler = MinMaxScaler()
    df[column + "_Normalized"] = scaler.fit_transform(df[[column]])

    # Chuyển DataFrame thành HTML với class để hiển thị bảng
    draw_table(df[[column, column + "_Normalized"]])
    return df


def app():

        # Header với CSS container
    st.subheader("1️⃣. Chọn tệp tin:")
    uploaded_file = st.file_uploader("Tải file dữ liệu CSV", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.info("Dữ liệu đã tải lên:")

        # Chuyển DataFrame thành HTML với class để hiển thị bảng
        # st.markdown(custom_data_table_css, unsafe_allow_html=True)
        draw_table(df)
        # Button to trigger the dialog

        st.subheader("2️⃣. Xử lý dữ liệu")
        # Thực hiện các bước xử lý
        with st.container(border = 1):
            step1 = st.checkbox("1. Xác định loại thuộc tính")
            if step1:
                identify_data_types(df)
        with st.container(border=1):
            step2 = st.checkbox("2. Xử lý dữ liệu bị thiếu")
            if step2:
                df = fill_missing_values(df)
        with st.container(border=1):
            step3 = st.checkbox("3. Khử nhiễu (Binning & Smoothing)")
            if step3:
                column = st.selectbox("Chọn cột dữ liệu số", df.select_dtypes(include=['int64', 'float64']).columns)
                df = binning_and_smoothing(df, column)
        with st.container(border=1):
            step4 = st.checkbox("4. Rời rạc hóa dữ liệu")
            if step4:
                column = st.selectbox("Chọn cột để rời rạc hóa", df.select_dtypes(include=['int64', 'float64']).columns, key="discretize")
                df = discretize_column(df, column)
        with st.container(border=1):
            step5 = st.checkbox("5. One-hot Encoding")
            if step5:
                column = st.selectbox("Chọn cột categorical để encoding", df.select_dtypes(include=['object']).columns)
                df = one_hot_encoding(df, column)
        with st.container(border=1):
            step6 = st.checkbox("6. Chuẩn hóa dữ liệu")
            if step6:
                column = st.selectbox("Chọn cột để chuẩn hóa", df.select_dtypes(include=['int64', 'float64']).columns, key="normalize")
                df = min_max_normalization(df, column)

        # Tải xuống dữ liệu đã xử lý
        st.subheader("3️⃣. Tải xuống dữ liệu đã xử lý")
        processed_csv = df.to_csv(index=False).encode("utf-8-sig")
        if st.download_button("Tải file CSV", data=processed_csv, file_name="processed_data.csv", mime="text/csv"):
            st.toast('Tải xuống thành công!', icon='😍')
    else:
        st.warning("✨ Vui lòng tải file CSV để tiếp tục! ✨")