import streamlit as st

# Thiết lập tiêu đề trang
st.set_page_config(
    page_title="Máy Tính BMI Đơn Giản",
    page_icon="⚖️",
    layout="centered"
)

# Hàm tính toán chỉ số BMI
def calculate_bmi(weight, height, unit):
    """Tính BMI dựa trên đơn vị được chọn."""
    if unit == "Metric (kg, m)":
        # Công thức: kg / (m^2)
        if height == 0:
            return 0
        return weight / (height ** 2)
    elif unit == "Imperial (lbs, ft)":
        # Công thức: (lbs / (in^2)) * 703
        if height == 0:
            return 0
        # Chuyển đổi feet sang inch
        height_in_inches = height * 12
        return (weight / (height_in_inches ** 2)) * 703

# Hàm phân loại chỉ số BMI
def classify_bmi(bmi):
    """Phân loại tình trạng sức khỏe dựa trên chỉ số BMI."""
    if bmi == 0:
        return "Vui lòng nhập số liệu hợp lệ"
    elif bmi < 18.5:
        return "Thiếu cân (Underweight)"
    elif 18.5 <= bmi < 24.9:
        return "Cân nặng khỏe mạnh (Healthy Weight)"
    elif 25 <= bmi < 29.9:
        return "Thừa cân (Overweight)"
    else:
        return "Béo phì (Obesity)"

# --- Giao diện người dùng ---

st.title("⚖️ Máy Tính Chỉ Số BMI (Body Mass Index)")
st.markdown("---")

# 1. Chọn hệ thống đơn vị
unit_system = st.radio(
    "Chọn hệ thống đo lường:",
    ["Metric (kg, m)", "Imperial (lbs, ft)"],
    key="unit_select"
)

# 2. Nhập dữ liệu dựa trên đơn vị được chọn
if unit_system == "Metric (kg, m)":
    st.subheader("Hệ Mét (Metric System)")
    weight = st.slider("Cân nặng (kg):", 20.0, 200.0, 70.0, 0.5, key="weight_kg")
    height = st.slider("Chiều cao (m):", 1.0, 2.5, 1.75, 0.01, key="height_m")
elif unit_system == "Imperial (lbs, ft)":
    st.subheader("Hệ Anh (Imperial System)")
    weight = st.slider("Cân nặng (lbs):", 50.0, 450.0, 150.0, 0.5, key="weight_lbs")
    
    # Chia thanh trượt cho Feet và Inches để dễ nhập hơn
    col1, col2 = st.columns(2)
    with col1:
        feet = st.slider("Chiều cao (feet):", 3, 8, 5, key="height_ft")
    with col2:
        inches = st.slider("Chiều cao (inches):", 0, 11, 10, key="height_in")
        
    # Chuyển đổi sang đơn vị tính toán: Tổng số feet
    # Trong công thức Imperial, cần inch, nhưng Streamlit Community Cloud sẽ dùng công thức này
    height = feet + (inches / 12) 


# --- Hiển thị kết quả ---
st.markdown("---")

# Tính toán
if unit_system == "Metric (kg, m)":
    bmi_value = calculate_bmi(weight, height, unit_system)
    
elif unit_system == "Imperial (lbs, ft)":
    # Phải chuyển đổi lại chiều cao sang inch cho hàm tính toán chính xác
    height_in_inches = (feet * 12) + inches
    bmi_value = (weight / (height_in_inches ** 2)) * 703 if height_in_inches > 0 else 0


classification = classify_bmi(bmi_value)

# Hiển thị
st.metric(
    label="Chỉ số BMI của bạn là:", 
    value=f"{bmi_value:.2f}"
)

# Hiển thị phân loại với màu sắc
if "Thiếu cân" in classification:
    st.warning(f"Tình trạng: **{classification}**")
elif "khỏe mạnh" in classification:
    st.success(f"Tình trạng: **{classification}**")
elif "Thừa cân" in classification:
    st.error(f"Tình trạng: **{classification}**")
elif "Béo phì" in classification:
    st.error(f"Tình trạng: **{classification}**")
else:
    st.info(f"Tình trạng: **{classification}**")

st.markdown("""
<div style='text-align: center; margin-top: 20px;'>
    <small>Chỉ số BMI được sử dụng để phân loại cân nặng dựa trên chiều cao và cân nặng.</small>
</div>
""", unsafe_allow_html=True)