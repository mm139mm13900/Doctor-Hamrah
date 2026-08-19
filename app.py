import streamlit as st

st.set_page_config(page_title="دکتر همراه", page_icon="💉")

st.title("🩺 Doctor Hamrah")
st.subheader("مدیریت هوشمند قند خون")

with st.form("my_form"):
    blood_sugar = st.number_input("میزان قند خون خود را وارد کنید:", min_value=50, max_value=400)
    submit_button = st.form_submit_button(label='ثبت اطلاعات')

if submit_button:
    st.success(f"مقدار {blood_sugar} با موفقیت ثبت شد!")
  
