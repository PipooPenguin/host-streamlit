# cd D:\NAM3\HK1\DataMining\DOAN\IS252.P11-DataMining\page
# streamlit run Cluster.py
# Import thư viện

import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from minisom import MiniSom
import numpy as np
import matplotlib.pyplot as plt
# from assets.table.Dataframe_to_Table import draw_table

def app():
    # Upload file CSV
    st.subheader("1️⃣. Chọn tệp tin:")
    uploaded_file = st.file_uploader("Tải file dữ liệu (CSV):", type=["csv"])
    if uploaded_file:
        # Nếu file đã được tải lên
        data = pd.read_csv(uploaded_file, sep=';')
    # CSS tùy chỉnh cho bảng Dữ liệu đã tải lên
        st.info("Dữ liệu đã tải lên:")

        # Chuyển DataFrame thành HTML với class để hiển thị bảng
        data_html = data.to_html(
            index=False,
            classes='data-table',  # Thêm class để áp dụng CSS
            border=0
        )
        # Hiển thị CSS và bảng HTML
        with st.container(border=0):
            st.markdown(
                f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)
        st.subheader("2️⃣. Chọn thuật toán gom cụm:")

        # Chọn thuật toán
        with st.container(border=1):
            algorithm = st.selectbox("Chọn thuật toán:", ["K-means", "Kohonen"],label_visibility ="hidden")

    # Hiển thị kết quả K-means
            if algorithm == "K-means":
                num_clusters = st.number_input(
                    "Số cụm (k):", min_value=1, max_value=20, step=1, value=3)
                if st.button("Thực hiện K-means", key="kmeans"):
                    # Thực hiện K-means
                    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
                    kmeans.fit(data)
                    data["Gom cụm"] = kmeans.labels_

                    # Hiển thị kết quả
                    data['Gom cụm'] = kmeans.labels_  # Thêm nhãn cụm vào dữ liệu

                    # Hiển thị tiêu đề
                    st.info("✨ **Kết quả K-means:**")

                    # CSS tùy chỉnh cho bảng K-means

                    # Chuyển đổi dataframe thành HTML với class

                    data_html = data.to_html(
                        index=False,
                        classes='data-table',  # Thêm class để áp dụng CSS
                        border=0
                    )
                    # Hiển thị CSS và bảng HTML
                    with st.container(border=0):
                        st.markdown(
                            f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)
                    # Hiển thị Vector trọng tâm dưới dạng bảng

                    st.info("✨ **Vector trọng tâm:**")

                    # Chuyển đổi các vector trọng tâm thành DataFrame
                    centroids = kmeans.cluster_centers_  # Vector trọng tâm

                    # Đổi tên cột cho phù hợp với yêu cầu
                    # Giả sử dữ liệu có 2 chiều (x, y)
                    centroids_df = pd.DataFrame(centroids, columns=["x", "y"])
                    centroids_df.insert(0, 'Trọng tâm các cụm', [ f'Cụm {i+1}' for i in range(len(centroids_df))])

                    data_html = centroids_df.to_html(
                        index=False,
                        classes='data-table',  # Thêm class để áp dụng CSS
                        border=0
                    )
                    # Hiển thị CSS và bảng HTML
                    with st.container(border=0):
                        st.markdown(
                            f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)
                    # Hiển thị biểu đồ K-means
                    st.info("✨ **Biểu đồ K-means:**")
                    plt.figure(figsize=(8, 6))
                    plt.scatter(data.iloc[:, 0], data.iloc[:, 1],  c=kmeans.labels_, cmap='viridis')
                    plt.title("K-means Clustering")
                    plt.xlabel(data.columns[0])
                    plt.ylabel(data.columns[1])
                    plt.colorbar(label='Cluster')
                    st.pyplot(plt)

            elif algorithm == "Kohonen":
                map_width = st.number_input(
                    "Chiều rộng bản đồ (Width):", min_value=1, step=1, value=5)
                map_height = st.number_input(
                    "Chiều cao bản đồ (Height):", min_value=1, step=1, value=5)
                num_epochs = st.number_input(
                    "Số lần lặp (Epochs):", min_value=1, step=1, value=100)
                alpha = st.number_input("Tốc độ học (Alpha):",min_value=0.01, max_value=1.0, step=0.01, value=0.5)
                neighborhood_radius = st.number_input("Bán kính vùng lân cận:", min_value=1, step=1, value=2)

                if st.button("Thực hiện Kohonen", key="kohonen"):
                    # Chuẩn bị dữ liệu
                    data_values = data.values
                    data_values = (data_values - np.mean(data_values, axis=0)) / np.std(data_values, axis=0)

                    # Huấn luyện Kohonen SOM
                    som = MiniSom(map_width, map_height,
                                  data_values.shape[1], sigma=neighborhood_radius, learning_rate=alpha)
                    som.random_weights_init(data_values)
                    som.train_random(data_values, num_epochs)

                    # Gắn cụm
                    # each label is a tuple (x, y) coordinate
                    labels = [som.winner(x) for x in data_values]
                    # Creating a string key for clusters
                    data["Gom cụm"] = [f"{x[0]}-{x[1]}" for x in labels]


                    st.info("✨ **Kết quả Kohonen:**")
                    # Chuyển đổi dữ liệu thành HTML bảng với CSS tùy chỉnh

                    # Chuyển đổi dataframe thành HTML với class
                    data_html = data.to_html(
                        index=False,
                        classes='data-table',  # Thêm class để áp dụng CSS
                        border=0
                    )
                    # Hiển thị CSS và bảng HTML
                    with st.container(border=0):
                        st.markdown(
                            f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)
                # Tiêu đề bảng
                    st.info("✨ **Trọng số các nút:**")

                    # Lấy trọng số từ SOM và chuyển thành DataFrame
                    weights_matrix = som.get_weights()
                    weights_df = pd.DataFrame(
                        [
                            {f"Nút {j}": [round(w, 4) for w in weights] for j, weights in enumerate(weights_matrix[i])}
                            for i in range(len(weights_matrix))
                        ]
                    )

                    # Tạo bảng HTML từ DataFrame
                    data_html = weights_df.to_html(
                        index=False,
                        classes='data-table',  # Thêm class để áp dụng CSS
                        border=0
                    )
                    # Hiển thị CSS và bảng HTML
                    with st.container(border=0):
                        st.markdown(
                            f'<div class="data-table-container">{data_html}</div>', unsafe_allow_html=True)
                    # Hiển thị nhận xét
                    st.success("""
                    Chú thích:
                    - Mỗi hàng trong bảng tương ứng với một hàng (row) trên bản đồ Kohonen.
                    - Các cột trong bảng tương ứng với các nút trên bản đồ, với mỗi nút có một vector trọng số (weights).
                    - Sự khác biệt giữa các giá trị trọng số cho thấy cách SOM đã học và tổ chức dữ liệu. 
                    - Các nút gần nhau trên bản đồ Kohonen thường có giá trị trọng số tương tự, phản ánh dữ liệu trong các cụm liên quan.
                    """)

                    # Hiển thị biểu đồ Kohonen SOM
                    st.info("✨ **Biểu đồ Kohonen SOM:**")

                    plt.figure(figsize=(8, 6))

                    # Flatten the coordinates of the labels
                    # x-coordinate from (x, y) tuples
                    x_vals = [label[0] for label in labels]
                    # y-coordinate from (x, y) tuples
                    y_vals = [label[1] for label in labels]

                    # Color map based on clusters
                    cluster_labels = [som.winner(x)[0] * som.get_weights().shape[1] + som.winner(x)[
                        1] for x in data_values]  # flatten cluster index
                    plt.scatter(x_vals, y_vals, c=cluster_labels,cmap='viridis', marker='o')

                    plt.title("Kohonen SOM Clustering")
                    plt.xlabel("X")
                    plt.ylabel("Y")
                    plt.colorbar(label='Cluster')
                    st.pyplot(plt)
    else:
        st.warning("✨ Vui lòng tải file CSV để tiếp tục! ✨")

