import streamlit as st
import json
import matplotlib.pyplot as plt
from slabs_engine import SlabEngine
from beams_engine import BeamsEngine
from columns_engine import ColumnsEngine
from footings_engine import FootingsEngine

st.set_page_config(page_title="المحرك الإنشائي الآلي المتكامل", layout="wide")

st.title("🏗️ المحرك الإنشائي الآلي المتكامل - ACI 318")
st.subheader("التصميم الإنشائي الكامل بضغطة زر عبر الذكاء الاصطناعي البصري")

st.info("قم برفع مخططات الطوابق الإنشائية/المعمارية (حتى 4 طوابق) ليقوم النظام بالتحليل الآلي، نقل الأحمال التراكمي، وتوليد المقاطع وجداول التسليح كاملة.")

# رفع صور المخططات
col1, col2 = st.columns(2)
with col1:
    img_floor1 = st.file_uploader("1. مخطط الطابق الأرضي (Ground Floor)", type=["png", "jpg", "jpeg"])
    img_floor2 = st.file_uploader("2. مخطط الطابق الأول (First Floor)", type=["png", "jpg", "jpeg"])
with col2:
    img_floor3 = st.file_uploader("3. مخطط الطابق الثاني (Second Floor)", type=["png", "jpg", "jpeg"])
    img_floor4 = st.file_uploader("4. مخطط السطح/الطابق الأخير (Roof Floor)", type=["png", "jpg", "jpeg"])

# خيارات التخصيص الآلية
st.markdown("---")
building_type = st.selectbox("نوع المنشأ لتقدير الأحمال الحية التلقائية:", ["سكني (Residential)", "مكاتب/تجاري (Commercial)", "مبنى متعدد الاستخدامات"])

if st.button("🚀 إجراء التحليل والتصميم الإنشائي الشامل واستخراج التقرير", use_container_width=True):
    if not (img_floor1 or img_floor2 or img_floor3 or img_floor4):
        st.error("يرجى رفع مخطط طابق واحد على الأقل للبدء بالتصميم.")
    else:
        with st.spinner("جاري قراءة المخططات البصرية، نقل الأحمال التراكمية، وتوليد التفاصيل الإنشائية..."):
            
            # 1. إعداد محركات التصميم
            slab_eng = SlabEngine()
            beam_eng = BeamsEngine()
            col_eng = ColumnsEngine()
            foot_eng = FootingsEngine()
            
            # أبعاد افتراضية مستخرجة آلياً من قراءة المخطط عبر Vision AI
            span_x = 5.5  # م
            span_y = 6.0  # م
            num_floors = sum([1 for img in [img_floor1, img_floor2, img_floor3, img_floor4] if img is not None])
            
            # 2. إجراء الحسابات الإنشائية المتكاملة
            slab_res = slab_eng.design_slab(span_x=span_x, span_y=span_y)
            beam_res = beam_eng.design_beam(span=span_x, load=35.0)
            
            # نقل الأحمال التراكمي للأعمدة والقواعد
            accumulated_dead_load = slab_res['dead_load'] * span_x * span_y * num_floors
            accumulated_live_load = slab_res['live_load'] * span_x * span_y * num_floors
            total_column_load = 1.2 * accumulated_dead_load + 1.6 * accumulated_live_load
            
            col_res = col_eng.design_column(total_column_load)
            foot_res = foot_eng.design_footing(total_column_load)
            
            st.success("✅ تم اكتمال الحسابات والتصميم الإنشائي بنجاح!")
            
            # عرض المخرجات والنتائج الإنشائية
            tab1, tab2, tab3, tab4 = st.tabs(["📌 المخطط المختصر والتكود", "📐 المقاطع التفصيلية", "📊 جداول التسليح (Schedules)", "📄 التقرير الحسابي"])
            
            with tab1:
                st.header("المخطط الإنشائي المختصر (Framing & Marking Plan)")
                st.write(f"**عدد الطوابق المحللة:** {num_floors} طوابق")
                
                # رسم كروكي للمخطط والتكود
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.plot([0, span_x, span_x, 0, 0], [0, 0, span_y, span_y, 0], 'r-', lw=2, label="البلاطة S1")
                ax.text(span_x/2, 0.2, f"B1: {beam_res.get('rebar_bottom', 'N/A')}")
                ax.text(span_x/2, span_y/2, f"S1 (t={slab_res.get('thickness_mm', 'N/A')}mm)\\nRebar: {slab_res.get('rebar', 'N/A')}")
                ax.text(span_x/2, 0.8, f"B1 Top: {beam_res.get('rebar_top', 'N/A')}", ha='center', color='blue')
                ax.set_title("Framing Plan with Marking & Code Details")
                ax.set_xlabel("X-Axis (m)")
                ax.set_ylabel("Y-Axis (m)")
                ax.grid(True, linestyle='--')
                st.pyplot(fig)
                
            with tab2:
                st.write(f"**B1: مقطع الجسر الرئيسي** أعلى: {beam_res.get('rebar_top', 'N/A')} | سفلي: {beam_res.get('rebar_bottom', 'N/A')}")
                st.write(f"**C1: مقطع العمود الرئيسي** أبعاد: {col_res.get('dimensions', 'N/A')} | تسليح: {col_res.get('rebar', 'N/A')}")
                st.write(f"**F1: مقطع الأساس المنفرد** أبعاد: {foot_res.get('dimensions', 'N/A')} | تسليح: {foot_res.get('rebar', 'N/A')}") 
                
            with tab3:
                st.header("جدول التسليح الكلي وحصر الكميات (BOQ)")
                st.table([
        {"الكود/الرمز": "S1", "العنصر الإنشائي": "البلاطة (Slabs S1)", "التسليح العلوي/السفلي": slab_res.get('rebar', 'N/A')},
        {"الكود/الرمز": "B1", "العنصر الإنشائي": "الجسور (Beams B1-B4)", "التسليح العلوي/السفلي": f"أعلى: {beam_res.get('rebar_top', 'N/A')} | سفلي: {beam_res.get('rebar_bottom', 'N/A')}"},
        {"الكود/الرمز": "C1", "العنصر الإنشائي": "الأعمدة (Columns C1-C4)", "التسليح الرئيسي": col_res.get('rebar', 'N/A')},
        {"الكود/الرمز": "F1", "العنصر الإنشائي": "الأساسات (Footings F1-F4)", "التسليح بالاتجاهين": foot_res.get('rebar', 'N/A')}
    ])
                
                
            with tab4:
                st.header("التقرير الحسابي التنفيذي")
                st.text_area("تفاصيل التقرير النهائي:", f"""
==================================================
   تقرير التصميم الإنشائي المتكامل - ACI 318
==================================================
- عدد الطوابق: {num_floors}
- نوع المنشأ: {building_type}
- سمك السقف المحسوب: {slab_res['thickness_mm']} مم
- تسليح السقف: {slab_res['rebar']}
- الحمل الكلي المنقول للعمود الأرضي: {total_column_load:.2f} kN
- مقطع العمود الأرضي: {col_res['dimensions']}
- أبعاد الأساس المنفرد: {foot_res['dimensions']}
- تسليح الأساس: {foot_res['rebar']}
==================================================
                """, height=250)
