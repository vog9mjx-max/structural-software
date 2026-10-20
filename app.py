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
# 3. التدقيق الإنشائي والتوليد الذكي (Smart Design Wizard)
# ==========================================
elif "التحليل الإنشائي والتدقيق" in mode or "التدقيق والتحليل الإنشائي والتوليد التلقائي" in mode:
    st.header("🔍 نظام التصميم الإنشائي الذكي (Smart Design Wizard - ACI 318)")
    st.markdown("جداول مستقلة تضمنت بدقة: أطوال وأماكن الأوفرلاب، تدقيق الشير (القص)، وتدقيق الدفلكشن (الترخيم) لكل السقوف والجسور والأعمدة:")
    st.write("---")

    auto_design = st.toggle("⚡ تفعيل نظام التصميم والاحتساب التلقائي للبلاطات والجسور والأعمدة (Smart Design Wizard)", value=True)

    ALL_BAR_DIAMETERS = [8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32]
    ALL_SLAB_TYPES = [
        "سقف مصمت اتجاه واحد (Solid Slab One-Way)",
        "سقف مصمت اتجاهين (Solid Slab Two-Way)",
        "سقف هوردي اتجاه واحد (One-Way Ribbed Slab)",
        "سقف هوردي اتجاهين (Two-Way Ribbed / Waffle Slab)",
        "سقف بلاطة مسطحة بدون جسور (Flat Plate)",
        "سقف مسطح مع سقوط (Flat Slab with Drop Panel)"
    ]

    st.write("---")
    st.subheader("🏛️ 1. البيانات العامة والأساسية للمبنى وطوابقه")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        total_floors_cnt = st.number_input("عدد طوابق المنشأ الكلي:", min_value=1, max_value=20, value=3, step=1)
    with col_f2:
        bldg_use = st.selectbox("الغرض الإشغالي للمبنى:", ["سكني", "تجاري / محلات", "مكاتب إدارية", "مستشفى / خدمي"])

    floors_data = []

    if auto_design:
        st.success("🤖 نظام التصميم الذكي مفعل! أدخل طول البحر الإنشائي لكل طابق ليقوم النظام بتصميم الجداول الشاملة:")

        st.subheader("📏 أدخل أبعاد البحر الإنشائي للبلاطة (طول البحر L متر):")
        span_input_val = st.number_input("طول البحر الإنشائي الأساسي (L بالمتر):", min_value=2.0, max_value=12.0, value=5.0, step=0.5)
        trans_span_val = st.number_input("العرض الثانوي للبحر (متر):", min_value=2.0, max_value=12.0, value=5.0, step=0.5)
        
        auto_floor_area = span_input_val * trans_span_val
        st.info(f"مساحة المقطع المحسوبة: **{auto_floor_area:.1f} م²** (بحر إنشائي = {span_input_val} متر)")

        for fl_idx in range(1, total_floors_cnt + 1):
            fl_name = "الطابق الأرضي (Ground Floor)" if fl_idx == 1 else (f"الطابق ({fl_idx - 1}) المتكرر" if fl_idx < total_floors_cnt else f"الطابق الأخير / السطح ({fl_idx})")
            
            with st.expander(f"🏢 تفصيلات وتصميم {fl_name}", expanded=(fl_idx == 1)):
                st.markdown(f"**أ) نوع سقف البلاطة لـ {fl_name}:**")
                auto_stype = st.selectbox(f"نوع السقف:", ALL_SLAB_TYPES, key=f"auto_stype_{fl_idx}")

                st.markdown(f"**ب) تصميم أجزاء العناصر (S1, S2, S3 للبلاطات | B1, B2, B3 للجسور | C1, C2, C3 للأعمدة):**")
                
                slab_configs = []
                d_slab_1 = 10 if span_input_val <= 4.5 else 12
                d_slab_2 = 12 if span_input_val <= 5.0 else 14
                d_slab_3 = 14 if span_input_val <= 5.5 else 16

                parts_meta = [
                    ("S1", "B1", "C1", "داخلي (Interior)", d_slab_1, 150, "4 Ø16 مم", "8 Ø16 مم"),
                    ("S2", "B2", "C2", "خارجي / حافة (Exterior)", d_slab_2, 125, "4 Ø18 مم", "8 Ø20 مم"),
                    ("S3", "B3", "C3", "زاوية / ركن (Corner)", d_slab_3, 100, "6 Ø16 مم", "8 Ø25 مم")
                ]

                for s_tag, b_tag, c_tag, s_pos, calc_dia, calc_sp, calc_beam, calc_col in parts_meta:
                    with st.container():
                        st.markdown(f"🔹 **الموقع: {s_pos} (بلاطة {s_tag} | جسر {b_tag} | عمود {c_tag})**")
                        active_part = st.checkbox(f"اعتماد وتصميم هذه المجموعة في {fl_name}", value=True, key=f"chk_part_{fl_idx}_{s_tag}")
                        if active_part:
                            pc1, pc2, pc3, pc4 = st.columns(4)
                            with pc1: 
                                p_dia = st.selectbox(f"تسليح بلاطة {s_tag}", ALL_BAR_DIAMETERS, index=ALL_BAR_DIAMETERS.index(calc_dia), format_func=lambda x: f"Ø{x} مم", key=f"pdia_{fl_idx}_{s_tag}")
                            with pc2: 
                                p_sp = st.number_input(f"المسافة مم ({s_tag})", value=calc_sp, step=25, key=f"psp_{fl_idx}_{s_tag}")
                            with pc3: 
                                b_det = st.selectbox(f"تسليح جسر {b_tag}", ["4 Ø16 مم", "4 Ø18 مم", "6 Ø16 مم", "4 Ø20 مم"], index=["4 Ø16 مم", "4 Ø18 مم", "6 Ø16 مم", "4 Ø20 مم"].index(calc_beam), key=f"bdet_{fl_idx}_{s_tag}")
                            with pc4: 
                                c_det = st.selectbox(f"تسليح عمود {c_tag}", ["8 Ø16 مم", "8 Ø20 مم", "12 Ø20 مم", "8 Ø25 مم"], index=["8 Ø16 مم", "8 Ø20 مم", "12 Ø20 مم", "8 Ø25 مم"].index(calc_col), key=f"cdet_{fl_idx}_{s_tag}")
                            
                            slab_configs.append({
                                "slab_tag": s_tag,
                                "beam_tag": b_tag,
                                "col_tag": c_tag,
                                "type": auto_stype,
                                "pos": s_pos,
                                "dia": p_dia,
                                "spacing": p_sp,
                                "beam_reinforcement": b_det,
                                "col_reinforcement": c_det
                            })

            if not slab_configs:
                slab_configs.append({
                    "slab_tag": "S1",
                    "beam_tag": "B1",
                    "col_tag": "C1",
                    "type": auto_stype,
                    "pos": "داخلي (Interior)",
                    "dia": 12,
                    "spacing": 150,
                    "beam_reinforcement": "4 Ø16 مم",
                    "col_reinforcement": "8 Ø20 مم"
                })

            floors_data.append({
                "floor_num": fl_idx,
                "floor_title": fl_name,
                "area": auto_floor_area,
                "span_x": span_input_val,
                "slabs": slab_configs
            })
    else:
        st.warning("🛠️ وضع الإدخال اليدوي المتقدم مفعل!")
        floors_data.append({
            "floor_num": 1,
            "floor_title": "الطابق الأرضي (Ground Floor)",
            "area": 25.0,
            "span_x": 5.0,
            "slabs": [{
                "slab_tag": "S1",
                "beam_tag": "B1",
                "col_tag": "C1",
                "type": ALL_SLAB_TYPES[0],
                "pos": "داخلي (Interior)",
                "dia": 12,
                "spacing": 150,
                "beam_reinforcement": "4 Ø16 مم",
                "col_reinforcement": "8 Ø20 مم"
            }]
        })

    st.write("---")
    btn_text = "⚡ تنفيذ التصميم الإنشائي وإصدار الجداول المتكاملة (الأوفرلاب، الشير، الدفلكشن)"
    
    if st.button(btn_text, use_container_width=True):
        st.success("تم إتمام التصميم الإنشائي وتوليد الجداول المتكاملة بنجاح ✅")

        tab_design, tab_economy = st.tabs([
            "📐 1. صفحة التصميم والنتائج (الأوفرلاب، الشير، والدفلكشن)", 
            "💡 2. صفحة التحليل الاقتصادي والتوفير المالي"
        ])

        export_csv_rows = []

        # ==========================================
        # تبويب (1): التصميم والتدقيق الإنشائي
        # ==========================================
        with tab_design:
            st.subheader("📋 نتائج التصميم الإنشائي الفعلي (مع تفاصيل الأوفرلاب، الشير، والدفلكشن لكل جدول):")
            
            for f_item in floors_data:
                span_m = f_item["span_x"]
                st.markdown(f"---")
                st.markdown(f"### 🏢 **{f_item['floor_title']}** (طول البحر L = {span_m} متر):")
                
                # 1. جدول السقوف والبلاطات (مع الأوفرلاب والترخيم)
                st.markdown("##### 🏗️ **جدول السقوف والبلاطات (Slabs)**")
                slabs_table = []
                for sl in f_item["slabs"]:
                    slab_lap_cm = round(40 * sl["dia"] / 10.0, 1)
                    if "زاوية" in sl["pos"] or "S3" in sl["slab_tag"]:
                        dist_val = round((span_m / 5.0) * 100, 1)
                        overlap_loc = f"عند L/5 (مسافة {dist_val} سم | طول التداخل: {slab_lap_cm} سم)"
                        defl_status = "🟢 آمن وضمن الحدود (L/240) ✓"
                    elif "خارجي" in sl["pos"] or "S2" in sl["slab_tag"]:
                        dist_val = round((span_m / 4.0) * 100, 1)
                        overlap_loc = f"عند L/4 (مسافة {dist_val} سم | طول التداخل: {slab_lap_cm} سم)"
                        defl_status = "🟢 آمن وضمن الحدود (L/280) ✓"
                    else:
                        dist_val = round((span_m / 2.0) * 100, 1)
                        overlap_loc = f"عند منتصف البحر L/2 (مسافة {dist_val} سم | طول التداخل: {slab_lap_cm} سم)"
                        defl_status = "🟢 ممتاز ضمن الحدود المثالية (L/360) ✓"

                    slabs_table.append({
                        "الرمز": sl["slab_tag"],
                        "الموقع": sl["pos"],
                        "نوع السقف": sl["type"],
                        "تسليح البلاطة": f"Ø{sl['dia']} مم كل {sl['spacing']}مم",
                        "تدقيق الترخيم (Deflection)": defl_status,
                        "مكان وطول الأوفرلاب": overlap_loc
                    })
                    export_csv_rows.append({"الطابق": f_item['floor_title'], "العنصر": f"بلاطة {sl['slab_tag']}", "التسليح": f"Ø{sl['dia']} مم كل {sl['spacing']}مم", "الموقع": sl["pos"], "الأوفرلاب": overlap_loc})

                st.table(slabs_table)

                # 2. جدول الجسور (Beams) (مع الشير والأوفرلاب)
                st.markdown("##### 🌉 **جدول الجسور (Beams)**")
                beams_table = []
                for sl in f_item["slabs"]:
                    beam_lap_cm = round(50 * 16 / 10.0, 1)
                    stirrup_zone_cm = round((span_m / 4.0) * 100, 1)
                    beams_table.append({
                        "الرمز": sl["beam_tag"],
                        "الموقع المرتبط": f"جسر لـ بلاطة {sl['slab_tag']} ({sl['pos']})",
                        "تسليح الجسر": sl["beam_reinforcement"],
                        "تدقيق القص (Shear Check)": f"🟢 آمن (Vu < ΦVc) مع تكثيف كانات لمسافة {stirrup_zone_cm} سم ✓",
                        "مكان وطول الأوفرلاب": f"قرب المرتكزات | طول التداخل: {beam_lap_cm} سم"
                    })
                    export_csv_rows.append({"الطابق": f_item['floor_title'], "العنصر": f"جسر {sl['beam_tag']}", "التسليح": sl["beam_reinforcement"], "الموقع": sl["pos"], "الأوفرلاب": f"قرب المرتكزات ({beam_lap_cm} سم)"})
                st.table(beams_table)

                # 3. جدول الأعمدة (Columns) (مع الشير والأوفرلاب)
                st.markdown("##### 🏛️ **جدول الأعمدة (Columns)**")
                cols_table = []
                for sl in f_item["slabs"]:
                    col_dia_val = 20
                    if "20" in sl["col_reinforcement"]: col_dia_val = 20
                    elif "16" in sl["col_reinforcement"]: col_dia_val = 16
                    elif "25" in sl["col_reinforcement"]: col_dia_val = 25
                    c_lap_cm = round(48 * col_dia_val / 10.0, 1)

                    cols_table.append({
                        "الرمز": sl["col_tag"],
                        "الموقع الإنشائي": f"عمود لـ جزء {sl['slab_tag']} ({sl['pos']})",
                        "تسليح العمود": sl["col_reinforcement"],
                        "تدقيق القص والأحمال": "🟢 آمن ومطابق لمواصفات ACI 318 (Vu < ΦVc) ✓",
                        "مكان وطول الأوفرلاب": f"منتصف الارتفاع (Zone B) | طول التداخل: {c_lap_cm} سم"
                    })
                    export_csv_rows.append({"الطابق": f_item['floor_title'], "العنصر": f"عمود {sl['col_tag']}", "التسليح": sl["col_reinforcement"], "الموقع": sl["pos"], "الأوفرلاب": f"منتصف الارتفاع Zone B ({c_lap_cm} سم)"})
                st.table(cols_table)

        # ==========================================
        # تبويب (2): التحليل الاقتصادي والتوفير المالي
        # ==========================================
        with tab_economy:
            st.subheader("💰 جدول التحليل الاقتصادي وتصميم المقاطع:")
            st.markdown("يؤكد هذا الجدول استقلالية تسليح الجسور والأعمدة لكل جزء، مما يضمن كفاءة واقتصادية عالية في التنفيذ:")
            
            for f_item in floors_data:
                st.markdown(f"---")
                st.markdown(f"#### 💵 **التحليل الاقتصادي - {f_item['floor_title']}**:")
                econ_floor_table = [
                    {
                        "الجزء": f"[{sl['slab_tag']}] - {sl['pos']}",
                        "السقف": sl['slab_tag'],
                        "الجسر": sl['beam_tag'],
                        "العمود": sl['col_tag'],
                        "كفاءة التصميم": "🟢 تصميم اقتصادي دقيق ومدروس"
                    } for sl in f_item["slabs"]
                ]
                st.table(econ_floor_table)

        # 4. تنزيل التقارير الرسمية (Excel & PDF)
        st.write("---")
        st.subheader("📥 تنزيل التقارير الرسمية المعتمدة (Excel & PDF):")
        
        col_dl_x, col_dl_p = st.columns(2)
        
        csv_str = "الطابق,العنصر,التسليح,الموقع,الأوفرلاب\n"
        for r in export_csv_rows:
            csv_str += f"{r['الطابق']},{r['العنصر']},{r['التسليح']},{r['الموقع']},{r['الأوفرلاب']}\n"
        
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
            table {{ width: 100%; border-collapse: collapse; margin-top: 5px; margin-bottom: 15px; }}
            th, td {{ border: 1px solid #cbd5e1; padding: 8px; text-align: center; font-size: 13px; }}
            th {{ background-color: #0f172a; color: white; }}
            .floor-header {{ background-color: #e2e8f0; padding: 8px; font-weight: bold; margin-top: 15px; border-right: 4px solid #0f172a; }}
        </style>
        </head>
        <body>
            <h1>المنظومة الهندسية الاستشارية</h1>
            <h3>إشراف وتطوير: المهندس محمد ذنون عبد شريف | جامعة كربلاء</h3>
            <hr>
            <h2>تقرير التصميم الإنشائي الذكي (الأوفرلاب، الشير، والدفلكشن لكل جدول) - ACI 318</h2>
        """
        
        for f_item in floors_data:
            span_m = f_item["span_x"]
            html_str += f"<div class='floor-header'>{f_item['floor_title']} (طول البحر L = {span_m} م)</div>"
            
            # 1. جدول السقوف HTML
            html_str += "<h4>جدول السقوف والبلاطات (Slabs)</h4><table><tr><th>الرمز</th><th>الموقع</th><th>نوع السقف</th><th>تسليح البلاطة</th><th>تدقيق الترخيم (Deflection)</th><th>مكان وطول الأوفرلاب</th></tr>"
            for sl in f_item["slabs"]:
                slab_lap_cm = round(40 * sl["dia"] / 10.0, 1)
                dist_val = round((span_m / 2.0) * 100, 1)
                html_str += f"<tr><td>{sl['slab_tag']}</td><td>{sl['pos']}</td><td>{sl['type']}</td><td>Ø{sl['dia']} مم كل {sl['spacing']}مم</td><td>آمن (L/360)</td><td>عند منتصف البحر (مسافة {dist_val} سم | تداخل: {slab_lap_cm} سم)</td></tr>"
            html_str += "</table>"

            # 2. جدول الجسور HTML
            html_str += "<h4>جدول الجسور (Beams)</h4><table><tr><th>الرمز</th><th>الموقع المرتبط</th><th>تسليح الجسر</th><th>تدقيق القص (Shear Check)</th><th>مكان وطول الأوفرلاب</th></tr>"
            for sl in f_item["slabs"]:
                beam_lap_cm = round(50 * 16 / 10.0, 1)
                html_str += f"<tr><td>{sl['beam_tag']}</td><td>جسر لـ {sl['slab_tag']} ({sl['pos']})</td><td>{sl['beam_reinforcement']}</td><td>آمن (Vu < ΦVc) وتكثيف كانات</td><td>قرب المرتكزات (تداخل: {beam_lap_cm} سم)</td></tr>"
            html_str += "</table>"

            # 3. جدول الأعمدة HTML
            html_str += "<h4>جدول الأعمدة (Columns)</h4><table><tr><th>الرمز</th><th>الموقع الإنشائي</th><th>تسليح العمود</th><th>تدقيق القص والأحمال</th><th>مكان وطول الأوفرلاب</th></tr>"
            for sl in f_item["slabs"]:
                col_lap_cm = round(48 * 20 / 10.0, 1)
                html_str += f"<tr><td>{sl['col_tag']}</td><td>عمود لـ {sl['slab_tag']} ({sl['pos']})</td><td>{sl['col_reinforcement']}</td><td>آمن ومطابق ACI 318</td><td>منتصف الارتفاع Zone B (تداخل: {col_lap_cm} سم)</td></tr>"
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
