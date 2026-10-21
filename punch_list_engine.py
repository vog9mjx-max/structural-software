import streamlit as st
import base64

def render_punch_list_module():
    st.header("📋 Smart Punch List - العراق ('حاسبها صح') لتسليم المشاريع")
    st.markdown("المنظومة الذكية لتسجيل العيوب وتشخيصها باللهجة العراقية وإرسالها للمقاولين:")
    st.write("---")

    col_pl1, col_pl2 = st.columns(2)
    with col_pl1:
        location_zone = st.text_input("موقع العيب (الطابق / الغرفة):", value="الشقة رقم 302 - الحمام الرئيسي")
        contractor_name = st.selectbox("المقاول الفرعي المسؤول:", ["شركة البناء السريع", "أبو كرار للتأسيسات الصحية", "مجموعة الكوثر للإنهاءات"])
        defect_category = st.selectbox("تصنيف العيب:", ["تأسيسات صحية وصرف", "إنهاءات وبلاط", "أبواب وشبابيك", "كهربائيات"])
    with col_pl2:
        defect_description = st.text_input("وصف العيب الظاهري:", value="رطوبة عالية ونش في جدار الحمام وصرف غير محكم")
        priority_level = st.selectbox("الأولوية:", ["عالية جداً (تعديل خلال 24 ساعة)", "متوسطة (خلال 3 أيام)", "بسيطة"])
        workflow_status = st.selectbox("حالة العيب:", ["🔴 جديد (New)", "🟡 قيد الإصلاح (In Progress)", "🟢 تم التسليم ومغلق (Approved)"])

    if "صحية" in defect_category or "نش" in defect_description:
        ai_diagnosis = "هذا رطوبة صاعدة بالجدار بسبب عزل مو زين أو نش للماي بالجدران الجانبية."
        ai_cause = "الميلان مال الشربتة مو صحيح أو السندريلا ما معزولة زين بمانع الرطوبة."
        ai_solution = "يلزم كشط البياض والتطبيق من جديد بعد حقن مادة العزل المائي وتثبيت شريط العزل."
    else:
        ai_diagnosis = "تطبل أو تكسر في السيراميك نتيجة عدم انتظام الملاط تحته."
        ai_cause = "عدم استخدام مادة لاصقة كافية أو عدم دك السيراميك بصورة صحيحة."
        ai_solution = "رفع البلاطة المتضررة، تنظيف المكان، وإعادة التطبيق بمادة لاصقة معتمدة."

    st.write("---")
    st.info(f"💬 **التشخيص العراقي:** {ai_diagnosis}\n\n🔍 **السبب:** {ai_cause}\n\n🛠️ **الحل الهندسي:** {ai_solution}")

    whatsapp_msg = f"عيني {contractor_name}، عندك ملاحظة بموقع ({location_zone}): {defect_description}. الحل: {ai_solution}. يرجى الإنجاز بأسرع وقت."
    st.markdown(f"📱 **نص الإشعار الجاهز للإرسال (WhatsApp):**\n> *{whatsapp_msg}*")

    punch_html = f"<html><body dir='rtl'><h1>محضر تسليم الملاحظات - Punch List</h1><p>الموقع: {location_zone} | المقاول: {contractor_name}</p><p>العيب: {defect_description}</p></body></html>"
    b64_pl = base64.b64encode(punch_html.encode('utf-8')).decode()
    st.markdown(f'<a href="data:text/html;base64,{b64_pl}" download="Punch_List_Report.html" style="text-decoration: none;"><div style="background-color: #0f172a; color: white; padding: 12px; border-radius: 6px; text-align: center; font-weight: bold;">📄 تحميل تقرير التسليم الرسمي (PDF/HTML)</div></a>', unsafe_allow_html=True)
