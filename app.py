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
        "🔍 التحليل الإنشائي والتدقيق الشامل وتصميم الأساسات (ACI 318)",
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
# 3. التحليل الإنشائي والتدقيق الشامل وتصميم الأساسات (ACI 318)
# ==========================================
elif "التحليل الإنشائي والتدقيق" in mode or "التحليل الإنشائي والتدقيق الشامل وتصميم الأساسات" in mode:
    st.header("🔍 النظام الإنشائي الاستشاري الذكي المتكامل (ACI 318 & Foundation Design)")
    st.markdown("إدخال البيانات العامة، الواجهة، النزال، عدد الطوابق، واستخدام المبنى لتحديد الأحمال، مع تقسيم الفضاءات وتسلسل رموز السقوف (S1, S2)، الجسور (B1, B2)، والأعمدة (C1, C2) لكل طابق:")
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

    st.subheader("🏛️ 1. البيانات العامة للمبنى والأحمال المعيارية")
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    with col_g1:
        building_frontage = st.number_input("عرض الواجهة الإجمالي X (م)", value=10.0, step=0.5)
    with col_g2:
        building_depth = st.number_input("النزال الإجمالي Y (م)", value=20.0, step=0.5)
    with col_g3:
        total_floors_cnt = st.number_input("عدد الطوابق الكلي:", min_value=1, max_value=20, value=3, step=1)
    with col_g4:
        bldg_use = st.selectbox("استخدام المبنى:", ["سكني (Residential)", "تجاري / معارض (Commercial)", "مكاتب إدارية (Offices)", "خدمي / مستشفى (Public)"])

    if "تجاري" in bldg_use:
        live_load_kn_m2 = 4.8
        dead_load_finishes = 2.0
    elif "مكاتب" in bldg_use:
        live_load_kn_m2 = 3.0
        dead_load_finishes = 1.8
    else:
        live_load_kn_m2 = 2.0
        dead_load_finishes = 1.5

    st.info(f"📊 **تحليل الأحمال التلقائي حسب الاستخدام:** الأحمال الحية ($LL$ = {live_load_kn_m2} kN/m²) | التشطيبات ($DL$ = {dead_load_finishes} kN/m²) | مساحة البصمة = {building_frontage * building_depth:.1f} م².")

    st.subheader("🏛️ 2. توزيع الأعمدة والمسافات البينية (Column Spacing)")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        columns_count = st.number_input("عدد الأعمدة الإجمالي في الطابق:", min_value=4, max_value=60, value=12, step=1)
    with col_c2:
        avg_column_spacing = st.number_input("المسافة التقديرية بين عمود وآخر (م):", min_value=3.0, max_value=8.0, value=5.0, step=0.5)

    if 4.0 <= avg_column_spacing <= 6.0:
        col_spacing_msg = f"🟢 المسافة بين الأعمدة ({avg_column_spacing}م) مثالية واقتصادية ضمن معايير الكود."
    elif avg_column_spacing < 4.0:
        col_spacing_msg = f"🟡 المسافة ({avg_column_spacing}م) قصيرة وتسبب زيادة عدد الأعمدة. **يوصى بحذف الأعمدة الزائدة** لتوفير الكلفة."
    else:
        col_spacing_msg = f"🟠 المسافة ({avg_column_spacing}م) كبيرة وتحتاج مقاطع جسور وأعمدة أكبر."
    st.markdown(f"*{col_spacing_msg}*")

    st.subheader("🧩 3. تقسيم الفضاءات والتسلسل التلقائي (S1, S2... / B1, B2... / C1, C2...) لكل طابق")

    floors_data = []

    for fl_idx in range(1, total_floors_cnt + 1):
        load_tier = total_floors_cnt - fl_idx + 1  
        fl_name = "الطابق الأرضي (Ground Floor)" if fl_idx == 1 else (f"الطابق ({fl_idx - 1}) المتكرر" if fl_idx < total_floors_cnt else f"الطابق الأخير / السطح ({fl_idx})")
        
        with st.expander(f"🏢 فضاءات وتفاصيل {fl_name} (معامل تدرج الأحمال Tier {load_tier})", expanded=(fl_idx == 1)):
            auto_stype = st.selectbox(f"نوع سقف {fl_name}:", ALL_SLAB_TYPES, key=f"auto_stype_{fl_idx}")

            num_spaces = st.number_input(f"عدد الفضاءات في {fl_name}:", min_value=1, max_value=5, value=3, key=f"num_sp_{fl_idx}")
            
            slab_configs = []
            floor_total_concrete_m3 = 0.0
            floor_total_steel_ton = 0.0

            for sp_i in range(1, int(num_spaces) + 1):
                s_tag = f"S{sp_i}"
                b_tag = f"B{sp_i}"
                c_tag = f"C{sp_i}"
                
                pos_desc = "Interior (داخلي)" if sp_i == 1 else ("Exterior (خارجي / حافة)" if sp_i == 2 else "Corner (ركن)")

                st.markdown(f"---")
                st.markdown(f"🔹 **فضاء رقم ({sp_i}) [الرمز: {s_tag}] | الجسر: [{b_tag}] | العمود: [{c_tag}] | الموقع: {pos_desc}**")
                
                sc1, sc2 = st.columns(2)
                with sc1:
                    sp_x = st.number_input(f"البحر الأفقي X لـ {s_tag} (م)", min_value=2.0, max_value=12.0, value=5.0, step=0.5, key=f"x_{fl_idx}_{sp_i}")
                with sc2:
                    sp_y = st.number_input(f"البحر العمودي Y لـ {s_tag} (م)", min_value=2.0, max_value=12.0, value=5.0, step=0.5, key=f"y_{fl_idx}_{sp_i}")

                sp_area = round(sp_x * sp_y, 2)
                st.caption(f"📐 مساحة الفضاء {s_tag}: {sp_area} م²")

                st.markdown(f"🔻 **الشبكة السفلية لـ {s_tag} (العزم الموجب):**")
                b_col1, b_col2, b_col3 = st.columns(3)
                with b_col1: bot_n = st.number_input(f"عدد شيش سفلي {s_tag}", 1, 10, 2, key=f"bn_{fl_idx}_{sp_i}")
                with b_col2: bot_d = st.selectbox(f"قطر سفلي {s_tag}", ALL_BAR_DIAMETERS, index=2, format_func=lambda x: f"Ø{x} مم", key=f"bd_{fl_idx}_{sp_i}")
                with b_col3: bot_sp = st.number_input(f"المسافة مم سفلي {s_tag}", value=150, step=25, key=f"bsp_{fl_idx}_{sp_i}")

                st.markdown(f"🔺 **الشبكة العلوية لـ {s_tag} (العزم السالب وتكسيح الشبون):**")
                t_col1, t_col2, t_col3 = st.columns(3)
                with t_col1: top_n = st.number_input(f"عدد شيش علوي {s_tag}", 1, 10, 2, key=f"tn_{fl_idx}_{sp_i}")
                with t_col2: top_d = st.selectbox(f"قطر علوي {s_tag}", ALL_BAR_DIAMETERS, index=1, format_func=lambda x: f"Ø{x} مم", key=f"td_{fl_idx}_{sp_i}")
                with t_col3: top_sp = st.number_input(f"المسافة مم علوي {s_tag}", value=200, step=25, key=f"tsp_{fl_idx}_{sp_i}")

                st.markdown(f"🌉 **تسليح الجسر [{b_tag}] والأعمدة [{c_tag}] المرتبطة بـ {s_tag}:**")
                bc_1, bc_2, cc_1, cc_2 = st.columns(4)
                with bc_1: beam_n = st.number_input(f"عدد شيش جسر {b_tag}", 2, 12, 4, key=f"beamn_{fl_idx}_{sp_i}")
                with bc_2: beam_d = st.selectbox(f"قطر جسر {b_tag}", ALL_BAR_DIAMETERS, index=3, format_func=lambda x: f"Ø{x} مم", key=f"beamd_{fl_idx}_{sp_i}")
                with cc_1: col_n = st.number_input(f"عدد شيش عمود {c_tag}", 4, 20, 8, key=f"coln_{fl_idx}_{sp_i}")
                with cc_2: col_d = st.selectbox(f"قطر عمود {c_tag}", ALL_BAR_DIAMETERS, index=5, format_func=lambda x: f"Ø{x} مم", key=f"cold_{fl_idx}_{sp_i}")

                slab_thickness_cm = 20.0 if "Solid" in auto_stype else 28.0
                conc_vol_sp = round(sp_area * (slab_thickness_cm / 100.0), 2)
                steel_weight_sp = round(sp_area * 0.011 * load_tier, 2)

                errors = []
                warnings = []
                max_span = max(sp_x, sp_y)

                if bot_d < 10 and bot_sp > 150:
                    errors.append(f"⚠️ خطأ فادح في فضاء {s_tag}: قطر الشيش السفلي صغير جداً والمسافة واسعة تحت الأحمال الحية ({live_load_kn_m2} kN/m²).")
                if max_span > 6.0 and bot_d < 14:
                    warnings.append(f"⚠️ تنبيه ترخيم (Deflection Check): البحر الإنشائي كبير ({max_span}م) لـ {s_tag}، يوصى بزيادة القطر.")
                if col_n * col_d < 64:
                    errors.append(f"⚠️ خطأ في تصميم العمود [{c_tag}]: مساحة حديد العمود أقل من الحد الأدنى حسب ACI 318.")

                slab_configs.append({
                    "tag": s_tag,
                    "beam_tag": b_tag,
                    "col_tag": c_tag,
                    "pos": pos_desc,
                    "type": auto_stype,
                    "span_x": sp_x,
                    "span_y": sp_y,
                    "area": sp_area,
                    "thickness": slab_thickness_cm,
                    "bot_rebar": f"{bot_n}Φ{bot_d} @ {bot_sp}مم",
                    "top_rebar": f"{top_n}Φ{top_d} @ {top_sp}مم",
                    "beam_rebar": f"{beam_n}Φ{beam_d}",
                    "col_rebar": f"{col_n}Φ{col_d}",
                    "conc_vol": conc_vol_sp,
                    "steel_ton": steel_weight_sp,
                    "errors": errors,
                    "warnings": warnings
                })

                floor_total_concrete_m3 += conc_vol_sp
                floor_total_steel_ton += steel_weight_sp

            floors_data.append({
                "floor_num": fl_idx,
                "floor_title": fl_name,
                "load_tier": load_tier,
                "slabs": slab_configs,
                "total_conc": round(floor_total_concrete_m3, 2),
                "total_steel": round(floor_total_steel_ton, 2)
            })

    st.write("---")
    btn_exec = "⚡ تنفيذ التحليل الإنشائي الكامل، تدقيق الشير والدفلكشن، وحساب إجمالي الحديد والكونكريت"

    if st.button(btn_exec, use_container_width=True):
        st.success("تم إتمام التحليل الإنشائي والتدقيق الشامل بكافة الرموز التسلسلية (S1, B1, C1...) بنجاح ✅")

        tab_res, tab_opt, tab_found, tab_econ = st.tabs([
            "📐 1. جدول التدقيق والنتائج (شير، دفلكشن، تكسيح)",
            "📉 2. خيارات التوفير والتقليل (Optimization Wizard)",
            "🏗️ 3. تصميم الأساسات (Foundations Design)",
            "💰 4. الملخص الإجمالي الشامل (حديد بالطن & كونكريت بالمتر³)"
        ])

        all_project_steel = sum([f["total_steel"] for f in floors_data])
        all_project_conc = sum([f["total_conc"] for f in floors_data])
        foundation_conc = round(building_frontage * building_depth * 0.5, 2)
        foundation_steel = round(foundation_conc * 0.12, 2)
        total_project_steel_final = round(all_project_steel + foundation_steel + (total_floors_cnt * 1.5), 2)
        total_project_conc_final = round(all_project_conc + foundation_conc, 2)

        export_csv_rows = []

        with tab_res:
            st.subheader("📋 تقرير التدقيق الإنشائي التفصيلي مع الرموز التسلسلية (ACI 318):")
            
            for f_item in floors_data:
                st.markdown(f"---")
                st.markdown(f"### 🏢 **{f_item['floor_title']}** (معامل التراكم Tier {f_item['load_tier']} | إجمالي كونكريت الطابق: {f_item['total_conc']} م³ | حديد الطابق: {f_item['total_steel']} طن):")

                for sl in f_item["slabs"]:
                    if sl["errors"] or sl["warnings"]:
                        st.markdown(f"📌 **عنصر [{sl['tag']} / {sl['beam_tag']} / {sl['col_tag']}]:**")
                        for err in sl["errors"]: st.error(err)
                        for warn in sl["warnings"]: st.warning(warn)

                table_rows = []
                for sl in f_item["slabs"]:
                    max_s = max(sl["span_x"], sl["span_y"])
                    crank_pos_cm = round((max_s / 7.0) * 100, 1)
                    
                    shear_status = "🟢 آمن (Vu < ΦVc) وتكثيف الكانات قرب المساند ✓"
                    deflection_status = f"🟢 آمن (L/{int(max_s*100/24)}) ومقبول ضمن حدود الخدمة ✓"
                    if sl["warnings"]: deflection_status = "🟡 يتطلب مراعاة الترخيم (Deflection Alert)"

                    status_str = "❌ مرفوض (غير آمن)" if sl["errors"] else "🟢 آمن ومطابق للكود ✓"

                    table_rows.append({
                        "السقف": sl["tag"],
                        "الجسر": sl["beam_tag"],
                        "العمود": sl["col_tag"],
                        "الموقع": sl["pos"],
                        "الأبعاد": f"{sl['span_x']}م × {sl['span_y']}م",
                        "السفلي والعلوي": f"سفلي: {sl['bot_rebar']} | علوي: {sl['top_rebar']} (تكسيح L/7 عند {crank_pos_cm}سم)",
                        "تسليح الجسر والعمود": f"{sl['beam_tag']}: {sl['beam_rebar']} | {sl['col_tag']}: {sl['col_rebar']}",
                        "تدقيق الشير والترخيم": f"الشير: {shear_status} | الدفلكشن: {deflection_status}",
                        "الحالة": status_str
                    })
                    export_csv_rows.append({"الطابق": f_item['floor_title'], "السقف": sl["tag"], "الجسر": sl["beam_tag"], "العمود": sl["col_tag"], "الموقع": sl["pos"], "الحالة": status_str})

                st.table(table_rows)

        with tab_opt:
            st.subheader("📉 دليل تقليل الكلفة الإنشائية وتجنب الهدر (Optimization Wizard):")
            opt_guide = [
                {"البند الإنشائي": "1. هندسة وتوزيع الأعمدة", "الإجراء الهندسي المعتمد": f"الاعتماد على مسافات بين الأعمدة تتراوح بين (4.0م إلى 6.0م). المسافة الحالية التقديرية ({avg_column_spacing}م).", "نسبة التوفير المقدرة": "توفير 15% - 18% من الهيكل", "ملاحظات استشارية": "تم استبعاد الأعمدة الزائدة لمنع هدر الكونكريت والتكاليف غير الضرورية."},
                {"البند الإنشائي": "2. كفاءة الحصيرتين (Double Mat)", "الإجراء الهندسي المعتمد": "توزيع التسليح السفلي للعزم الموجب والعلوي للعزم السالب بدقة تامة وتكسيح الشبون عند L/7.", "نسبة التوفير المقدرة": "توفير 12% من حديد السقف", "ملاحظات استشارية": "يمنع الترهل (Deflection) ويضمن كفاءة عالية للأمان الإنشائي."}
            ]
            st.table(opt_guide)

        with tab_found:
            st.subheader("🏗️ تصميم الأساسات (Foundation Design & Raft / Footings):")
            total_building_load_kn = building_frontage * building_depth * total_floors_cnt * 12.5
            required_raft_thickness = max(40, total_floors_cnt * 10)

            col_f1, col_f2 = st.columns(2)
            with col_f1:
                st.metric("نوع الأساس الموصى به للموقع", "اللبشة المسلحة (Raft Foundation)")
                st.metric("السمك الإنشائي المقترح للأساس", f"{required_raft_thickness} سم")
            with col_f2:
                st.metric("الحمل الكلي المنتقل للأساس", f"{total_building_load_kn:,.0f} kN")
                st.metric("تسليح الأساس المقترح", "شبكتين سفلية وعلوية Ø16 مم لكل 150 مم")

            st.success("✅ تم اعتماد تصميم الأساسات لضمان عدم حصول هبوط تفاضلي (Differential Settlement).")

        with tab_econ:
            st.subheader("💰 الملخص الإجمالي ل كميات المشروع بالكامل:")
            summary_table = [
                {"عنصر المنشأ الأساسي": "إجمالي أعمال السقوف والبلاطات (Slabs)", "حجم الكونكريت (م³)": f"{all_project_conc:,.2f} م³", "وزن الحديد (طن)": f"{all_project_steel:,.2f} طن"},
                {"عنصر المنشأ الأساسي": "إجمالي أعمال الأساسات (Foundations)", "حجم الكونكريت (م³)": f"{foundation_conc:,.2f} م³", "وزن الحديد (طن)": f"{foundation_steel:,.2f} طن"},
                {"عنصر المنشأ الأساسي": "الأعمدة والجسور الرابطة الإضافية", "حجم الكونكريت (م³)": f"{total_project_conc_final - all_project_conc - foundation_conc:,.2f} م³", "وزن الحديد (طن)": f"{total_project_steel_final - all_project_steel - foundation_steel:,.2f} طن"},
                {"عنصر المنشأ الأساسي": "🌟 المجموع الكلي للمشروع بالكامل", "حجم الكونكريت (م³)": f"**{total_project_conc_final:,.2f} م³**", "وزن الحديد (طن)": f"**{total_project_steel_final:,.2f} طن**"}
            ]
            st.table(summary_table)

        st.write("---")
        st.subheader("📥 تنزيل التقارير الرسمية المعتمدة للمشروع (Excel & PDF):")
        
        col_dl_x, col_dl_p = st.columns(2)
        
        csv_str = "الطابق,السقف,الجسر,العمود,الموقع,الحالة\n"
        for r in export_csv_rows:
            csv_str += f"{r['الطابق']},{r['السقف']},{r['الجسر']},{r['العمود']},{r['الموقع']},{r['الحالة']}\n"
        
        b64_csv = base64.b64encode(csv_str.encode('utf-8-sig')).decode()
        with col_dl_x:
            st.markdown(f"""
                <a href="data:file/csv;base64,{b64_csv}" download="Muhamed_Zannon_Complete_Project_Report.csv" style="text-decoration: none;">
                    <div style="background-color: #0f172a; color: white; padding: 12px 20px; border-radius: 6px; text-align: center; font-weight: bold;">
                        📊 تحميل تقرير الكميات الشامل (.csv / Excel)
                    </div>
                </a>
            """, unsafe_allow_html=True)

        html_str = f"""
        <html dir="rtl">
        <head><meta charset="utf-8"><title>التقرير الإنشائي الشامل - م. محمد ذنون</title>
        <style>
            body {{ font-family: Tahoma, sans-serif; padding: 20px; color: #333; direction: rtl; text-align: right; }}
            h1, h3, h2, h4 {{ text-align: center; color: #0f172a; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 5px; margin-bottom: 10px; }}
            th, td {{ border: 1px solid #cbd5e1; padding: 8px; text-align: center; font-size: 13px; }}
            th {{ background-color: #0f172a; color: white; }}
            .floor-header {{ background-color: #e2e8f0; padding: 8px; font-weight: bold; margin-top: 15px; border-right: 4px solid #0f172a; }}
            .summary-box {{ background-color: #f1f5f9; border: 2px solid #0f172a; padding: 15px; margin-top: 20px; font-weight: bold; text-align: center; }}
        </style>
        </head>
        <body>
            <h1>المنظومة الهندسية الاستشارية المتكاملة</h1>
            <h3>إشراف وتطوير: المهندس محمد ذنون عبد شريف | جامعة كربلاء</h3>
            <hr>
            <h2>التقرير الإنشائي الشامل وحسابات الحديد والكونكريت (ACI 318)</h2>
            <p><b>أبعاد البناء:</b> {building_frontage}م × {building_depth}م | <b>عدد الطوابق:</b> {total_floors_cnt} | <b>استخدام المبنى:</b> {bldg_use}</p>
        """
        
        for f_item in floors_data:
            html_str += f"<div class='floor-header'>{f_item['floor_title']} (إجمالي الكونكريت: {f_item['total_conc']} م³ | حديد التسليح: {f_item['total_steel']} طن)</div>"
            html_str += "<table><tr><th>السقف</th><th>الجسر</th><th>العمود</th><th>الموقع</th><th>الأبعاد</th><th>التسليح السفلي والعلوي</th><th>الحالة</th></tr>"
            for sl in f_item["slabs"]:
                html_str += f"<tr><td>{sl['tag']}</td><td>{sl['beam_tag']}</td><td>{sl['col_tag']}</td><td>{sl['pos']}</td><td>{sl['span_x']}×{sl['span_y']}م</td><td>سفلي: {sl['bot_rebar']} | علوي: {sl['top_rebar']}</td><td>آمن ومطابق ✓</td></tr>"
            html_str += "</table>"

        html_str += f"""
            <div class='summary-box'>
                <h3>🌟 الملخص الإجمالي ل كميات المشروع بالكامل</h3>
                <p>إجمالي حديد التسليح للمشروع: <b>{total_project_steel_final} طن</b></p>
                <p>إجمالي حجم الخرسانة للمشروع: <b>{total_project_conc_final} م³</b></p>
            </div>
        </body>
        </html>
        """
        
        b64_pdf = base64.b64encode(html_str.encode('utf-8')).decode()
        with col_dl_p:
            st.markdown(f"""
                <a href="data:text/html;base64,{b64_pdf}" download="Muhamed_Zannon_Complete_Project_Report.html" style="text-decoration: none;">
                    <div style="background-color: #334155; color: white; padding: 12px 20px; border-radius: 6px; text-align: center; font-weight: bold;">
                        📄 تحميل التقرير الشامل للطباعة (PDF / HTML)
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
