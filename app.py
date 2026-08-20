import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="دکتر همراه", page_icon="🩺")
st.title("🩺 دکتر همراه")
st.caption("دستیار هوشمند مدیریت قند خون")

# محدوده نرمال قند خون بر اساس زمان اندازه‌گیری
normal_ranges = {
    "ناشتا": (70, 100),
    "قبل از غذا": (70, 110),
    "۲ ساعت بعد از غذا": (70, 140),
    "قبل از خواب": (90, 140),
}

if "records" not in st.session_state:
    st.session_state.records = []

def get_verdict(value, timing):
    low, high = normal_ranges[timing]
    if value < low:
        return "low", "🔴 قند پایین (هیپوگلیسمی)", "#d63031", (
            "پیشنهاد: یک خوراکی کوچک مثل خرما یا آب‌میوه بخورید و بعد از ۱۵ دقیقه "
            "دوباره اندازه بگیرید. اگر حال‌تان بهتر نشد، با پزشک تماس بگیرید."
        )
    if value > high:
        return "high", "🟠 قند بالا (هیپرگلیسمی)", "#e17055", (
            "پیشنهاد: آب بنوشید، پیاده‌روی سبک کنید و دارو را طبق دستور پزشک مصرف کنید. "
            "اگر چند بار پیاپی بالا بود، پزشک خود را در جریان بگذارید."
        )
    return "normal", "🟢 قند نرمال", "#00b894", (
        "آفرین! قند خون شما در محدوده سالم است. دارو، رژیم غذایی و فعالیت بدنی را منظم ادامه دهید."
    )

st.subheader("📝 ثبت قند خون")
with st.form("blood_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    value = c1.number_input("مقدار قند خون (mg/dL)", min_value=20, max_value=600, value=100, step=1)
    timing = c2.selectbox("زمان اندازه‌گیری", list(normal_ranges.keys()))
    submitted = st.form_submit_button("ثبت و تحلیل هوشمند")

if submitted:
    cat, label, color, advice = get_verdict(value, timing)
    st.session_state.records.append({
        "time": datetime.now().strftime("%H:%M"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "value": value,
        "timing": timing,
        "cat": cat,
    })
    st.markdown(
        f'<div style="background:{color}; padding:12px; border-radius:10px; '
        f'color:white; text-align:center; font-size:18px;">{label}</div>',
        unsafe_allow_html=True
    )
    st.info(advice)

if st.session_state.records:
    st.divider()
    st.subheader("🤖 تحلیل هوشمند")
    df = pd.DataFrame(st.session_state.records)

    avg = df["value"].mean()
    in_range_pct = (df["cat"] == "normal").mean() * 100
    hba1c = (avg + 46.7) / 28.7

    colA, colB, colC = st.columns(3)
    colA.metric("میانگین قند خون", f"{avg:.0f} mg/dL")
    colB.metric("درصد در محدوده نرمال", f"{in_range_pct:.0f}٪")
    colC.metric("برآورد HbA1c", f"{hba1c:.1f}٪")

    # روند تغییرات
    last_two = df["value"].tail(2).tolist()
    if len(last_two) == 2:
        diff = last_two[-1] - last_two[-2]
        if diff > 10:
            trend = "📈 روند صعودی (قند در حال بالا رفتن است)"
        elif diff < -10:
            trend = "📉 روند نزولی (قند در حال پایین آمدن است)"
        else:
            trend = "➡️ روند تقریباً ثابت"
        st.write(trend)

    # امتیاز خطر
    risk = 0
    if avg > 130:
        risk += 2
    elif avg > 110:
        risk += 1
    if in_range_pct < 70:
        risk += 2
    elif in_range_pct < 90:
        risk += 1
    if hba1c > 6.5:
        risk += 1

    if risk <= 1:
        risk_label = "🟢 خطر کم — کنترل عالی است"
    elif risk <= 3:
        risk_label = "🟡 خطر متوسط — نیاز به دقت بیشتر"
    else:
        risk_label = "🔴 خطر بالا — حتماً با پزشک مشورت کنید"
    st.success(risk_label)

    # نمودار روند
    st.subheader("📊 نمودار روند قند خون")
    fig, ax = plt.subplots(figsize=(8, 4))
    color_map = {"normal": "#00b894", "high": "#e17055", "low": "#d63031"}
    ax.plot(df["time"], df["value"], color="#0984e3", linewidth=1.2, alpha=0.7)
    for cat_name in ["normal", "high", "low"]:
        part = df[df["cat"] == cat_name]
        if not part.empty:
            ax.scatter(part["time"], part["value"], color=color_map[cat_name], s=70, zorder=5, label=cat_name)
    ax.axhline(70, color="#d63031", linestyle="--", alpha=0.5, label="low limit (70)")
    ax.axhline(140, color="#e17055", linestyle="--", alpha=0.5, label="high limit (140)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Blood Sugar (mg/dL)")
    ax.set_title("Blood Sugar Trend")
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)

    # جدول ثبت‌ها
    st.subheader("📋 جدول اندازه‌گیری‌ها")
    show = df.rename(columns={
        "time": "ساعت", "date": "تاریخ", "value": "قند خون", "timing": "زمان", "cat": "وضعیت"
    })
    show["وضعیت"] = show["وضعیت"].map({"normal": "✅ نرمال", "high": "🟠 بالا", "low": "🔴 پایین"})
    st.dataframe(show[["ساعت", "تاریخ", "قند خون", "زمان", "وضعیت"]], use_container_width=True)

    if st.button("🗑 پاک کردن همه داده‌ها"):
        st.session_state.records = []
        st.rerun()
else:
    st.info("هنوز داده‌ای ثبت نشده. اولین اندازه‌گیری قند خون خود را اضافه کنید.")

st.divider()
st.warning("⚠️ توجه: «دکتر همراه» فقط یک ابزار کمکی است و جایگزین نظر پزشک نیست.")
    
