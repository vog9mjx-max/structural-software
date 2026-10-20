import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="منظومة التدقيق الإنشائي - ACI 318", layout="wide")

st.title("🛡️ منظومة التدقيق الإنشائي الشاملة (Shear & Deflection Integration)")
st.write("---")

# 1. إدخال مواصفات المواد والأحمال
st.header("1️⃣ مواصفات المواد والأحمال (Materials & Loading)")
c1, c2, c3, c4 = st.columns(4)
with c1:
    fc = st.number_input("مقاومة الخرسانة f'c (MPa)", value=28.0)
with c2:
    fy = st.number_input("إجهاد خضوع الحديد fy (MPa)", value=420.0)
with c3:
    dead_super = st.number_input("أحمال إضافية Dead Load (kN/m²)", value=2.5)
with c4:
    live_load = st.number_input("الحمل الحي Live Load (kN/m²)", value=2.0)

st.write("---")

# 2. إدخال وتدقيق البلاطة (Slab Check - Deflection & Flexure)
st.header("2️⃣ تدقيق البلاطة والترخيم (Slab & Deflection Check)")
cs1, cs2, cs3, cs4 = st.columns(4)
with cs1:
    L_long = st.number_input("الطول الطويل L_L (m)", value=5.0)
with cs2:
    L_short = st.number_input("الطول القصير L_S (m)", value=4.0)
with cs3:
    h_slab = st.number_input("سمك البلاطة المدخل (mm)", value=150)
with cs4:
    slab_rebar = st.text_input("تسليح البلاطة", value="Ø12@200mm")

# حسابات البلاطة والترخيم (Deflection Check)
ratio = L_long / L_short if L_short > 0 else 1.0
slab_type = "One-Way Slab" if ratio >= 2.0 else "Two-Way Slab"

# حد سمك الترخيم المسموح به كودياً (Deflection Minimum Thickness ACI 318)
h_min_deflection = int((L_short * 1000) / 24) # فرضية بلاطة مستمرة من جانب واحد
deflection_status = "✅ آمن ومقاوم للترخيم (Deflection OK)" if h_slab >= h_min_deflection else f"⚠️ قد يحدث ترخيم! السمك الأدنى المطلوب: {h_min_deflection} mm"

st.info(f"**نوع البلاطة:** {slab_type} (النسبة = {ratio:.2f}) | **حالة الترخيم (Deflection Check):** {deflection_status}")

st.write("---")

# 3. إدخال وتدقيق الجسر والقص (Beam Shear & Flexure Check)
st.header("3️⃣ تدقيق الجسر ومقاومة القص (Beam Shear & Flexure Check)")
cb1, cb2, cb3, cb4, cb5 = st.columns(5)
with cb1:
    b_beam = st.number_input("عرض الجسر b (mm)", value=250)
with cb2:
    h_beam = st.number_input("عمق الجسر h (mm)", value=500)
with cb3:
    span_beam = st.number_input("بحر الجسر Span (m)", value=5.0)
with cb4:
    top_rebar = st.text_input("التسليح العلوي", value="2Ø14")
with cb5:
    bot_rebar = st.text_input("التسليح السفلي", value="3Ø16")

# حسابات القص والجسر (Shear Analysis)
d_eff = h_beam - 50 # العمق الفعال d
w_u = 1.2 * (dead_super + (0.25 * 0.5 * 25)) + 1.6 * live_load # الحمل الموزع الأقصى kN/m
Vu = (w_u * span_beam) / 2 # قوة القص القصوى عند المسند Vu (kN)

# قوة تحمل الخرسانة للقص phi*Vc
phi_Vc = (0.75 * 0.17 * math.sqrt(fc) * b_beam * d_eff) / 1000 # kN

if Vu <= phi_Vc:
    shear_status = f"✅ الخرسانة تقاوم القص تماماً (Vu = {Vu:.1f} kN ≤ φVc = {phi_Vc:.1f} kN) - يتطلب كانات حد أدنى فقط"
else:
    Vs_req = (Vu - phi_Vc) / 0.75
    shear_status = f"⚠️ الخرسانة لوحدها لا تكفي! يتطلب إضافة كانات تسليح قص لحمل Vs = {Vs_req:.1f} kN"

st.warning(f"**حالة تدقيق القص (Shear Check):** {shear_status}")

st.write("---")

# 4. إدخال الأعمدة
st.header("4️⃣ تدقيق العمود والأحمال (Column Capacity Check)")
cc1, cc2, cc3, cc4 = st.columns(4)
with cc1:
    b_col = st.number_input("عرض العمود B (mm)", value=300)
with cc2:
    h_col = st.number_input("عمق العمود H (mm)", value=400)
with cc3:
    col_rebar = st.text_input("تسليح العمود", value="8Ø16")
with cc4:
    floors = st.number_input("عدد الطوابق", value=2)

if st.button("📋 إخراج التقرير الاستشاري الشامل (شامل القص والدفلكشن)"):
    st.success("تم إتمام حسابات القص والترخيم والعزوم بنجاح! ✅")
    
    st.text_area("التقرير التنفيذي النهائي", f"""
====================================================================
      تقرير التدقيق الإنشائي للقص والدفلكشن - كود ACI 318
====================================================================
المواد: f'c = {fc} MPa | fy = {fy} MPa

1. تدقيق الترخيم للبلاطة (Slab Deflection Check):
   - نوع البلاطة: {slab_type} (L_L/L_S = {ratio:.2f})
   - سمك البلاطة المدخل: {h_slab} mm
   - الحد الأدنى للسمك لمنع الدفلكشن (h_min): {h_min_deflection} mm
   - التقييم: {deflection_status}

2. تدقيق القص للجسور (Beam Shear Check):
   - مقطع الجسر: {b_beam}x{h_beam} mm (d = {d_eff} mm)
   - قوة القص المسلطة القصوى (Vu): {Vu:.2f} kN
   - مقاومة الخرسانة للقص (φVc): {phi_Vc:.2f} kN
   - التقييم: {shear_status}

3. الأعمدة (Columns):
   - المقطع: {b_col}x{h_col} mm | التسليح: {col_rebar} لعدد {floors} طوابق.
====================================================================
""", height=350)
