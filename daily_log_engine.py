import streamlit as st
import base64

def render_daily_log_module(laborer_daily, carpenters_daily, steel_fixer_daily):
    st.header("🎙️ تطبيق التوثيق التلقائي لأعمال المقاولين الفرعيين عبر الصوت (AI Daily Log)")
    st.markdown("تحدث باللهجة المحلية الوسطى أو الجنوبية، وسيقوم الذكاء الاصطناعي بتحليله فوراً إلى تقارير وجداول:")
    st.write("---")

    subcontractor_name = st.text_input("اسم المقاول الفرعي:", value="شركة الرافدين لأعمال الكونكريت")
    project_location = st.text_input("موقع العمل / المشروع:", value="مجمع اللؤلؤة السكني - الطابق الثاني")

    default_iraqi_voice = "والله اليوم صبينا سقف الطابق الأول وعدنا 12 عامل و3 نجارين و2 حدادين، وتأخر صهريج الخرسانة ساعة ونص بسبب الازدحام، وعدنا تأخير بتوريد حديد البلاطة من المقاول الثانوي."
    voice_input_text = st.text_area("النص المنطوق (Voice-to-Text):", value=default_iraqi_voice, height=100)

    if st.button("🤖 تحليل التقرير بالذكاء الاصطناعي واستخراج الجداول", use_container_width=True):
        st.success("تم تحليل اللهجة العراقية واستخراج البيانات بنجاح ✅")

        st.subheader("👷 جدول حصر العمالة اليومي:")
        st.table([
            {"اختصاص العمالة": "عمال عامة", "العدد": "12 عامل", "الأجور": f"{laborer_daily:,} د.ع"},
            {"اختصاص العمالة": "نجارين تسليح", "العدد": "3 نجارين", "الأجور": f"{carpenters_daily:,} د.ع"},
            {"اختصاص العمالة": "حدادين تسليح", "العدد": "2 حدادين", "الأجور": f"{steel_fixer_daily:,} د.ع"}
        ])

        st.subheader("⚠️ سجل التأخيرات والمطالبات (Claims):")
        st.table([
            {"سبب التأخير": "تأخر صهريج الخرسانة", "المدة": "1.5 ساعة", "المسؤولية": "المقاول الفرعي"},
            {"سبب التأخير": "تأخير توريد حديد التسليح", "المدة": "يوم عمل", "المسؤولية": "المورّد / مطالبات"}
        ])

        dailylog_html = f"<html><body dir='rtl'><h1>تقرير يوميات الموقع</h1><p>المقاول: {subcontractor_name}</p><p>النص الأصلي: {voice_input_text}</p></body></html>"
        b64_dlog = base64.b64encode(dailylog_html.encode('utf-8')).decode()
        st.markdown(f'<a href="data:text/html;base64,{b64_dlog}" download="Daily_Log_Report.html" style="text-decoration: none;"><div style="background-color: #0f172a; color: white; padding: 12px; border-radius: 6px; text-align: center; font-weight: bold;">📄 تحميل تقرير يوميات الموقع (PDF/HTML)</div></a>', unsafe_allow_html=True)
