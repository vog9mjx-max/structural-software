import streamlit as st

# استدعاء المحركات الميدانية المحدثة
try:
    from sci_engine import render_sci_module
    from curing_engine import render_curing_module
    from daily_log_engine import render_daily_log_module
    from punch_list_engine import render_punch_list_module
except ImportError:
    pass

st.set_page_config(page_title="المنظومة الهندسية الاستشارية - م. محمد ذنون", layout="wide")

# ==========================================
# تخصيص واجهة CSS الفاخرة
# ==========================================
st.markdown("""
    <style>
    .main { background-color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; direction: rtl; }
    h1, h2, h3, p, label, div { font-family: 'Segoe UI', Tahoma, sans-serif; text-align: right; }
    [data-testid="stSidebar"] { background-color: #1e293b; color: #ffffff; }
    [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stButton button, [data-testid="stSidebar"] p { color: #ffffff; text-align: right; }
    .stButton button { background-color: #0f172a; color: white; border-radius: 6px; font-weight: bold; border: 1px solid #334155; }
    .stButton button:hover { background-color: #334155; color: #ffffff; border-color: #cbd5e1; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# نظام حماية التطبيق بكلمة السر
# ==========================================
PASSWORD_KEY = "1234" 

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #0f172a; font-size: 24px;'>🔐 بوابة الدخول للمنظومة الهندسية الاستشارية</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 16px; font-weight: bold; color: #475569;'>إشراف وتطوير: المهندس محمد ذنون عبد شريف</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px;'>الرجاء إدخال رمز المرور السري للدخول إلى النظام:</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password_input = st.text_input("كلمة السر", type="password", key="pwd_input")
        if st.button("تسجيل الدخول الاحترافي 🔓", use_container_width=True):
            if password_input == PASSWORD_KEY:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ كلمة السر غير صائبة! يرجى المحاولة مرة أخرى.")
    return False

if not check_password():
    st.stop()

# ==========================================
# العنوان الرئيسي للمنظومة
# ==========================================
st.title("🏛️ المنظومة الهندسية الاستشارية المتكاملة")
st.markdown("### 👨‍💻 إشراف وتطوير: **المهندس محمد ذنون عبد شريف** | جامعة كربلاء")
st.write("---")

if st.sidebar.button("🔒 قفل النظام وتسجيل الخروج"):
    st.session_state["password_correct"] = False
    st.rerun()

# القائمة الجانبية للأقسام الـ 9
mode = st.sidebar.selectbox(
    "اختر قسم العمل المطلوب:", 
    [
        "📋 Smart Punch List - العراق (حاسبها صح)",
        "🎙️ Subcontractor Daily Log AI (يوميات الموقع والصوت)",
        "🌡️ Concrete Curing & Thermal Monitor (إدارة الصب)",
        "🔍 Structural Crack Inspector (SCI - التشققات)",
        "📋 جدول الكميات والكلف المعياري المفصل (Modular BOQ)",
        "🏛️ حساب كميات وكلف واجهات البيوت والفلل (Façade Works)",
        "🏡 التصميم المعماري وتوزيع المساحات والخرائط", 
        "🔍 التحليل الإنشائي والتدقيق الشامل وتصميم الأساسات (ACI 318)",
        "📊 حاسبة المواد التفصيلية (الطابوق، الأسمنت، الأرضيات)"
    ]
)

# أسعار السوق العراقي
st.sidebar.write("---")
st.sidebar.subheader("📈 مراقب أسعار السوق العراقي والأجور")
live_steel_price = st.sidebar.number_input("سعر طن الحديد (د.ع)", value=980000, step=10000)
live_cement_price = st.sidebar.number_input("سعر كيس الأسمنت (د.ع)", value=8500, step=250)
carpenters_daily = st.sidebar.number_input("أجور النجار اليومية (د.ع)", value=45000, step=5000)
steel_fixer_daily = st.sidebar.number_input("أجور الحداد اليومية (د.ع)", value=45000, step=5000)
laborer_daily = st.sidebar.number_input("أجور العامل اليومية (د.ع)", value=30000, step=2500)

prices = {"epoxy_liter": 25000, "grout_kg": 3500, "cement_bag": live_cement_price}

# ==========================================
# التوجيه الحقيقي للملفات والمحركات الفرعية
# ==========================================
if "Smart Punch List" in mode:
    try:
        render_punch_list_module()
    except NameError:
        st.error("⚠️ يرجى التأكد من وجود ملف punch_list_engine.py في المستودع.")
elif "Subcontractor Daily Log" in mode:
    try:
        render_daily_log_module(laborer_daily, carpenters_daily, steel_fixer_daily)
    except NameError:
        st.error("⚠️ يرجى التأكد من وجود ملف daily_log_engine.py في المستودع.")
elif "Concrete Curing" in mode:
    try:
        render_curing_module()
    except NameError:
        st.error("⚠️ يرجى التأكد من وجود ملف curing_engine.py في المستودع.")
elif "Structural Crack Inspector" in mode:
    try:
        render_sci_module(prices)
    except NameError:
        st.error("⚠️ يرجى التأكد من وجود ملف sci_engine.py في المستودع.")
else:
    st.info("اختر القسم المطلوب من القائمة الجانبية للبدء بالعمل الهندسي.")
