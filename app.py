import streamlit as st
import time
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Streamlit Caching Demo",
    page_icon="⏱️",
    layout="centered"
)

st.title("⏱️ Demo Xử lý Tác vụ Chạy Lâu với Caching")
st.markdown("Sử dụng `@st.cache_data` để ngăn tác vụ chạy lại không cần thiết.")
st.markdown("---")

# ----------------------------------------------------
# 1. Định nghĩa Hàm chạy lâu và áp dụng CACHING
# ----------------------------------------------------
@st.cache_data
def load_heavy_data(num_rows, delay_time):
    """
    Hàm mô phỏng việc tải dữ liệu hoặc tính toán nặng.
    Nó chỉ chạy 1 LẦN duy nhất trừ khi tham số đầu vào thay đổi.
    """
    # Mô phỏng độ trễ (Delay)
    st.info(f"Đang thực hiện tác vụ nặng... (Chờ {delay_time} giây)")
    time.sleep(delay_time) 
    
    # Tạo một DataFrame lớn
    data = pd.DataFrame(
        np.random.randn(num_rows, 5),
        columns=['A', 'B', 'C', 'D', 'E']
    )
    st.success("Tác vụ nặng đã hoàn thành và kết quả đã được lưu cache! 🎉")
    return data

# ----------------------------------------------------
# 2. Giao diện người dùng
# ----------------------------------------------------

# Widget để thay đổi input (tham số của hàm load_heavy_data)
st.subheader("Tham số đầu vào (Inputs)")
N_ROWS = st.slider(
    "Chọn số lượng hàng dữ liệu:",
    min_value=100,
    max_value=10000,
    step=100,
    value=1000,
    key="rows"
)

# Nút để kích hoạt việc chạy lại (Re-run)
if st.button("Chạy lại (Rerun Script)", key="rerun_button"):
    st.toast("Đang chạy lại toàn bộ script...")
    
# Ghi chú về thời gian delay (thời gian mô phỏng tác vụ nặng)
DELAY = 5

# ----------------------------------------------------
# 3. Gọi hàm và xử lý Loading State
# ----------------------------------------------------

st.subheader("Kết quả Tác vụ")

# Sử dụng st.spinner để hiển thị trạng thái "đang tải" trong lần chạy đầu tiên
start_time = time.time()
with st.spinner(f"Đang tải hoặc tính toán (chờ {DELAY}s)..."):
    # Gọi hàm đã được cache. 
    # Tác vụ sleep(5) chỉ chạy trong lần đầu tiên hoặc khi N_ROWS thay đổi.
    data_frame = load_heavy_data(N_ROWS, DELAY)

end_time = time.time()
duration = end_time - start_time

st.metric(
    label="Thời gian thực thi",
    value=f"{duration:.2f} giây"
)

st.write(f"Đã tải DataFrame với {N_ROWS} hàng:")
st.dataframe(data_frame.head())

st.markdown("---")
st.markdown("""
### 💡 Thử nghiệm:
1. **Lần 1:** Chạy lần đầu sẽ mất khoảng 5 giây.
2. **Lần 2 (Bấm nút 'Rerun'):** Bấm nút "Chạy lại (Rerun Script)". Thời gian thực thi sẽ rất nhanh (khoảng 0.01 giây) vì kết quả được lấy từ cache.
3. **Lần 3 (Thay đổi Slider):** Thay đổi giá trị trên thanh trượt "Số lượng hàng dữ liệu". Hàm sẽ chạy lại 5 giây vì đầu vào (`num_rows`) đã thay đổi.
""")