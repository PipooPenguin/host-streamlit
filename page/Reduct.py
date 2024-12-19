import streamlit as st
import pandas as pd
from assets.table.Dataframe_to_Table import draw_table
# Tiêu đề trang


def app():
    st.subheader("1️⃣. Chọn tệp tin:")
    uploaded_file = st.file_uploader("Tải lên file CSV", type=["csv"])

    if uploaded_file is not None:
        # Đọc dữ liệu từ file Excel
        try:
            df = pd.read_csv(uploaded_file)

            # Hiển thị bảng dữ liệu trên giao diện
            with st.container(border=1):
                st.info("Dữ liệu đã tải lên:")
                draw_table(df,long_table=0)
            # st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {e}")

        # Mapping dữ liệu định tính sang số
        mapping = {
            "Troi": {"Trong": 0, "May": 1 },
            "Gio": {"Bac": 0, "Nam": 1},
            "Apsuat": {"Cao": 1, "TB": 2, "Thap": 3},
            "Ketqua": {"Kmua": 0, "Mua": 1}
        }
        reverse_mapping = {col: {v: k for k, v in mapping.items()}
                           for col, mapping in mapping.items()}

        for col, col_mapping in mapping.items():
            if col in df.columns:
                df[col] = df[col].map(col_mapping)

        # Lấy danh sách các cột thuộc tính
        columns = df.columns.tolist()
        decision_column = columns[-1]  # Cột thuộc tính quyết định (cuối cùng)
        attributes = columns[1:-1]  # Các thuộc tính (trừ cột quyết định)
        st.subheader("2️⃣. Chọn cách tính muốn thực hiện:")
        with st.container(border=1):
            # Chọn cách tính muốn thực hiện
            selected_method = st.selectbox(
                "Chọn cách tính muốn thực hiện",
                ["Tính xấp xỉ", "Khảo sát sự phụ thuộc", "Tính các rút gọn"]
            )
            # Giao diện theo từng phương pháp
            if selected_method == "Tính xấp xỉ":
                # Chọn tập thuộc tính
                st.markdown(
                    '<label for="tap-thuoc-tinh">Chọn tập thuộc tính:</label>', unsafe_allow_html=True)
                selected_attributes = st.multiselect(
                    "Chọn tập thuộc tính", attributes)

                # Tạo từ điển ánh xạ ngược từ số sang chữ (reverse mapping)
                reverse_mapping_decision = {v: k for k,
                v in mapping[decision_column].items()}

                # Lấy danh sách các giá trị thuộc tính quyết định dưới dạng chữ
                unique_decision_values = [reverse_mapping_decision[val]
                                          for val in df[decision_column].dropna().unique()]

                # Hiển thị dropdown với giá trị chữ
                decision_value_label = st.selectbox(
                    "Chọn giá trị của thuộc tính quyết định",
                    unique_decision_values
                )

                # Chuyển giá trị được chọn từ chữ về số để tính toán
                decision_value = {v: k for k, v in reverse_mapping_decision.items()}[
                    decision_value_label]

            elif selected_method == "Khảo sát sự phụ thuộc":
                # Chọn tập thuộc tính
                st.markdown(
                    '<label for="tap-thuoc-tinh">Chọn tập thuộc tính:</label>', unsafe_allow_html=True)
                selected_attributes = st.multiselect(
                    "Chọn tập thuộc tính", attributes)

        # Nút tính toán
        if st.button("Thực hiện"):
            if selected_method == "Tính xấp xỉ":
                if not selected_attributes:
                    st.write("Vui lòng chọn tập thuộc tính.")
                else:
                    # Hàm tính xấp xỉ dưới
                    def approximation_lower(df, attributes, decision_value):
                        lower_indices = []
                        for idx, row in df.iterrows():
                            attribute_values = tuple(row[attributes])
                            subset = df[(df[attributes] == attribute_values).all(
                                axis=1)][decision_column]
                            if (subset == decision_value).all():
                                lower_indices.append(idx + 1)  # Lưu số thứ tự
                        return len(lower_indices), lower_indices

                    # Hàm tính xấp xỉ trên
                    def approximation_upper(df, attributes, decision_value):
                        upper_indices = []
                        for idx, row in df.iterrows():
                            attribute_values = tuple(row[attributes])
                            subset = df[(df[attributes] == attribute_values).all(
                                axis=1)][decision_column]
                            if decision_value in subset.values:
                                upper_indices.append(idx + 1)  # Lưu số thứ tự
                        return len(upper_indices), upper_indices

                    # Tính toán xấp xỉ
                    lower_count, lower_set = approximation_lower(
                        df, selected_attributes, decision_value)
                    upper_count, upper_set = approximation_upper(
                        df, selected_attributes, decision_value)
                    with st.container(border=1):
                        st.markdown("✨ **Kết quả:**")
                        st.info(f"**Xấp xỉ dưới:** {lower_count}  -  **tập giá trị:** {set(lower_set)}")
                        st.info(f"**Xấp xỉ trên:** {upper_count}  -  **tập giá trị:** {set(upper_set)}")

            elif selected_method == "Khảo sát sự phụ thuộc":
                if not selected_attributes:
                    st.write("Vui lòng chọn tập thuộc tính.")
                else:
                    # Lấy cột quyết định (cột cuối cùng)
                    decision_column = columns[-1]
                    df = df.dropna(subset=selected_attributes +
                                          [decision_column])  # Loại bỏ giá trị NaN

                    # Hàm tính xấp xỉ dưới
                    def approximation_lower(df, attributes, decision_column):
                        lower_set = []
                        for _, row in df.iterrows():
                            attribute_values = tuple(row[attributes])
                            decision_value = row[decision_column]
                            subset = df[(df[attributes] == attribute_values).all(
                                axis=1)][decision_column]
                            if (subset == decision_value).all():
                                lower_set.append(1)
                            else:
                                lower_set.append(0)
                        return sum(lower_set)

                    # Hàm tính xấp xỉ trên
                    def approximation_upper(df, attributes, decision_column):
                        upper_set = []
                        for _, row in df.iterrows():
                            attribute_values = tuple(row[attributes])
                            subset = df[(df[attributes] == attribute_values).all(
                                axis=1)][decision_column]
                            upper_set.append(len(subset))
                        return sum(upper_set)

                    # Tính toán theo phương pháp đã chọn
                    lower_approximation = approximation_lower(
                        df, selected_attributes, decision_column)
                    upper_approximation = approximation_upper(
                        df, selected_attributes, decision_column)

                    # Tính hệ số phụ thuộc
                    k = lower_approximation / \
                        len(df) if len(df) > 0 else 0  # Hệ số phụ thuộc
                    st.write(f"Hệ số phụ thuộc (k): {k:.2f}")

                    # Tính độ chính xác
                    accuracy = lower_approximation / \
                               upper_approximation if upper_approximation != 0 else 0
                    st.write(f"Độ chính xác: {accuracy:.2f}")

            elif selected_method == "Tính các rút gọn":
                # Loại bỏ cột đầu tiên để không xét nó khi tìm rút gọn
                columns = df.columns
                decision_column = columns[-1]  # Cột quyết định
                # Chỉ lấy các thuộc tính (bỏ cột đầu tiên và cột quyết định)
                attributes = columns[1:-1]

                # Hàm tìm rút gọn (reduct)

                def find_reducts(df, decision_column, attributes):
                    reducts = []  # Danh sách các tập rút gọn

                    # Lấy tất cả các tổ hợp thuộc tính (rút gọn)
                    from itertools import combinations
                    for r in range(1, len(attributes) + 1):
                        for subset in combinations(attributes, r):
                            # Kiểm tra nếu tập thuộc tính này có khả năng phân biệt tất cả các đối tượng
                            grouped = df.groupby(list(subset))[
                                decision_column].nunique()
                            if grouped.eq(1).all():
                                reducts.append(set(subset))  # Lưu tập rút gọn

                    # Loại bỏ các tập dư thừa (không cần thiết)
                    minimal_reducts = []
                    for reduct in reducts:
                        if not any(reduct > other for other in reducts if reduct != other):
                            minimal_reducts.append(reduct)
                    return minimal_reducts

                # Hàm tạo luật phân lớp với dữ liệu được chuyển về dạng chữ
                def generate_classification_rules_with_reverse_mapping(df, reduct, decision_column, reverse_mapping):
                    rules = []
                    # Lọc dữ liệu theo tập rút gọn
                    for _, subset in df.groupby(list(reduct)):
                        # Tìm giá trị duy nhất của cột quyết định
                        decision_values = subset[decision_column].unique()
                        if len(decision_values) == 1:  # Đảm bảo chỉ có 1 giá trị duy nhất
                            decision_value = decision_values[0]
                            # Chuyển giá trị số sang chữ dựa trên reverse_mapping
                            decision_label = reverse_mapping[decision_column].get(
                                decision_value, decision_value)

                            # Tạo điều kiện với dữ liệu đã chuyển về dạng chữ
                            conditions = " AND ".join(
                                [
                                    f"{col} = '{reverse_mapping[col].get(subset[col].iloc[0], subset[col].iloc[0])}'"
                                    for col in reduct
                                ]
                            )
                            rules.append(f"IF {conditions} THEN {decision_column} = '{decision_label}'")
                    return rules

                # Tìm các rút gọn
                reducts = find_reducts(df, decision_column, attributes)

                # Hiển thị kết quả
                st.write("Kết quả:")
                if reducts:
                    st.write("Các rút gọn tìm được:")
                    for reduct in reducts:
                        st.write(", ".join(reduct))

                    # Chọn tập rút gọn đầu tiên để tạo luật phân lớp
                    reduct = list(reducts[0])  # Lấy rút gọn đầu tiên
                    classification_rules = generate_classification_rules_with_reverse_mapping(
                        df, reduct, decision_column, reverse_mapping
                    )

                    # Hiển thị 3 luật phân lớp đầu tiên
                    st.write("Đề xuất các luật phân lớp chính xác 100%:")
                    for rule in classification_rules[:3]:
                        st.write(rule)
                else:
                    st.write("Không tìm thấy rút gọn.")
    else:
        st.warning("✨ Vui lòng tải file CSV để tiếp tục! ✨")
