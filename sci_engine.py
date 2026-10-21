import streamlit as st
import base64

def render_sci_module(prices):
    st.header("🔍 النظام الذكي المتكامل لفحص، تشخيص، ومعالجة التشققات الإنشائية (SCI)")
    st.markdown("🌐 **وضع التشغيل الميداني (Offline First):** ارفق صورة الشق وأدخل البيانات للتشخيص الفوري:")
    st.write("---")

    # أداة إرفاق والتقاط صور الشق ميدانياً
    st.markdown("📷 **إرفاق أو التقاط صورة الشق ميدانياً (Crack Image Upload):**")
    crack_image = st.file_uploader("اختر صورة الشق من الكاميرا أو الألبوم:", type=["jpg", "jpeg", "png"])
    if crack_image is not None:
        st.image(crack_image, caption="معاينة صورة الشق الميدانية المرصودة", use_container_width=True)

    col_sci1, col_sci2 = st.columns(2)
    with col_sci1:
        element_id = st.text_input("رقم أو رمز العنصر الإنشائي (Element ID):", value="Beam-B1 (الطابق الأرضي)")
        crack_width_mm = st.number_input("عرض الشق المقاس (مم):", min_value=0.05, max_value=15.0, value=0.6, step=0.05)
        crack_length_m = st.number_input("طول الشق الإجمالي (متر):", min_value=0.1, max_value=50.0, value=2.5, step=0.1)
    with col_sci2:
        crack_angle = st.selectbox("زاوية واتجاه الشق (Pattern & Angle):", [
            "شق مائل بـ 45 درجة (يدل على إجهاد قص / Shear Crack)",
            "شق أفقي (يدل على هبوط أساسات أو عزوم سالبة / Settlement or Flexure)",
            "شق عمودي شاقولي (يدل على انكماش أو زيادة أحمال ضغط / Shrinkage or Overloading)",
            "تشققات شعرية عشوائية (Crazing / Shrinkage Cracks)"
        ])
        crack_activity = st.radio("نشاط الشق (Crack Activity):", ["شق مستقر (Dormant)", "شق نشط ويتسع بمرور الزمن (Active - يحتاج مراقبة Tell-Tale)"], horizontal=True)

    st.write("---")
    st.subheader("🛠️ التشخيص الهندسي وحلول المعالجة (حسب كود ACI 318 / ACI 224R):")

    if "45" in crack_angle or crack_width_mm > 1.0:
        diagnosis_result = "⚠️ شق إنشائي حرج (Structural Critical Crack): يشير إلى تجاوز إحداثيات القص أو العزوم القصوى، ويجب التدخل الفوري."
        repair_method = "التدعيم بألياف الكربون (FRP Systems) أو قمصان خرسانية/إيبوكسية بعد تخفيف الأحمال."
        material_type = "مادة لاصقة إيبوكسيدية عالية المقاومة للتشققات الهيكلية."
        depth_est_cm = 15.0
        unit_cost_factor = prices["epoxy_liter"] * 1.5
    elif crack_width_mm < 0.3:
        diagnosis_result = "🟢 شق غير إنشائي (Non-Structural / Hairline Crack): غالباً ناتج عن انكماش سطحي أو تغيرات حرارية."
        repair_method = "معالجة سطحية بمالئ أو طلاء إيبوكسي مرن (Surface Sealing / Epoxy Injection)."
        material_type = "إيبوكسي منخفض اللزوجة للحقن السطحي."
        depth_est_cm = 3.0
        unit_cost_factor = prices["epoxy_liter"]
    else:
        diagnosis_result = "🟡 شق إنشائي متوسط (Moderate Structural Crack): يتطلب حقن إيبوكسي ومتابعة."
        repair_method = "حقن إيبوكسي عميق تحت ضغط (Pressure Epoxy Injection) لملء الفراغات الداخلية."
        material_type = "إيبوكسي حقن متوسط اللزوجة (Low Viscosity Epoxy Resin)."
        depth_est_cm = 8.0
        unit_cost_factor = prices["epoxy_liter"]

    st.markdown(f"**التقييم التشخيصي:** {diagnosis_result}")
    st.markdown(f"**طريقة الإصلاح المعتمدة:** {repair_method}")
    st.markdown(f"**المواصفات الفنية للمادة:** {material_type}")

    if "نشط" in crack_activity:
        st.warning("⚠️ **تنبيه أمان ميداني:** نظراً لأن الشق (نشط)، يُلزم وضع مؤشرات مراقبة زجاجية أو ميكانيكية (Crack Tell-Tale) لمدة لا تقل عن 30 يوماً لتتبع معدل الاتساع قبل الحقن النهائي.")

    material_volume_liters = round((crack_length_m * 100) * (depth_est_cm) * (crack_width_mm / 10.0) * 0.001 * 1.2, 2)
    if material_volume_liters < 0.5: material_volume_liters = 0.5
    estimated_total_cost = round(material_volume_liters * (unit_cost_factor / 10.0) + 75000, -3)

    st.write("---")
    st.subheader("💰 جدول حصر الكميات والتكلفة التقديرية (BoQ):")
    st.table([{"عنصر الفحص": element_id, "عرض الشق": f"{crack_width_mm} مم", "الطول": f"{crack_length_m} م", "كمية مادة المعالجة المطلوبة": f"{material_volume_liters} لتر / كغ", "الكلفة التقديرية للمواد والعمالة": f"{estimated_total_cost:,.0f} دينار عراقي"}])

    st.write("---")
    sci_html = f"""
    <html dir="rtl"><head><meta charset="utf-8"><title>تقرير فحص الشق - SCI</title>
    <style>body {{ font-family: Tahoma, sans-serif; padding: 20px; direction: rtl; text-align: right; }} h1, h2 {{ text-align: center; color: #0f172a; }} table {{ width: 100%; border-collapse: collapse; }} th, td {{ border: 1px solid #cbd5e1; padding: 8px; text-align: center; }} th {{ background-color: #0f172a; color: white; }}</style>
    </head><body><h1>المنظومة الهندسية الاستشارية - وحدة SCI</h1><h3>إشراف وتطوير: المهندس محمد ذنون عبد شريف | جامعة كربلاء</h3><hr>
    <p><b>رمز العنصر:</b> {element_id} | <b>عرض الشق:</b> {crack_width_mm} مم | <b>الطول:</b> {crack_length_m} م</p>
    <p><b>التشخيص:</b> {diagnosis_result}</p><p><b>طريقة الإصلاح:</b> {repair_method}</p>
    </body></html>"""
    b64_sci = base64.b64encode(sci_html.encode('utf-8')).decode()
    st.markdown(f'<a href="data:text/html;base64,{b64_sci}" download="SCI_Report.html" style="text-decoration: none;"><div style="background-color: #0f172a; color: white; padding: 12px; border-radius: 6px; text-align: center; font-weight: bold;">📄 تحميل تقرير فحص الشق الرسمي (PDF/HTML)</div></a>', unsafe_allow_html=True)
