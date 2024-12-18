import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

def app():
    # Load data
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

    st.markdown("<div class='file-uploader'><strong>1. Chọn tệp tin:</strong></div>",
                unsafe_allow_html=True)
    file = st.file_uploader("Chọn tệp dữ liệu (CSV hoặc XLSX)", type=['csv', 'xlsx'])

    # Kiểm tra data
    if file is not None:
        try:
            # Đọc file
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)

            # Kiểm tra dữ liệu
            if "Ma hoa don" not in df.columns or "Ma hang" not in df.columns:
                st.markdown(
                    "<p class='error'>Tệp tin cần có các cột: 'Ma hoa don' và 'Ma hang'.</p>", unsafe_allow_html=True)
            else:
                st.write("**Dữ liệu đã tải lên:**")

                st.markdown(custom_data_table_css, unsafe_allow_html=True)
                data_html = df.to_html(
                    index=False,
                    classes='data-table',  # Thêm class để áp dụng CSS
                    border=0
                )
                st.markdown(f"<table class='data-table-container'>{data_html}</table>", unsafe_allow_html=True)

                # Chọn cách tính muốn thực hiện
                st.markdown("### 2. Chọn cách tính muốn thực hiện:")
                option = st.selectbox(
                    "Chọn thuật toán bạn muốn thực hiện:",
                    options=["", "Tìm tập phổ biến","Tìm tập phổ biến tối đại", "Tìm luật kết hợp"])

                # Các tham số đầu vào
                if option in ["Tìm tập phổ biến", "Tìm tập phổ biến tối đại"]:
                    minsupp = st.number_input(
                        "Nhập giá trị min_sup (0.01 - 1.0):",
                        min_value=0.01, max_value=1.0, value=0.1, step=0.01
                    )
                elif option == "Tìm luật kết hợp":
                    minsupp = st.number_input(
                        "Nhập giá trị min_sup (0.01 - 1.0):",
                        min_value=0.01, max_value=1.0, value=0.1, step=0.01
                    )
                    mincoff = st.number_input(
                        "Nhập giá trị min_coff (0.01 - 1.0):",
                        min_value=0.01, max_value=1.0, value=0.5, step=0.01
                    )

                # Nút chạy thuật toán
                if st.button("Chạy thuật toán"):
                    # Tiền xử lý dữ liệu
                    transactions = df.groupby('Ma hoa don')[
                        'Ma hang'].apply(list).tolist()
                    te = TransactionEncoder()
                    te_ary = te.fit(transactions).transform(transactions)
                    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

                    # Thực thi thuật toán
                    if option == "Tìm tập phổ biến":
                        frequent_itemsets = apriori(
                            df_encoded, min_support=minsupp, use_colnames=True)
                        st.markdown(
                            "<div class='result-container'><strong>Các tập phổ biến: </strong></div>", unsafe_allow_html=True)
                        data_html = frequent_itemsets.to_html(
                            index=False,
                            classes='data-table',  # Thêm class để áp dụng CSS
                            border=0
                        )
                        st.markdown(f"<table class='data-table-container'>{data_html}</table>", unsafe_allow_html=True)

                    elif option == "Tìm tập phổ biến tối đại":
                        frequent_itemsets = apriori(
                            df_encoded, min_support=minsupp, use_colnames=True)

                        # Tìm các tập phổ biến tối đại
                        max_itemsets = []
                        for idx, itemset in frequent_itemsets.iterrows():
                            itemset_list = list(itemset['itemsets'])
                            is_maximal = True
                            for sub_idx, sub_itemset in frequent_itemsets.iterrows():
                                # Kiểm tra nếu tập con lớn hơn tập hiện tại và cũng là tập phổ biến
                                if len(itemset_list) < len(sub_itemset['itemsets']) and set(itemset_list).issubset(sub_itemset['itemsets']):
                                    is_maximal = False
                                    break
                            if is_maximal:
                                max_itemsets.append(itemset)

                        max_itemsets_df = pd.DataFrame(max_itemsets)
                        st.markdown(
                            "<div class='result-container'><strong>Các tập phổ biến tối đại: </strong></div>", unsafe_allow_html=True)
                        st.markdown(f"<table class='dataframe'>{max_itemsets_df.to_html(index=False)}</table>", unsafe_allow_html=True)

                    elif option == "Tìm luật kết hợp":
                        # Tìm tập phổ biến
                        frequent_itemsets = apriori(df_encoded, min_support=minsupp, use_colnames=True)

                        if frequent_itemsets.empty:
                            st.warning("Không có tập phổ biến nào thỏa mãn ngưỡng min_sup đã chọn.")
                        else:
                            # Tìm tập phổ biến tối đại
                            max_itemsets = []
                            for idx, itemset in frequent_itemsets.iterrows():
                                itemset_list = list(itemset['itemsets'])
                                is_maximal = True
                                for sub_idx, sub_itemset in frequent_itemsets.iterrows():
                                    if len(itemset_list) < len(sub_itemset['itemsets']) and set(itemset_list).issubset(sub_itemset['itemsets']):
                                        is_maximal = False
                                        break
                                if is_maximal:
                                    max_itemsets.append(itemset)

                            max_itemsets_df = pd.DataFrame(max_itemsets)

                            if max_itemsets_df.empty:
                                st.warning("Không có tập phổ biến tối đại nào.")
                            else:
                                try:
                                    # Tính toán luật kết hợp
                                    num_itemsets = len(frequent_itemsets)  # Cung cấp số lượng itemsets
                                    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=mincoff)

                                    # Lọc các luật kết hợp có antecedents và consequents thuộc tập phổ biến tối đại
                                    filtered_rules = rules[
                                        rules['antecedents'].apply(lambda x: any(frozenset(x).issubset(fs) for fs in max_itemsets_df['itemsets'])) &
                                        rules['consequents'].apply(lambda x: any(frozenset(x).issubset(fs) for fs in max_itemsets_df['itemsets']))
                                    ]

                                    # Kiểm tra nếu không có luật thỏa mãn
                                    if filtered_rules.empty:
                                        st.warning("Không có luật kết hợp nào thỏa mãn ngưỡng min_cof và lift > 1.")
                                    else:
                                        # Chỉ giữ lại các cột cần thiết
                                        filtered_rules = filtered_rules[['antecedents', 'consequents', 'confidence']]

                                        st.markdown(
                                            "<div class='result-container'><strong> Các luật kết hợp từ tập phổ biến tối đại</strong></div>",
                                            unsafe_allow_html=True
                                        )
                                        st.markdown(f"<table class='dataframe'>{filtered_rules.to_html(index=False)}</table>", unsafe_allow_html=True)

                                except Exception as e:
                                    st.error(f"Đã xảy ra lỗi khi tìm luật kết hợp: {e}")

        except Exception as e:
            st.error(f"Đã có lỗi xảy ra: {e}")
