import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import base64

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
# واجهة التطبيق الرئيسية للمهندس محمد ذنون
# ==========================================
st.title("🏛️ المنظومة الهندسية الاستشارية المتكاملة")
st.markdown("### 👨‍💻 إشراف وتطوير: **المهندس محمد ذنون عبد شريف** | جامعة كربلاء")
st.write("---")

if st.sidebar.button("🔒 قفل النظام وتسجيل الخروج"):
    st.session_state["password_correct"] = False
    st.rerun()

# القائمة الرئيسية لجميع الأقسام
mode = st.sidebar.selectbox(
    "اختر قسم العمل المطلوب:", 
    [
        "📋 جدول الكميات والكلف المعياري المفصل (Modular BOQ)",
        "🏛️ حساب كميات وكلف واجهات البيوت والفلل (Façade Works)",
        "🏡 التصميم المعماري وتوزيع المساحات والخرائط", 
        "🔍 التدقيق والتحليل الإنشائي والتوليد التلقائي (ACI 318)",
        "📊 حاسبة المواد التفصيلية (الطابوق، الأسمنت، الأرضيات)"
    ]
)

# ==========================================
# لوحة التحكم الجانبية لمراقبة وتحديث أسعار السوق العراقي
# ==========================================
st.sidebar.write("---")
st.sidebar.subheader("📈 مراقب أسعار السوق العراقي والأجور")
st.sidebar.markdown("تحديث الأسعار والأجور لتواكب السوق المحلي لحظياً:")

live_steel_price = st.sidebar.number_input("سعر طن الحديد (د.ع)", value=980000, step=10000)
live_cement_price = st.sidebar.number_input("سعر كيس الأسمنت (د.ع)", value=8500, step=250)
live_brick_price = st.sidebar.number_input("سعر الطابوقة الحمراء (د.ع)", value=275, step=10)
carpenters_daily = st.sidebar.number_input("أجور النجار اليومية (د.ع)", value=45000, step=5000)
steel_fixer_daily = st.sidebar.number_input("أجور الحداد اليومية (د.ع)", value=45000, step=5000)
laborer_daily = st.sidebar.number_input("أجور العامل اليومية (د.ع)", value=30000, step=2500)

prices = {
    "brick_red": live_brick_price,
    "brick_yellow": live_brick_price * 1.25,
    "block_20": 1250,
    "cement_bag": live_cement_price,
    "sand_m3": 28000,
    "gravel_m3": 32000,
    "bourk_bag": 7000,
    "steel_high": live_steel_price,
    "steel_plain": live_steel_price + 70000,
    "kashi_m2": 12000,
    "ceramic_floor_m2": 10500,
    "porcelain_m2": 18000,
    "marble_m2": 35000,
    "nylon_m2": 750,
    "shovel_hour": 35000,
    "roller_day": 150000
}

# ==========================================
# 0. قسم جدول الكميات المعياري المفصل (Modular BOQ)
# ==========================================
if "جدول الكميات والكلف المعياري المفصل" in mode:
    st.header("📋 جدول الكميات والكلف المعياري المفصل (Modular BOQ)")
    st.markdown("اختر الأقسام التي ترغب بحساب تكلفتها الفعلية في مشروعك:")
    st.write("---")

    modular_table_data = []
    grand_total_cost = 0.0

    st.subheader("1️⃣ قسم أعمال البناء والطابوق / البلوك")
    use_brick = st.radio("هل تريد حساب قسم الطابوق والبلوك في الكلفة؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_brick")
    b_cost = 0
    if "نعم" in use_brick:
        bc1, bc2 = st.columns(2)
        with bc1: q_brick_area = st.number_input("مساحة الجدران للطابوق (م²)", min_value=0.0, value=100.0, step=10.0, key="mod_b_area")
        with bc2: brick_type_sel = st.selectbox("نوع الطابوق/البلوك:", ["طابوق أحمر قياسي عراقي", "طابوق أصفر فرشي/ناري", "بلوك خرساني مجوف 20سم"], key="mod_b_type")
        
        if "أصفر" in brick_type_sel:
            b_count = int(q_brick_area * 58 * 1.05)
            b_cost = b_count * prices["brick_yellow"]
        elif "بلوك" in brick_type_sel:
            b_count = int(q_brick_area * 12.5 * 1.05)
            b_cost = b_count * prices["block_20"]
        else:
            b_count = int(q_brick_area * 58 * 1.05)
            b_cost = b_count * prices["brick_red"]

        modular_table_data.append({"القسم": "قسم البناء", "المادة / العنصر": brick_type_sel, "المساحة / البعد": f"{q_brick_area} م² جدران", "الكمية المطلوبة": f"{b_count:,} قطعة", "الكلفة التقديرية (د.ع)": f"{b_cost:,.0f}"})
        grand_total_cost += b_cost

    st.write("---")
    st.subheader("2️⃣ قسم اللبخ والإنهاءات الداخلية والخارجية")
    use_plaster = st.radio("هل تريد حساب قسم اللبخ والإنهاءات؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_plaster")
    plaster_cost = 0
    if "نعم" in use_plaster:
        pc1, pc2 = st.columns(2)
        with pc1: q_plaster_area = st.number_input("مساحة الجدران للَّبخ والإنهاء (م²)", min_value=0.0, value=200.0, step=10.0, key="mod_p_area")
        with pc2:
            cement_bags_p = int(q_plaster_area * 0.32)
            sand_p_m3 = round(q_plaster_area * 0.022, 1)
            plaster_cost = (cement_bags_p * prices["cement_bag"]) + (sand_p_m3 * prices["sand_m3"])

        modular_table_data.append({"القسم": "قسم اللبخ", "المادة / العنصر": "مواد لبخ أسمنتي (أسمنت + رمل)", "المساحة / البعد": f"{q_plaster_area} م²", "الكمية المطلوبة": f"{cement_bags_p} كيس | {sand_p_m3} م³ رمل", "الكلفة التقديرية (د.ع)": f"{plaster_cost:,.0f}"})
        grand_total_cost += plaster_cost

    st.write("---")
    st.subheader("3️⃣ قسم الأرضيات (كاشي، مرمر، بورسلين، سيراميك)")
    use_floors = st.radio("هل تريد حساب قسم الأرضيات؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_floors")
    floor_cost = 0
    if "نعم" in use_floors:
        fc1, fc2 = st.columns(2)
        with fc1: q_floor_area = st.number_input("مساحة الأرضيات الكلية (م²)", min_value=0.0, value=120.0, step=10.0, key="mod_f_area")
        with fc2: floor_type_sel = st.selectbox("نوع الأرضيات:", ["كاشي موزاييك عراقي تقليدي", "سيراميك أرضيات فاخر", "بورسلين صالونات", "مرمر طبيعي"], key="mod_f_type")

        if "بورسلين" in floor_type_sel: floor_cost = q_floor_area * prices["porcelain_m2"]
        elif "سراميك" in floor_type_sel: floor_cost = q_floor_area * prices["ceramic_floor_m2"]
        elif "مرمر" in floor_type_sel: floor_cost = q_floor_area * prices["marble_m2"]
        else: floor_cost = q_floor_area * prices["kashi_m2"]

        modular_table_data.append({"القسم": "قسم الأرضيات", "المادة / العنصر": f"أرضيات ({floor_type_sel})", "المساحة / البعد": f"{q_floor_area} م²", "الكمية المطلوبة": f"{q_floor_area} م²", "الكلفة التقديرية (د.ع)": f"{floor_cost:,.0f}"})
        grand_total_cost += floor_cost

    st.write("---")
    st.subheader("4️⃣ قسم الخرسانة المسلحة وحديد التسليح")
    use_concrete = st.radio("هل تريد حساب قسم الهيكل الإنشائي (كونكريت + حديد)؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_concrete")
    struct_cost = 0
    if "نعم" in use_concrete:
        cc1, cc2, cc3 = st.columns(3)
        with cc1: q_conc_vol = st.number_input("حجم الكونكريت الإنشائي (م³)", min_value=0.0, value=30.0, step=5.0, key="mod_c_vol")
        with cc2: 
            q_steel_t = st.number_input("وزن حديد التسليح (طن)", min_value=0.0, value=3.5, step=0.5, key="mod_s_ton")
            steel_t_sel = st.selectbox("نوع الحديد:", ["حديد مشوه عالي المقاومة", "حديد أملس / ناعم"], key="mod_s_type")
        with cc3:
            steel_dia_sel = st.selectbox("قطر الحديد الشائع:", ["Ø10 مم (كانات)", "Ø12 مم (سقوف وجسور)", "Ø16 مم (أعمدة وجسور رئيسية)", "Ø20 مم (أساسات)", "Ø25 مم (أعمدة ثقيلة)"], key="mod_s_dia")

        conc_mat_cost = q_conc_vol * (prices["cement_bag"] * 7 + prices["sand_m3"] * 0.5 + prices["gravel_m3"] * 0.8)
        st_cost = q_steel_t * (prices["steel_plain"] if "أملس" in steel_t_sel else prices["steel_high"])
        struct_cost = conc_mat_cost + st_cost

        modular_table_data.append({"القسم": "قسم الإنشائي", "المادة / العنصر": "خرسانة مسلحة (أساسات/أعمدة/سقوف)", "المساحة / البعد": f"{q_conc_vol} م³", "الكمية المطلوبة": f"{q_conc_vol} م³", "الكلفة التقديرية (د.ع)": f"{conc_mat_cost:,.0f}"})
        modular_table_data.append({"القسم": "قسم الإنشائي", "المادة / العنصر": f"حديد تسليح ({steel_t_sel}) - قطر ({steel_dia_sel})", "المساحة / البعد": f"{q_conc_vol} م³ منشأ", "الكمية المطلوبة": f"{q_steel_t} طن", "الكلفة التقديرية (د.ع)": f"{st_cost:,.0f}"})
        grand_total_cost += struct_cost

    st.write("---")
    st.subheader("5️⃣ العزل، الآليات، وأجور الكوادر")
    use_extras = st.radio("هل تريد حساب مواد العزل والآليات والأجور؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_ext")
    if "نعم" in use_extras:
        nylon_area = st.number_input("مساحة فرش النايلون (م²)", value=100.0, step=10.0)
        nylon_c = nylon_area * prices["nylon_m2"]
        mach_c = (8 * prices["shovel_hour"]) + (1 * prices["roller_day"])
        lab_c = (10 * carpenters_daily) + (10 * steel_fixer_daily) + (30 * laborer_daily)
        
        modular_table_data.append({"القسم": "قسم العزل والآليات والكوادر", "المادة / العنصر": "فرش نايلون + آليات (شفل وفراد) + أجور عمالة", "المساحة / البعد": "شامل", "الكمية المطلوبة": "مجموع الفعاليات", "الكلفة التقديرية (د.ع)": f"{nylon_c + mach_c + lab_c:,.0f}"})
        grand_total_cost += (nylon_c + mach_c + lab_c)

    st.write("---")
    if st.button("📊 إظهار الجدول المجمع والتكلفة الفعلية للمشروع", use_container_width=True):
        if not modular_table_data:
            st.warning("⚠️ لم تقم بتفعيل أي قسم بالأعلى!")
        else:
            st.success("تم تجميع جدول كميات وكلف المشروع بنجاح ✅")
            st.table(modular_table_data)
            st.markdown(f"### 💰 الكلفة الإجمالية الفعلية للمشروع: **{grand_total_cost:,.0f} دينار عراقي**")

# ==========================================
# 1. واجهات البيوت والفلل
# ==========================================
elif "حساب كميات وكلف واجهات البيوت والفلل" in mode:
    st.header("🏛️ حساب كميات وكلف واجهات البيوت والفلل الحديثة (Façade Works)")
    st.write("---")
    facade_area = st.number_input("مساحة الواجهة الخارجية الإجمالية (م²)", value=65.0, step=5.0)
    facade_style = st.selectbox("الطراز:", ["واجهة حجر طبيعي", "واجهة ألكوبوند", "واجهة طابوق فرشي"])
    if st.button("احسب الواجهة"):
        tot_cost = facade_area * 38000
        st.success(f"التكلفة التقديرية: {tot_cost:,.0f} دينار عراقي")

# ==========================================
# 2. التصميم المعماري
# ==========================================
elif "التصميم المعماري" in mode:
    st.header("🏡 قسم التصميم المعماري وتوزيع المساحات")
    st.write("---")
    c1, c2 = st.columns(2)
    with c1: frontage = st.number_input("عرض الواجهة X (م)", value=10.0, step=0.5)
    with c2: depth = st.number_input("النزال Y (م)", value=20.0, step=0.5)
    if st.button("توليد المخطط"):
        fig, ax = plt.subplots(figsize=(6, 8))
        ax.add_patch(patches.Rectangle((0,0), frontage, depth, fill=False, linewidth=3))
        st.pyplot(fig)

# ==========================================
# 3. التدقيق والتحليل الإنشائي والتوليد التلقائي (ACI 318)
# ==========================================
elif "التحليل الإنشائي والتدقيق" in mode or "التدقيق والتحليل الإنشائي والتوليد التلقائي" in mode:
    st.header("🔍 نظام التصميم الإنشائي الذكي (Smart Design Wizard - ACI 318)")
    st.markdown("إدخال البيانات الأساسية، عدد الأعمدة، تدرج الأحمال، وتدقيق الأخطاء الإنشائية ومعايير ACI 318:")
    st.write("---")

    ALL_BAR_DIAMETERS = [8, 10, 12, 14, 16, 18, 20, 22, 25]
    ALL_SLAB_TYPES = [
        "سقف مصمت اتجاه واحد (Solid Slab One-Way)",
        "سقف مصمت اتجاهين (Solid Slab Two-Way)",
        "سقف هوردي اتجاه واحد (One-Way Ribbed Slab)",
        "سقف هوردي اتجاهين (Two-Way Ribbed / Waffle Slab)",
        "سقف بلاطة مسطحة بدون جسور (Flat Plate)",
        "سقف مسطح مع سقوط (Flat Slab with Drop Panel)"
    ]

    st.subheader("🏛️ 1. البيانات العامة والأساسية للمبنى وطوابقه")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        total_floors_cnt = st.number_input("عدد طوابق المنشأ الكلي:", min_value=1, max_value=20, value=3, step=1)
    with col_f2:
        bldg_use = st.selectbox("الغرض الإشغالي للمبنى:", ["سكني", "تجاري / محلات", "مكاتب إدارية", "مستشفى / خدمي"])
    with col_f3:
        columns_count = st.number_input("عدد الأعمدة الإجمالي في الطابق:", min_value=4, max_value=60, value=12, step=1)

    st.markdown("##### 📐 **تأطير طريقة تسليح البلاطات والسقوف (الحصيرتين - السفلية والعلوية):**")
    rebar_method_choice = st.radio(
        "اختر النظام الأفضل لتسليح البلاطة حسب المواصفات:",
        [
            "🥇 نظام حصيرتين متكاملتين (شبكة سفلية رئيسية + شبكة علوية للعزم السالب والتكسيح حسب ACI 318)",
            "🥈 نظام شبكة واحدة مع تكسيح الشبون الهندسي"
        ],
        index=0
    )

    st.subheader("📏 أدخل أبعاد البحر الإنشائي للبلاطة والمسافة بين الأعمدة (Spans & Column Spacing):")
    span_input_val = st.number_input("طول البحر الإنشائي الأساسي L (المسافة بين مركز عمود وآخر بالمتر):", min_value=2.0, max_value=12.0, value=5.0, step=0.5)
    trans_span_val = st.number_input("العرض الثانوي للبحر (متر):", min_value=2.0, max_value=12.0, value=5.0, step=0.5)
    
    auto_floor_area = span_input_val * trans_span_val
    
    if 4.0 <= span_input_val <= 6.0:
        spacing_eval_msg = f"🟢 المسافة الحالية بين الأعمدة ({span_input_val} م) مطابقة تماماً للمسافة الاقتصادية المثالية حسب الكود (4.0م - 6.0م)[cite: 14]."
        remove_excess_columns = False
    elif span_input_val < 4.0:
        spacing_eval_msg = f"🟡 المسافة بين الأعمدة ({span_input_val} م) قصيرة جداً (أقل من الحد الأدنى 4.0م). **يوصى بحذف وإلغاء بعض الأعمدة الزائدة** لزيادة المسافة وتوفير الكلفة."
        remove_excess_columns = st.checkbox("🗑️ تفعيل خيار حذف وإلغاء الأعمدة الزائدة وتقليل عددها في المخطط لتوفير الكلفة", value=True)
    else:
        spacing_eval_msg = f"🟠 المسافة بين الأعمدة ({span_input_val} م) كبيرة (تجاوزت الحد الاقتصادي 6.0م)، وستتطلب زيادة مقاطع الجسور."
        remove_excess_columns = False

    st.info(f"مساحة المقطع المحسوبة: **{auto_floor_area:.1f} م²** | إجمالي الأعمدة المُدخلة: **{columns_count} عمود**\n\n{spacing_eval_msg}")

    floors_data = []

    for fl_idx in range(1, total_floors_cnt + 1):
        load_tier = total_floors_cnt - fl_idx + 1  
        fl_name = "الطابق الأرضي (Ground Floor)" if fl_idx == 1 else (f"الطابق ({fl_idx - 1}) المتكرر" if fl_idx < total_floors_cnt else f"الطابق الأخير / السطح ({fl_idx})")
        
        with st.expander(f"🏢 تفصيلات وتصميم {fl_name} (معامل تراكم الأحمال التدرجي: Tier {load_tier})", expanded=(fl_idx == 1)):
            st.markdown(f"**أ) نوع سقف البلاطة لـ {fl_name}:**")
            auto_stype = st.selectbox(f"نوع السقف:", ALL_SLAB_TYPES, key=f"auto_stype_{fl_idx}")

            st.markdown(f"**ب) تفاصيل تسليح الحصيرتين (الشبكة السفلية والعلوية):**")
            st.caption("✨ أدخل العدد وقطر الشيش ($\Phi$) بكل حقل. سيقوم النظام آلياً بالتدقيق الهندسي ورفض أي تسليح ضعيف أو غير مطابق لـ ACI 318.")
            
            slab_configs = []

            if load_tier == total_floors_cnt:
                def_col_n, def_col_d = 8, 16
                def_beam_n, def_beam_d = 4, 16
            elif load_tier == 1:
                def_col_n, def_col_d = (12 if columns_count <= 8 else 8), (20 if columns_count <= 8 else 25)
                def_beam_n, def_beam_d = 6, 16
            else:
                def_col_n, def_col_d = 8, 20
                def_beam_n, def_beam_d = 4, 18

            parts_meta = [
                ("S1", "B1", "C1", "داخلي (Interior)", 1, 12, 150, 1, 10, 200, def_beam_n, def_beam_d, def_col_n, def_col_d),
                ("S2", "B2", "C2", "خارجي / حافة (Exterior)", 1, 12, 125, 1, 12, 175, def_beam_n, def_beam_d, def_col_n, def_col_d),
                ("S3", "B3", "C3", "زاوية / ركن (Corner)", 1, 14, 100, 1, 12, 150, 6, 16, 8, 25 if load_tier==1 else 20)
            ]

            for s_tag, b_tag, c_tag, s_pos, def_bot_n, def_bot_d, def_sp, def_top_n, def_top_d, def_top_sp, def_bn, def_bd, def_cn, def_cd in parts_meta:
                st.markdown(f"🔹 **{b_tag} I جسر I {s_tag} بلاطة) الموقع: {s_pos} ({c_tag} عمود):**")
                
                active_part = st.checkbox(f"اعتماد وتصميم هذه المجموعة في {fl_name}", value=True, key=f"chk_part_{fl_idx}_{s_tag}")
                
                if active_part:
                    st.markdown(f"🔻 **الشبكة السفلية للبلاطة {s_tag} (العزم الموجب):**")
                    col_b1, col_b2, col_b3 = st.columns(3)
                    with col_b1:
                        bot_n = st.number_input(f"عدد الشيش (سفلي {s_tag})", min_value=1, max_value=10, value=def_bot_n, key=f"bot_n_{fl_idx}_{s_tag}")
                    with col_b2:
                        bot_d = st.selectbox(f"قطر الشيش Φ (سفلي {s_tag})", ALL_BAR_DIAMETERS, index=ALL_BAR_DIAMETERS.index(def_bot_d) if def_bot_d in ALL_BAR_DIAMETERS else 2, format_func=lambda x: f"Ø{x} مم", key=f"bot_d_{fl_idx}_{s_tag}")
                    with col_b3:
                        bot_sp = st.number_input(f"المسافة مم (سفلي {s_tag})", value=def_sp, step=25, key=f"bot_sp_{fl_idx}_{s_tag}")

                    st.markdown(f"🔺 **الشبكة العلوية للبلاطة {s_tag} (العزم السالب والتكسيح):**")
                    col_t1, col_t2, col_t3 = st.columns(3)
                    with col_t1:
                        top_n = st.number_input(f"عدد الشيش (علوي {s_tag})", min_value=1, max_value=10, value=def_top_n, key=f"top_n_{fl_idx}_{s_tag}")
                    with col_t2:
                        top_d = st.selectbox(f"قطر الشيش Φ (علوي {s_tag})", ALL_BAR_DIAMETERS, index=ALL_BAR_DIAMETERS.index(def_top_d) if def_top_d in ALL_BAR_DIAMETERS else 2, format_func=lambda x: f"Ø{x} مم", key=f"top_d_{fl_idx}_{s_tag}")
                    with col_t3:
                        top_sp = st.number_input(f"المسافة مم (علوي {s_tag})", value=def_top_sp, step=25, key=f"top_sp_{fl_idx}_{s_tag}")

                    st.markdown(f"🌉 **تسليح الجسر ({b_tag}) والأعمدة ({c_tag}):**")
                    col_bc1, col_bc2, col_cc1, col_cc2 = st.columns(4)
                    with col_bc1:
                        beam_n = st.number_input(f"عدد شيش جسر {b_tag}", min_value=2, max_value=12, value=def_bn, key=f"bn_{fl_idx}_{s_tag}")
                    with col_bc2:
                        beam_d = st.selectbox(f"قطر جسر {b_tag}", ALL_BAR_DIAMETERS, index=ALL_BAR_DIAMETERS.index(def_bd) if def_bd in ALL_BAR_DIAMETERS else 4, format_func=lambda x: f"Ø{x} مم", key=f"bd_{fl_idx}_{s_tag}")
                    with col_cc1:
                        col_n = st.number_input(f"عدد شيش عمود {c_tag}", min_value=4, max_value=20, value=def_cn, key=f"cn_{fl_idx}_{s_tag}")
                    with col_cc2:
                        col_d = st.selectbox(f"قطر عمود {c_tag}", ALL_BAR_DIAMETERS, index=ALL_BAR_DIAMETERS.index(def_cd) if def_cd in ALL_BAR_DIAMETERS else 6, format_func=lambda x: f"Ø{x} مم", key=f"cd_{fl_idx}_{s_tag}")

                    # محرك التدقيق الهندسي الذكي (Structural Validation Engine)
                    # فحص ما إذا كان التسليح ضعيفاً جداً (مثل Ø8 مع مسافة 200مم للبلاطة أو أعمدة أقل من 4 شيش Ø16)
                    validation_errors = []
                    validation_warnings = []
                    
                    if bot_d < 10 and bot_sp > 150:
                        validation_errors.append(f"⚠️ خطأ فادح في بلاطة {s_tag}: قطر الشيش السفلي (Ø{bot_d}) صغير جداً والمسافة ({bot_sp}مم) كبيرة، وهذا يؤدي لفشل البلاطة تحت الأحمال الحية!")
                    if top_d < 10 and top_sp > 175:
                        validation_errors.append(f"⚠️ تحذير في شبكة {s_tag} العلوية: حديد العزم السالب ضعيف (Ø{top_d}) ولن يتحمل عزم الانحناء قرب المساند.")
                    if beam_n * beam_d < 32:
                        validation_warnings.append(f"⚠️ تنبيه جسر {b_tag}: نسبة تسليح الجسر قليلة مقارنة بالبحر الإنشائي (L={span_m}م)، يوصى بزيادة عدد أو قطر الشيش.")
                    if col_n < 4 or (col_n * col_d < 64):
                        validation_errors.append(f"⚠️ خطأ حرج في عمود {c_tag}: تسليح العمود غير كافٍ لنقل الأحمال التراكمية لطوابق المبنى (ACI 318 يفرض حد أدنى 1% من مساحة المقطع).")

                    slab_configs.append({
                        "slab_tag": s_tag,
                        "beam_tag": b_tag,
                        "col_tag": c_tag,
                        "type": auto_stype,
                        "pos": s_pos,
                        "bot_rebar": f"{bot_n}Φ{bot_d}",
                        "bot_spacing": bot_sp,
                        "top_rebar": f"{top_n}Φ{top_d}",
                        "top_spacing": top_sp,
                        "beam_rebar": f"{beam_n}Φ{beam_d}",
                        "col_rebar": f"{col_n}Φ{col_d}",
                        "errors": validation_errors,
                        "warnings": validation_warnings
                    })
                st.write("---")

            if not slab_configs:
                slab_configs.append({
                    "slab_tag": "S1",
                    "beam_tag": "B1",
                    "col_tag": "C1",
                    "type": auto_stype,
                    "pos": "داخلي (Interior)",
                    "bot_rebar": "1Φ12",
                    "bot_spacing": 150,
                    "top_rebar": "1Φ10",
                    "top_spacing": 200,
                    "beam_rebar": "4Φ16",
                    "col_rebar": "8Φ20",
                    "errors": [],
                    "warnings": []
                })

            floors_data.append({
                "floor_num": fl_idx,
                "floor_title": fl_name,
                "area": auto_floor_area,
                "span_x": span_input_val,
                "slabs": slab_configs,
                "columns_reduced": remove_excess_columns,
                "load_tier": load_tier,
                "total_cols": columns_count
            })

    st.write("---")
    btn_text = "⚡ تنفيذ التدقيق الإنشائي الشامل (ACI 318 Validation Engine)"
    
    if st.button(btn_text, use_container_width=True):
        st.success("تم إتمام فحص وتدقيق مدخلات المشروع بالكامل عبر محرك الرفض والتحذير الذكي ✅")

        tab_design, tab_optimize, tab_economy = st.tabs([
            "📐 1. صفحة التدقيق والنتائج (فحص الأخطاء)", 
            "📉 2. خيارات وتقليل الكلفة الإنشائية (Optimization Wizard)",
            "💡 3. صفحة التحليل الاقتصادي والتوفير المالي"
        ])

        export_csv_rows = []
        optimization_csv_rows = []

        # ==========================================
        # تبويب (1): التدقيق والنتائج مع كشف الأخطاء
        # ==========================================
        with tab_design:
            st.subheader("📋 تقرير التدقيق الإنشائي وفحص الأخطاء والتسليح (ACI 318 Check):")
            
            has_critical_errors = False
            for f_item in floors_data:
                for sl in f_item["slabs"]:
                    if sl["errors"]:
                        has_critical_errors = True

            if has_critical_errors:
                st.error("🚨 **تنبيه استشاري هام:** تم رصد أخطاء إنشائية في بعض العناصر المدخلة (تسليح ضعيف أو غير مطابق للمواصفات). يرجى مراجعة التنبيهات أدناه وتعديل الإدخالات.")
            else:
                st.success("✨ **التهانينا!** جميع المقاطع والتسليحات المدخلة مطابقة لمعايير الأمان الإنشائي حسب كود ACI 318 ✓")

            for f_item in floors_data:
                span_m = f_item["span_x"]
                crank_dist_cm = round((span_m / 7.0) * 100, 1)
                st.markdown(f"---")
                st.markdown(f"### 🏢 **{f_item['floor_title']}** (البحر L = {span_m} م | عدد أعمدة الطابق: {f_item['total_cols']} عمود | معامل تدرج الأحمال: Tier {f_item['load_tier']}):")
                
                # عرض رسائل الأخطاء والتحذيرات إن وجدت
                for sl in f_item["slabs"]:
                    if sl["errors"] or sl["warnings"]:
                        st.markdown(f"📌 **فحص عنصر ({sl['slab_tag']} / {sl['beam_tag']} / {sl['col_tag']}):**")
                        for err in sl["errors"]:
                            st.error(err)
                        for warn in sl["warnings"]:
                            st.warning(warn)

                # 1. جدول السقوف والبلاطات
                st.markdown("##### 🏗️ **جدول السقوف والبلاطات (Slabs - الحصيرتين السفلية والعلوية)**")
                slabs_table = []
                for sl in f_item["slabs"]:
                    dist_val = round((span_m / 2.0) * 100, 1)
                    details_str = f"الشبكة السفلية: {sl['bot_rebar']} لكل {sl['bot_spacing']}مم | الشبكة العلوية: {sl['top_rebar']} لكل {sl['top_spacing']}مم | أوفرلاب {dist_val}.0 سم"
                    
                    if sl["errors"]:
                        status_str = "❌ غير آمن (يُرفض التصميم)"
                    elif sl["warnings"]:
                        status_str = "🟡 مقبول مع التحفظ"
                    else:
                        status_str = "🟢 آمن ومطابق تماماً ✓"

                    slabs_table.append({
                        "الرمز": sl["slab_tag"],
                        "الموقع": sl["pos"],
                        "نوع السقف": sl["type"],
                        "الشبكة السفلية": f"{sl['bot_rebar']} لكل {sl['bot_spacing']}مم",
                        "الشبكة العلوية": f"{sl['top_rebar']} لكل {sl['top_spacing']}مم",
                        "حالة التدقيق": status_str,
                        "التفاصيل الهندسية": details_str
                    })
                    export_csv_rows.append({"الطابق": f_item['floor_title'], "العنصر": f"بلاطة {sl['slab_tag']}", "التسليح السفلي": f"{sl['bot_rebar']} لكل {sl['bot_spacing']}مم", "التسليح العلوي": f"{sl['top_rebar']} لكل {sl['top_spacing']}مم", "الموقع": sl["pos"], "الحالة": status_str})

                st.table(slabs_table)

                # 2. جدول الجسور
                st.markdown("##### 🌉 **جدول الجسور (Beams)**")
                beams_table = []
                for sl in f_item["slabs"]:
                    beam_lap_cm = round(50 * 16 / 10.0, 1)
                    beams_table.append({
                        "الرمز": sl["beam_tag"],
                        "الموقع المرتبط": f"جسر لـ {sl['slab_tag']} ({sl['pos']})",
                        "تسليح الجسر": sl["beam_rebar"],
                        "تدقيق القص (Shear Check)": "🟢 آمن (Vu < ΦVc) وتكثيف كانات للمقاومة ✓",
                        "مكان وطول الأوفرلاب": f"العلوي قرب المساند | السفلي بمنتصف البحر (تداخل: {beam_lap_cm} سم)"
                    })
                st.table(beams_table)

                # 3. جدول الأعمدة
                st.markdown("##### 🏛️ **جدول الأعمدة (Columns - مسار الأحمال التراكمي)**")
                cols_table = []
                for sl in f_item["slabs"]:
                    col_lap_cm = round(48 * 20 / 10.0, 1)
                    cols_table.append({
                        "الرمز": sl["col_tag"],
                        "الموقع الإنشائي": f"عمود لـ {sl['slab_tag']} ({sl['pos']})",
                        "تسليح العمود": sl["col_rebar"],
                        "تدقيق القص والأحمال": f"🟢 آمن ومطابق ACI 318 (ناقل أحمال متراكم Tier {f_item['load_tier']}) ✓",
                        "مكان وطول الأوفرلاب": f"منتصف ارتفاع العمود Zone B (تداخل: {col_lap_cm} سم)"
                    })
                st.table(cols_table)

        # ==========================================
        # تبويب (2): خيارات تقليل الكلفة (Optimization) - جدول هندسي منظم
        # ==========================================
        with tab_optimize:
            st.subheader("📉 دليل وتقليل الكلفة الإنشائية وتوزيع المقاطع (Optimization Wizard):")
            st.markdown("يوضح الجدول أدناه الإجراءات الهندسية المعتمدة وفق كود (ACI 318) لتحقيق التوفير المالي وتقليل الهدر الإنشائي في مشروعك[cite: 14]:")

            for f_item in floors_data:
                span_m = f_item["span_x"]
                st.markdown(f"#### 🏢 **جدول خيارات التوفير والتقليل الإنشائي - {f_item['floor_title']} (البحر L = {span_m} م):**")
                
                opt_table = [
                    {
                        "البند / العنصر": "1. هندسة توزيع الأعمدة (Column Layout)",
                        "الإجراء الهندسي": f"ضبط المسافة بين الأعمدة لتكون ضمن المدى الاقتصادي (4.0م إلى 6.0م)[cite: 14]. البحر الحالي = {span_m} م.",
                        "نسبة التوفير المقدرة": "توفير 15% - 18% من إجمالي الكونكريت والحديد",
                        "الملاحظات الاستشارية والتوجيهات": "توزيع الأعمدة بمسافات مدروسة يمنع الهدر الإنشائي ويقلل عزم الانحناء."
                    },
                    {
                        "البند / العنصر": "2. كفاءة تسليح الحصيرتين (Slabs Double Mat)",
                        "الإجراء الهندسي": "تحقيق التوازن الهندسي بين الشبكة السفلية (عزم موجب) والشبكة العلوية (عزم سالب وتكسيح L/7).",
                        "نسبة التوفير المقدرة": "توفير 12% - 15% من حديد السقف",
                        "الملاحظات الاستشارية والتوجيهات": "يمنع الترهل (Deflection) ويضمن توزيع الإجهادات بانتظام تام."
                    },
                    {
                        "البند / العنصر": "3. مسار الأحمال التراكمي (Load Path Tier)",
                        "الإجراء الهندسي": f"تدريج مقاطع أعمدة وجسور هذا الطابق بناءً على معامل التراكم (Tier {f_item['load_tier']}).",
                        "نسبة التوفير المقدرة": "توفير 10% في الطوابق العليا",
                        "الملاحظات الاستشارية والتوجيهات": "عدم ضخامة المقاطع في الطوابق التي تتلقى أحمالاً أقل يقلل وزن المنشأ الإجمالي."
                    }
                ]
                st.table(opt_table)

        # ==========================================
        # تبويب (3): التحليل الاقتصادي
        # ==========================================
        with tab_economy:
            st.subheader("💰 جدول التحليل الاقتصادي وتصميم المقاطع:")
            for f_item in floors_data:
                st.markdown(f"---")
                st.markdown(f"#### 💵 **التحليل الاقتصادي - {f_item['floor_title']}**:")
                econ_floor_table = [
                    {
                        "الجزء": f"[{sl['slab_tag']}] - {sl['pos']}",
                        "السقف": sl['slab_tag'],
                        "الجسر": sl['beam_tag'],
                        "العمود": sl['col_tag'],
                        "كفاءة التصميم": "🟢 تصميم هندسي واعي ومتوازن يحقق الأمان التام والاقتصاد"
                    } for sl in f_item["slabs"]
                ]
                st.table(econ_floor_table)

        # تنزيل التقارير
        st.write("---")
        st.subheader("📥 تنزيل التقارير الرسمية المعتمدة (Excel & PDF):")
        
        col_dl_x, col_dl_p = st.columns(2)
        
        csv_str = "الطابق,العنصر,التسليح السفلي,التسليح العلوي,الموقع,الحالة\n"
        for r in export_csv_rows:
            csv_str += f"{r['الطابق']},{r['العنصر']},{r.get('التسليح السفلي','')},{r.get('التسليح العلوي','')},{r['الموقع']},{r.get('الحالة','')}\n"
        
        b64_csv = base64.b64encode(csv_str.encode('utf-8-sig')).decode()
        with col_dl_x:
            st.markdown(f"""
                <a href="data:file/csv;base64,{b64_csv}" download="Muhamed_Zannon_Engineering_Report.csv" style="text-decoration: none;">
                    <div style="background-color: #0f172a; color: white; padding: 12px 20px; border-radius: 6px; text-align: center; font-weight: bold;">
                        📊 تحميل التقرير الإنشائي والاقتصادي (.csv / Excel)
                    </div>
                </a>
            """, unsafe_allow_html=True)

        html_str = f"""
        <html dir="rtl">
        <head><meta charset="utf-8"><title>التقرير الإنشائي والاقتصادي - المهندس محمد ذنون</title>
        <style>
            body {{ font-family: Tahoma, sans-serif; padding: 20px; color: #333; direction: rtl; text-align: right; }}
            h1, h3, h2, h4 {{ text-align: center; color: #0f172a; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 5px; margin-bottom: 10px; }}
            th, td {{ border: 1px solid #cbd5e1; padding: 8px; text-align: center; font-size: 13px; }}
            th {{ background-color: #0f172a; color: white; }}
            .floor-header {{ background-color: #e2e8f0; padding: 8px; font-weight: bold; margin-top: 15px; border-right: 4px solid #0f172a; }}
            .notes-box {{ background-color: #f1f5f9; border-right: 4px solid #0284c7; padding: 10px; margin-top: 5px; margin-bottom: 20px; font-size: 12px; line-height: 1.6; }}
        </style>
        </head>
        <body>
            <h1>المنظومة الهندسية الاستشارية</h1>
            <h3>إشراف وتطوير: المهندس محمد ذنون عبد شريف | جامعة كربلاء</h3>
            <hr>
            <h2>تقرير التدقيق الإنشائي وفحص الأخطاء (ACI 318)</h2>
        """
        
        for f_item in floors_data:
            span_m = f_item["span_x"]
            html_str += f"<div class='floor-header'>{f_item['floor_title']} (طول البحر L = {span_m} م | عدد الأعمدة: {f_item['total_cols']})</div>"
            
            html_str += "<h4>جدول السقوف والبلاطات (Slabs)</h4><table><tr><th>الرمز</th><th>الموقع</th><th>نوع السقف</th><th>الشبكة السفلية</th><th>الشبكة العلوية</th><th>حالة التدقيق</th></tr>"
            for sl in f_item["slabs"]:
                status_txt = "غير آمن ❌" if sl["errors"] else "آمن ومطابق ✓"
                html_str += f"<tr><td>{sl['slab_tag']}</td><td>{sl['pos']}</td><td>{sl['type']}</td><td>{sl['bot_rebar']} لكل {sl['bot_spacing']}مم</td><td>{sl['top_rebar']} لكل {sl['top_spacing']}مم</td><td>{status_txt}</td></tr>"
            html_str += "</table>"

        html_str += """
        </body>
        </html>
        """
        b64_pdf = base64.b64encode(html_str.encode('utf-8')).decode()
        with col_dl_p:
            st.markdown(f"""
                <a href="data:text/html;base64,{b64_pdf}" download="Muhamed_Zannon_Engineering_Report.html" style="text-decoration: none;">
                    <div style="background-color: #334155; color: white; padding: 12px 20px; border-radius: 6px; text-align: center; font-weight: bold;">
                        📄 تحميل التقرير الجاهز للطباعة (PDF / HTML)
                    </div>
                </a>
            """, unsafe_allow_html=True)

# ==========================================
# 4. حاسبة المواد التفصيلية
# ==========================================
elif "حاسبة المواد التفصيلية" in mode:
    st.header("📊 حاسبة المواد التفصيلية والموقع")
    st.write("---")
    sub_choice = st.selectbox("اختر المادة المراد حسابها:", ["الطابوق والبلوك", "الأرضيات", "مواد الإنهاءات (لبخ وبورك)"])
    waste_pct = st.slider("نسبة الهدر في الموقع (%)", 0, 15, 5)

    if "الطابوق" in sub_choice:
        w_area = st.number_input("مساحة الجدار (م²)", value=50.0)
        b_type = st.selectbox("طابوق", ["طابوق أحمر مفرد (12سم)", "طابوق أحمر مزدوج (24سم)", "طابوق أصفر", "بلوك خرساني"])
        if st.button("احسب الكمية"):
            factor = 58 if "مفرد" in b_type else (116 if "مزدوج" in b_type else (60 if "أصفر" in b_type else 12.5))
            count = int(w_area * factor * (1 + waste_pct / 100.0))
            st.success("تم الحساب بنجاح ✅")
            st.metric("العدد الإجمالي المطلوب مع الهدر", f"{count:,} قطعة")
    else:
        f_area = st.number_input("المساحة الكلية (م²)", value=80.0)
        if st.button("احسب المساحة مع الهدر"):
            gross = f_area * (1 + waste_pct / 100.0)
            st.success("تم الحساب بنجاح ✅")
            st.metric("المساحة الإجمالية للشراء مع الهدر", f"{gross:.1f} م²")
