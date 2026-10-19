import os
import streamlit as st

# استيراد محركات الحساب الإنشائي
from beams_engine import BeamEngine
from columns_engine import ColumnEngine
from footings_engine import FootingEngine
from slabs_engine import SlabEngine

# إعداد صفحة الويب
st.set_page_config(
    page_title="Structural Suite - Pro", page_icon="🏗️", layout="centered"
)

# --- نظام الحماية بكلمة المرور ---
if "authenticated" not in st.session_state:
  st.session_state.authenticated = False

if not st.session_state.authenticated:
  st.markdown(
      "<h2 style='text-align: center; color: #38BDF8;'>🔒 بوابة الدخول للنظام"
      " الإنشائي</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #94A3B8;'>يرجى إدخال كلمة المرور"
      " المخصصة للمهندس محمد ذنون</p>",
      unsafe_allow_html=True,
  )

  password_input = st.text_input("كلمة المرور (Password):", type="password")

  if st.button("دخول للنظام", use_container_width=True):
    if password_input == "MuhamedRX":
      st.session_state.authenticated = True
      st.rerun()
    else:
      st.error("❌ كلمة المرور غير صحيحة! يرجى المحاولة مرة أخرى.")
  st.stop()

# --- الواجهة الرئيسية بعد تسجيل الدخول بنجاح ---
st.markdown(
    "<h1 style='text-align: center; color: #38BDF8;'>🏗️ نظام التصميم الإنشائي"
    " الذكي</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #94A3B8;'>مرحباً بك يا مهندس محمد -"
    " تحليل المخططات وفق كود ACI 318-19</p>",
    unsafe_allow_html=True,
)
st.divider()

# رفع صورة المخطط المعماري
uploaded_file = st.file_uploader(
    "📁 قم بتحديد ورفع صورة المخطط المعماري أو الكروكي (PNG / JPG)",
    type=["png", "jpg", "jpeg"],
)

if uploaded_file is not None:
  st.success(
      f"تم رفع الملف بنجاح: **{uploaded_file.name}** جاهز للتحليل الآلي!"
  )
  st.image(uploaded_file, caption="صورة المخطط المرفق", use_column_width=True)

st.divider()

# إدخال المعطيات أو الاعتماد على التحليل التلقائي
col1, col2 = st.columns(2)
with col1:
  sx = st.number_input(
      "المسافة بين الأعمدة S_x (متر):", min_value=1.0, max_value=20.0, value=5.0
  )
  num_floors = st.number_input(
      "عدد طوابق المبنى:", min_value=1, max_value=50, value=3
  )
with col2:
  sy = st.number_input(
      "المسافة بالاتجاه الآخر S_y (متر):",
      min_value=1.0,
      max_value=20.0,
      value=6.0,
  )
  qa = st.number_input(
      "قوة تحمل التربة QA (kN/m²):", min_value=50.0, max_value=500.0, value=150.0
  )

q_slab = 12.0  # الحمل التقديري للسقف

# زر تشغيل الحسابات
if st.button(
    "⚡ إجراء التصميم الإنشائي الشامل واستخراج التقرير",
    use_container_width=True,
):
  try:
    # الحسابات الإنشائية
    max_span = max(sx, sy)
    slab_res = SlabEngine.design_one_way_slab(span_m=max_span)

    w_beam = q_slab * (sy / 2.0)
    estimated_mu = (w_beam * (sx**2)) / 8.0
    beam_res = BeamEngine.design_flexure(
        mu_knm=estimated_mu, b_mm=250, h_mm=600
    )

    trib_area = sx * sy
    total_pu = q_slab * trib_area * num_floors
    col_res = ColumnEngine.design_short_column(pu_kn=total_pu)

    footing_res = FootingEngine.design_isolated_footing(
        service_load_kn=total_pu / 1.5, allowable_q_kpa=qa
    )

    # عرض النتائج بشكل احترافي
    st.markdown("### 📊 تقرير النتائج الإنشائية المعتمدة")

    r1, r2 = st.columns(2)
    with r1:
      st.metric(
          label="السمك الأدنى للسقف (h_min)",
          value=f"{slab_res['h_min_mm']:.1f} mm",
      )
      st.metric(
          label="مساحة تسليح الجسر (As)",
          value=f"{beam_res['as_required_mm2']:.1f} mm²",
      )
    with r2:
      st.metric(
          label="مساحة مقطع العمود (Ag)",
          value=f"{col_res['Ag_required_mm2']:.0f} mm²",
      )
      st.metric(
          label="مساحة قاعدة الأساس",
          value=f"{footing_res['area_required_m2']:.2f} m²",
      )

    # نص التقرير الكامل
    full_report = (
        f"تقرير التحليل والإنشاء للمبنى (عدد الطوابق: {num_floors})\n"
        f"--------------------------------------------------\n"
        f"• أبعاد الشبكة: {sx}m x {sy}m | الحمل الكلي للعمود: {total_pu:.1f} kN\n"
        f"• سمك البلطة: {slab_res['h_min_mm']:.1f} mm\n"
        f"• تسليح الجسر (Mu={estimated_mu:.1f} kN.m): {beam_res['as_required_mm2']:.1f} mm²\n"
        f"• مساحة العمود: {col_res['Ag_required_mm2']:.0f} mm²\n"
        f"• مساحة الأساس: {footing_res['area_required_m2']:.2f} m²\n"
    )

    st.text_area("نسخ التقرير النهائي:", full_report, height=150)

  except Exception as e:
    st.error(f"حدث خطأ أثناء تنفيذ الحسابات: {e}")