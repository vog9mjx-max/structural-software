import streamlit as st
import base64

def render_curing_module():
    st.header("🌡️ نظام إدارة صب ومعالجة الخرسانة والظروف الجوية (ACI 305R / 306R)")
    st.markdown("🌐 **وضع التشغيل الميداني (Offline First):** محرك محلي لحساب معدل التبخر وخطورة الصب دون الحاجة لإنترنت:")
    st.write("---")

    col_cur1, col_cur2 = st.columns(2)
    with col_cur1:
        air_temp_c = st.number_input("درجة حرارة الجو (°C):", min_value=0.0, max_value=55.0, value=38.0, step=0.5)
        concrete_temp_c = st.number_input("درجة حرارة الخرسانة الطازجة (°C):", min_value=10.0, max_value=45.0, value=30.0, step=0.5)
        relative_humidity = st.slider("نسبة الرطوبة النسبية (%):", 10, 100, 30)
    with col_cur2:
        wind_speed_kmh = st.number_input("سرعة الرياح (كم/ساعة):", min_value=0.0, max_value=60.0, value=18.0, step=1.0)
        cement_type_curing = st.selectbox("نوع الإسمنت المستخدم:", ["إسمنت بورتلاندي عادي (OPC - Type I)", "إسمنت سريع الشك أو مقاوم (Type V)"])
        element_type_curing = st.selectbox("العنصر الخرساني المراد صبه:", ["قواعد أساسات / لبشة (Mass Concrete)", "أعمدة وجسور (Columns & Beams)", "سقوف وبلاطات (Slabs)"])

    evap_rate_metric = round((((concrete_temp_c**1.8) - (relative_humidity * 0.01 * air_temp_c**1.8)) * (wind_speed_kmh + 4)) * 0.00008, 2)
    if evap_rate_metric < 0.1: evap_rate_metric = 0.1

    st.write("---")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("معدل تبخر الماء من سطح الخرسانة", f"{evap_rate_metric} kg/m²/hr")
    with col_res2:
        if evap_rate_metric > 1.0:
            st.error("🚨 خطر جداً! معدل التبخر يتجاوز 1.0 كغ/م²/ساعة. **يمنع الصب حالياً** أو يلزم استخدام مصدات رياح وموال معالجة فورية.")
        elif evap_rate_metric > 0.5:
            st.warning("⚠️ تحذير: معدل التبخر مرتفع. يجب اتخاذ إجراءات احترازية ورش مائي.")
        else:
            st.info("🟢 حالة الطقس ملائمة ومستقرة للصب.")

    base_days_form = 14 if "لبشة" in element_type_curing else (7 if "جسور" in element_type_curing else 2)
    if "سريع" in cement_type_curing: base_days_form = max(1, int(base_days_form * 0.7))
    if air_temp_c > 35: base_days_form = max(1, int(base_days_form * 0.8))

    curing_days_req = 7 if "عادي" in cement_type_curing else 5

    st.write("---")
    st.subheader("⏱️ جدول مواعيد فك القوالب والمعالجة المثلى:")
    st.table([{"عنصر المنشأ": element_type_curing, "فك القوالب": f"بعد {base_days_form} إلى {base_days_form+2} أيام", "فترة المعالجة الإلزامية": f"{curing_days_req} أيام متواصلة"}])

    curing_html = f"<html><body dir='rtl'><h1>تقرير صب ومعالجة الخرسانة</h1><p>حرارة الجو: {air_temp_c} °C | معدل التبخر: {evap_rate_metric} kg/m²/hr</p></body></html>"
    b64_cur = base64.b64encode(curing_html.encode('utf-8')).decode()
    st.markdown(f'<a href="data:text/html;base64,{b64_cur}" download="Curing_Report.html" style="text-decoration: none;"><div style="background-color: #0f172a; color: white; padding: 12px; border-radius: 6px; text-align: center; font-weight: bold;">📄 تحميل تقرير الصب الميداني (PDF/HTML)</div></a>', unsafe_allow_html=True)
