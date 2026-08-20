import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# ۱. تنظیمات صفحه
st.set_page_config(page_title="Doctor Hamrah", page_icon="🩺")

# ۲. نمایش لوگو (مطمئن شو فایل لوگو در کنار app.py هست)
try:
    logo = Image.open("image_gen_679ec72c-71c0-4150-8b7a-41ace0bf9013_0.png")
    st.image(logo, width=150)
except:
    st.title("🩺 Doctor Hamrah")

st.write("### خوش آمدید به دکتر همراه")
st.write("در اینجا می‌توانید روند قند خون خود را مدیریت کنید.")

# ۳. ایجاد داده‌های نمونه برای نمایش نمودار
# در آینده این داده‌ها از فایل یا دیتابیس خوانده می‌شوند
data = {
    'تاریخ': pd.to_datetime(['2026-08-15', '2026-08-16', '2026-08-17', '2026-08-18', '2026-08-19']),
    'قند خون (mg/dL)': [95, 110, 130, 105, 98]
}
df = pd.DataFrame(data)

# ۴. بخش ورودی کاربر (فرم ساده)
st.sidebar.header("ثبت داده جدید")
new_value = st.sidebar.number_input("مقدار قند خون را وارد کنید:", min_value=40, max_value=400, value=100)
if st.sidebar.button("ثبت"):
    st.sidebar.success(f"مقدار {new_value} با موفقیت ثبت شد! (فعلاً فقط نمایش داده می‌شود)")

# ۵. نمایش نمودار
st.subheader("📈 نمودار روند قند خون")
fig, ax = plt.subplots()
ax.plot(df['تاریخ'], df['قند خون (mg/dL)'], marker='o', linestyle='-', color='red')
ax.set_xlabel("تاریخ")
ax.set_ylabel("قند خون (mg/dL)")
ax.grid(True)

# تنظیمات برای نمایش بهتر تاریخ در نمودار
plt.xticks(rotation=45)

st.pyplot(fig)

# نمایش جدول داده‌ها
if st.checkbox("نمایش جدول داده‌ها"):
    st.dataframe(df)
