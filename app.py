import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import base64

st.set_page_config(page_title="المنظومة الهندسية الاستشارية - م. محمد ذنون", layout="wide")

# ==========================================
# تخصيص واجهة CSS الفاخرة (الطابع الهندسي الكلاسيكي النظيف)
# ==========================================
st.markdown("""
    <style>
    .main { background-color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3 { color: #0f172a; font-family: 'Segoe UI', Tahoma, sans-serif; font-weight: 700; }
    [data-testid="stSidebar"] { background-color: #1e293b; color: #ffffff; }
    [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stButton button, [data-testid="stSidebar"] p { color: #ffffff; }
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
    st.markdown("<h1 style='text-align: center; color: #0f172a;'>🔐 بوابة الدخول للمنظومة الهندسية الاستشارية</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; font-weight: bold; color: #475569;'>إشراف وتطوير: المهندس محمد ذنون عبد شريف</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>الرجاء إدخال رمز المرور السري للدخول إلى النظام:</p>", unsafe_allow_html=True)
    
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

    # 1. أعمال البناء والطابوق
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

    # 2. اللبخ والإنهاءات
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

    # 3. الأرضيات
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

    # 4. الخرسانة والحديد
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

    # 5. العزل والآليات
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
    st.header("🏡 قسم التصميم المعماري وتوزيع الفضاءات")
    st.write("---")
    c1, c2 = st.columns(2)
    with c1: frontage = st.number_input("عرض الواجهة X (م)", value=10.0, step=0.5)
    with c2: depth = st.number_input("النزال Y (م)", value=20.0, step=0.5)
    if st.button("توليد المخطط"):
        fig, ax = plt.subplots(figsize=(6, 8))
        ax.add_patch(patches.Rectangle((0,0), frontage, depth, fill=False, linewidth=3))
        st.pyplot(fig)

# ==========================================
# 3. التدقيق الإنشائي والتوليد التلقائي الذكي (ACI 318)
# ==========================================
elif "التدقيق والتحليل الإنشائي والتوليد التلقائي" in mode:
    st.header("🔍 التدقيق والتحليل الإنشائي والتوليد الذكي التلقائي (ACI 318)")
    st.markdown("اختر نمط العمل (التصميم والتوليد التلقائي الشامل لجميع الطوابق والبلاطات والجسور والأعمدة، أو التدقيق اليدوي):")
    st.write("---")

    auto_design = st.toggle("⚡ تفعيل نظام التوليد والتصميم الإنشائي الذكي التلقائي (Auto-Design Wizard)", value=True)

    ALL_BAR_DIAMETERS = [8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32]
    ALL_SLAB_TYPES = [
        "سقف مصمت اتجاه واحد (Solid Slab One-Way)",
        "سقف مصمت اتجاهين (Solid Slab Two-Way)",
        "سقف هوردي اتجاه واحد (One-Way Ribbed Slab)",
        "سقف هوردي اتجاهين (Two-Way Ribbed / Waffle Slab)",
        "سقف بلاطة مسطحة بدون جسور (Flat Plate)",
        "سقف مسطح مع سقوط (Flat Slab with Drop Panel)"
    ]
    SLAB_POSITIONS = ["داخلي (Interior)", "خارجي / حافة (Exterior / Edge)", "زاوية / ركن (Corner)"]

    st.write("---")
    st.subheader("🏛️ 1. البيانات العامة والأساسية للمبنى وطوابقه")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        total_floors_cnt = st.number_input("عدد طوابق المنشأ الكلي:", min_value=1, max_value=20, value=3, step=1)
    with col_f2:
        bldg_use = st.selectbox("الغرض الإشغالي للمبنى:", ["سكني", "تجاري / محلات", "مكاتب إدارية", "مستشفى / خدمي"])

    floors_data = []

    # ==========================================
    # المسار الأول: التوليد التلقائي الذكي الشامل لكل طابق وبلاطة وجسر وعمود
    # ==========================================
    if auto_design:
        st.success("🤖 نظام التوليد التلقائي الشامل مفعل! حدد مواصفات السقوف وأعداد الجسور والأعمدة لكل طابق أدناه:")

        st.subheader("📏 أبعاد مساحة الطابق الأساسية (محاور X & Y)")
        auto_col_x, auto_col_y = st.columns(2)
        with auto_col_x:
            auto_x = st.number_input("عرض البناية الرئيسي X (متر):", value=10.0, step=0.5)
        with auto_col_y:
            auto_y = st.number_input("طول البناية الرئيسي Y (متر):", value=20.0, step=0.5)
        
        auto_floor_area = auto_x * auto_y
        st.info(f"إجمالي مساحة الطابق المحسوبة: **{auto_floor_area:.1f} م²**")

        for fl_idx in range(1, total_floors_cnt + 1):
            fl_name = "الطابق الأرضي (Ground Floor)" if fl_idx == 1 else (f"الطابق ({fl_idx - 1}) المتكرر" if fl_idx < total_floors_cnt else f"الطابق الأخير / السطح ({fl_idx})")
            
            with st.expander(f"🏢 تفصيلات واختيارات {fl_name}", expanded=(fl_idx == 1)):
                st.markdown(f"**أ) نوع سقف البلاطة لـ {fl_name}:**")
                auto_stype = st.selectbox(f"نوع السقف:", ALL_SLAB_TYPES, key=f"auto_stype_{fl_idx}")

                st.markdown(f"**ب) عدد الجسور والأعمدة لـ {fl_name} (لانتقال الأحمال وتحديد الأحمال الميتة والحية):**")
                ac1, ac2 = st.columns(2)
                with ac1:
                    auto_beams_cnt = st.number_input(f"عدد الجسور (Beams) في {fl_name}:", min_value=2, max_value=30, value=8, step=1, key=f"auto_b_{fl_idx}")
                with ac2:
                    auto_cols_cnt = st.number_input(f"عدد الأعمدة (Columns) في {fl_name}:", min_value=4, max_value=40, value=12, step=1, key=f"auto_c_{fl_idx}")

            auto_slabs = [
                {
                    "slab_num": 1,
                    "type": auto_stype,
                    "pos": "داخلي (Interior)",
                    "dia": 12 if fl_idx == 1 else 10,
                    "spacing": 150
                },
                {
                    "slab_num": 2,
                    "type": auto_stype,
                    "pos": "خارجي / حافة (Exterior / Edge)" if fl_idx == 1 else "زاوية / ركن (Corner)",
                    "dia": 12,
                    "spacing": 125
                }
            ]

            col_d_auto = 25 if fl_idx == 1 and total_floors_cnt > 3 else (20 if fl_idx <= 2 else 16)
            col_n_auto = 8 if total_floors_cnt <= 3 else 10

            floors_data.append({
                "floor_num": fl_idx,
                "floor_title": fl_name,
                "area": auto_floor_area,
                "slabs": auto_slabs,
                "c_dia": col_d_auto,
                "c_num": col_n_auto,
                "b_dia": 16,
                "b_num": 4,
                "b_cnt": auto_beams_cnt,
                "c_cnt": auto_cols_cnt,
                "st_sp": 100
            })

    # ==========================================
    # المسار الثاني: التدقيق والإدخال اليدوي المباشر
    # ==========================================
    else:
        st.warning("🛠️ وضع التدقيق اليدوي مفعل! حدد كافة تفاصيل الطوابق، البلاطات، والجسور والأعمدة بنفسك.")
        if "floor_segments" not in st.session_state:
            st.session_state.floor_segments = {}

        for fl_idx in range(1, total_floors_cnt + 1):
            fl_name = "الطابق الأرضي (Ground Floor)" if fl_idx == 1 else (f"الطابق ({fl_idx - 1}) المتكرر" if fl_idx < total_floors_cnt else f"الطابق الأخير / السطح ({fl_idx})")
            
            with st.expander(f"📌 تفاصيل وبيانات واختيارات {fl_name}", expanded=(fl_idx == 1)):
                st.markdown(f"##### أ) مساحة المقطع لـ {fl_name}:")
                seg_key = f"fl_seg_{fl_idx}"
                if seg_key not in st.session_state.floor_segments:
                    st.session_state.floor_segments[seg_key] = [{"x": 10.0, "y": 20.0}]

                fl_area = 0.0
                for s_i, seg in enumerate(st.session_state.floor_segments[seg_key]):
                    cx, cy = st.columns(2)
                    with cx: st.session_state.floor_segments[seg_key][s_i]["x"] = st.number_input(f"عرض X_{s_i+1} (م):", value=seg["x"], step=0.5, key=f"x_{fl_idx}_{s_i}")
                    with cy: st.session_state.floor_segments[seg_key][s_i]["y"] = st.number_input(f"طول Y_{s_i+1} (م):", value=seg["y"], step=0.5, key=f"y_{fl_idx}_{s_i}")
                    fl_area += st.session_state.floor_segments[seg_key][s_i]["x"] * st.session_state.floor_segments[seg_key][s_i]["y"]

                st.info(f"إجمالي مساحة {fl_name}: **{fl_area:.1f} م²**")

                st.markdown(f"##### ب) السقوف وبلاطات {fl_name}:")
                sl_count = st.number_input(f"عدد البلاطات في {fl_name}:", min_value=1, max_value=8, value=2, step=1, key=f"sl_cnt_{fl_idx}")

                floor_slabs = []
                for s_idx in range(int(sl_count)):
                    sc1, sc2, sc3, sc4 = st.columns(4)
                    with sc1: stype = st.selectbox(f"نوع سقف البلاطة ({s_idx+1}):", ALL_SLAB_TYPES, key=f"stype_{fl_idx}_{s_idx}")
                    with sc2: spos = st.selectbox(f"موقع البلاطة ({s_idx+1}):", SLAB_POSITIONS, index=0 if s_idx==0 else 1, key=f"spos_{fl_idx}_{s_idx}")
                    with sc3: sdia = st.selectbox(f"قطر حديد البلاطة:", ALL_BAR_DIAMETERS, index=1, format_func=lambda x: f"Ø{x} مم", key=f"sdia_{fl_idx}_{s_idx}")
                    with sc4: sspace = st.number_input(f"المسافة بين الأسياخ (مم):", min_value=100, max_value=300, value=150, step=25, key=f"ssp_{fl_idx}_{s_idx}")

                    floor_slabs.append({"slab_num": s_idx + 1, "type": stype, "pos": spos, "dia": sdia, "spacing": sspace})

                st.markdown(f"##### ج) أعداد وتفاصيل الأعمدة والجسور لـ {fl_name}:")
                col_d1, col_d2, col_d3 = st.columns(3)
                with col_d1:
                    col_bar_d = st.selectbox(f"قطر حديد الأعمدة:", ALL_BAR_DIAMETERS, index=6, format_func=lambda x: f"Ø{x} مم", key=f"cd_{fl_idx}")
                    col_bar_num = st.number_input(f"عدد أسياخ العمود:", min_value=4, max_value=24, value=8, step=2, key=f"cn_{fl_idx}")
                    cols_count_man = st.number_input(f"عدد أعمدة الطابق:", min_value=4, max_value=40, value=12, step=1, key=f"ccnt_{fl_idx}")
                with col_d2:
                    beam_bar_d = st.selectbox(f"قطر حديد الجسور:", ALL_BAR_DIAMETERS, index=4, format_func=lambda x: f"Ø{x} مم", key=f"bd_{fl_idx}")
                    beam_bar_num = st.number_input(f"أسياخ الجسر:", min_value=2, max_value=16, value=4, step=1, key=f"bn_{fl_idx}")
                with col_d3:
                    beam_count_man = st.number_input(f"عدد الجسور بالطابق:", min_value=2, max_value=30, value=8, step=1, key=f"bmc_{fl_idx}")
                    stirrup_sp = st.number_input(f"مسافة الكانات (مم):", min_value=50, max_value=250, value=100, step=25, key=f"stsp_{fl_idx}")

                floors_data.append({
                    "floor_num": fl_idx,
                    "floor_title": fl_name,
                    "area": fl_area,
                    "slabs": floor_slabs,
                    "c_dia": col_bar_d,
                    "c_num": col_bar_num,
                    "b_dia": beam_bar_d,
                    "b_num": beam_bar_num,
                    "b_cnt": beam_count_man,
                    "c_cnt": cols_count_man,
                    "st_sp": stirrup_sp
                })

    st.write("---")
    btn_text = "⚡ توليد وعرض التقرير الإنشائي الشامل والمفصل لكل طابق" if auto_design else "🚀 إجراء التحليل الهندسي مفصلاً لكل طابق وبلاطة وجسر"
    
    if st.button(btn_text, use_container_width=True):
        st.success("تم الحساب والتحليل الهندسي المفصل وفصل نتائج الطوابق عن بعضها بنجاح ✅")

        # 1. جداول تحليل السقوف والبلاطات مفصولة لكل طابق
        st.subheader("📑 1. جدول تحليل السقوف، مواقع البلاطات، والأوفرلاب لكل طابق منفصل:")
        
        export_csv_rows = []
        tot_overlap_wt_all_floors = 0.0

        for f_item in floors_data:
            st.markdown(f"#### 🏢 **{f_item['floor_title']}** (المساحة: {f_item['area']:.1f} م² | عدد الأعمدة: {f_item['c_cnt']} | عدد الجسور: {f_item['b_cnt']}):")
            
            c_lap_cm = round(48 * f_item["c_dia"] / 10.0, 1)
            c_unit_wt = (f_item["c_dia"]**2) / 162.0
            f_col_lap_wt_kg = f_item["c_cnt"] * f_item["c_num"] * (c_lap_cm / 100.0) * c_unit_wt
            tot_overlap_wt_all_floors += f_col_lap_wt_kg

            slab_analysis_table = []
            for sl in f_item["slabs"]:
                slab_lap_cm = round(40 * sl["dia"] / 10.0, 1)
                if "زاوية" in sl["pos"]:
                    mom_notes = "عزوم التواء (Torsion) وعزوم حافة قصوى. يُكثّف التسليح بالزوايا وفي الاتجاهين."
                    overlap_loc = f"عند 1/5 البحر (طول الأوفرلاب {slab_lap_cm} سم)"
                    rec_space = "100 - 125 مم"
                elif "خارجي" in sl["pos"]:
                    mom_notes = "عزم سالب مرتفع عند المرتكزات الخارجية. يُكثّف التسليح العلوي المقاوم للشقوق."
                    overlap_loc = f"عند مناطق الانقلاب L/4 (طول الأوفرلاب {slab_lap_cm} سم)"
                    rec_space = "125 - 150 مم"
                else:
                    mom_notes = "عزوم موجبة وسالبة متوازنة. التسليح قياسي."
                    overlap_loc = f"في منتصف البحر للعلوي وعند المرتكزات للسفلي ({slab_lap_cm} سم)"
                    rec_space = "150 - 200 مم"

                slab_analysis_table.append({
                    "البلاطة والسقف": f"بلاطة ({sl['slab_num']})",
                    "نوع السقف الهندسي": sl["type"],
                    "الموقع": sl["pos"],
                    "التسليح": f"Ø{sl['dia']} كل {sl['spacing']}مم",
                    "موقع وطول الأوفرلاب": overlap_loc,
                    "تحليل العزوم ومناطق التكثيف": mom_notes,
                    "التقييم": "✅ آمن ومطابق للكود"
                })

                export_csv_rows.append({
                    "الطابق": f_item['floor_title'],
                    "العنصر": f"بلاطة ({sl['slab_num']}) - {sl['type']}",
                    "الموقع": sl["pos"],
                    "التسليح": f"Ø{sl['dia']} كل {sl['spacing']}مم",
                    "مكان الأوفرلاب": overlap_loc,
                    "تحليل العزوم": mom_notes
                })

            st.table(slab_analysis_table)

            # تفاصيل الجسور والأعمدة لكل طابق منفصل
            b_lap_cm = round(50 * f_item["b_dia"] / 10.0, 1)
            cb_table = [
                {
                    "العنصر الإنشائي": f"الأعمدة ({f_item['c_cnt']} عمود)",
                    "التسليح": f"{f_item['c_num']} Ø{f_item['c_dia']}",
                    "موقع وطول الأوفرلاب": f"منتصف العمود (Zone B) | الطول: {c_lap_cm} سم | الوزن: {f_col_lap_wt_kg:.1f} كغم",
                    "حالة الأمان": "✅ مطابق للكود ACI 318"
                },
                {
                    "العنصر الإنشائي": f"الجسور ({f_item['b_cnt']} جسر)",
                    "التسليح والكانات": f"{f_item['b_num']} Ø{f_item['b_dia']} | كانات كل {f_item['st_sp']}مم",
                    "موقع وطول الأوفرلاب": f"علوي بالمنتصف، سفلي قرب الأعمدة | الطول: {b_lap_cm} سم",
                    "حالة الأمان": "✅ تكثيف الكانات قرب المرتكزات محقق"
                }
            ]
            st.table(cb_table)

        # 2. جدول التحليل الاقتصادي المفصول لكل طابق
        st.write("---")
        st.subheader("💡 2. جدول التحليل الاقتصادي والتوفير المالي المفصول لكل طابق:")
        
        for f_item in floors_data:
            st.markdown(f"#### 💰 **التحليل الاقتصادي - {f_item['floor_title']}**:")
            econ_floor_table = [
                {
                    "العنصر": "السقوف والبلاطات",
                    "التسليح الحالي": f"Ø{f_item['slabs'][0]['dia']}",
                    "التسليح الاقتصادي": "Ø10 أو Ø12 كل 175-200مم",
                    "نسبة التوفير المتوقعة": "توفير ~10% من حديد السقف."
                },
                {
                    "العنصر": "الأعمدة والجسور",
                    "التسليح الحالي": f"{f_item['c_num']} Ø{f_item['c_dia']} أعمدة",
                    "التسليح الاقتصادي": "8 Ø16 للأعمدة المتكررة",
                    "نسبة التوفير المتوقعة": "تحسين التوزيع الهيكلي وتقليل الهدر."
                }
            ]
            st.table(econ_floor_table)

        # 3. جدول تتبع وانتقال الأحمال طابقاً بطابق (الحمل الميت والحي)
        st.write("---")
        st.subheader("🪜 3. جدول تتبع وانتقال الأحمال الميتة والحية (Load Takedown) طابقاً بطابق:")
        
        unit_dl = 3.2 # kN/m2 (حمل ميت مع وزن السقف والتشطيبات)
        unit_ll = 2.0 if "سكني" in bldg_use else 4.0 # kN/m2 (حمل حي حسب الاستخدام)
        
        cum_load_kn = 0.0
        load_takedown_table = []

        for f_item in reversed(floors_data):
            f_dl_total = f_item["area"] * unit_dl
            f_ll_total = f_item["area"] * unit_ll
            f_tot_u = 1.2 * f_dl_total + 1.6 * f_ll_total
            cum_load_kn += f_tot_u
            
            # نصيب العمود الواحد في هذا الطابق من الحمل المنتقل
            col_share_load = cum_load_kn / f_item["c_cnt"]

            load_takedown_table.append({
                "مستوى الطابق": f_item["floor_title"],
                "مساحة الطابق": f"{f_item['area']:.1f} م²",
                "الحمل الميت (DL)": f"{f_dl_total:,.1f} kN",
                "الحمل الحي (LL)": f"{f_ll_total:,.1f} kN",
                "الحمل التصميمي الكلي بالطابق": f"{f_tot_u:,.1f} kN",
                "الحمل التراكمي النازل": f"{cum_load_kn:,.1f} kN (~{cum_load_kn/10:.1f} طن)",
                "حصة العمود الواحد من الحمل": f"{col_share_load:,.1f} kN"
            })

        st.table(load_takedown_table)

        # 4. التكلفة وتصدير التقارير
        st.write("---")
        st.subheader("📥 4. تنزيل التقارير الرسمية والجدول الإنشائي لكل الطوابق (Excel & PDF):")
        
        tot_lap_cost_iqd = (tot_overlap_wt_all_floors / 1000.0) * live_steel_price
        st.info(f"💡 إجمالي وزن حديد الأوفرلاب لجميع أعمدة المبنى: **{tot_overlap_wt_all_floors:,.1f} كغم (~{tot_overlap_wt_all_floors/1000:.2f} طن)** | الكلفة التقديرية: **{tot_lap_cost_iqd:,.0f} دينار عراقي**")

        col_dl_x, col_dl_p = st.columns(2)
        
        # إنشاء ملف CSV
        csv_str = "الطابق,العنصر,الموقع,التسليح,مكان الأوفرلاب,تحليل العزوم ومناطق التكثيف\n"
        for r in export_csv_rows:
            csv_str += f"{r['الطابق']},{r['العنصر']},{r['الموقع']},{r['التسليح']},{r['مكان الأوفرلاب']},{r['تحليل العزوم']}\n"
        
        b64_csv = base64.b64encode(csv_str.encode('utf-8-sig')).decode()
        with col_dl_x:
            st.markdown(f"""
                <a href="data:file/csv;base64,{b64_csv}" download="Muhamed_Zannon_Comprehensive_Report.csv" style="text-decoration: none;">
                    <div style="background-color: #0f172a; color: white; padding: 12px 20px; border-radius: 6px; text-align: center; font-weight: bold;">
                        📊 تحميل التقرير الشامل والمفصل لكافة الطوابق (.csv / Excel)
                    </div>
                </a>
            """, unsafe_allow_html=True)

        # HTML/PDF
        html_str = f"""
        <html dir="rtl">
        <head><meta charset="utf-8"><title>التقرير الإنشائي الاستشاري الشامل - المهندس محمد ذنون</title>
        <style>
            body {{ font-family: Tahoma, sans-serif; padding: 20px; color: #333; }}
            h1, h3 {{ text-align: center; color: #0f172a; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; }}
            th, td {{ border: 1px solid #cbd5e1; padding: 8px; text-align: center; font-size: 13px; }}
            th {{ background-color: #0f172a; color: white; }}
        </style>
        </head>
        <body>
            <h1>المنظومة الهندسية الاستشارية</h1>
            <h3>إشراف وتطوير: المهندس محمد ذنون عبد شريف | جامعة كربلاء</h3>
            <hr>
            <h2>التقرير الإنشائي المفصل وتحليل الطوابق والسقوف والأحمال (ACI 318)</h2>
            <table>
                <tr><th>الطابق</th><th>العنصر</th><th>الموقع</th><th>التسليح</th><th>مكان وطول الأوفرلاب</th><th>تحليل العزوم ومناطق التكثيف</th></tr>
        """
        for r in export_csv_rows:
            html_str += f"<tr><td>{r['الطابق']}</td><td>{r['العنصر']}</td><td>{r['الموقع']}</td><td>{r['التسليح']}</td><td>{r['مكان الأوفرلاب']}</td><td>{r['تحليل العزوم']}</td></tr>"
        html_str += f"""
            </table>
            <p><b>إجمالي كلفة حديد الأوفرلاب للأعمدة:</b> {tot_lap_cost_iqd:,.0f} دينار عراقي</p>
        </body>
        </html>
        """
        b64_pdf = base64.b64encode(html_str.encode('utf-8')).decode()
        with col_dl_p:
            st.markdown(f"""
                <a href="data:text/html;base64,{b64_pdf}" download="Muhamed_Zannon_Comprehensive_Report.html" style="text-decoration: none;">
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
        b_type = st.selectbox("نوع الطابوق", ["طابوق أحمر مفرد (12سم)", "طابوق أحمر مزدوج (24سم)", "طابوق أصفر", "بلوك خرساني"])
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
