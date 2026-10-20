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
        "🔍 التدقيق الإنشائي والمساحات المقطعة طابقاً بطابق (ACI 318)",
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
# 3. التدقيق الإنشائي والمساحات المقطعة طابقاً بطابق (ACI 318)
# ==========================================
elif "التدقيق الإنشائي والمساحات المقطعة طابقاً بطابق" in mode:
    st.header("🔍 التدقيق الإنشائي، نظام المساحات المقطعة (X & Y)، والأوفرلاب طابقاً بطابق")
    st.markdown("حساب مساحات الطابق الأرضي والطوابق العليا بواسطة مقاطع متعددة ($X_1 \\times Y_1, X_2 \\times Y_2, ...$) مع حساب انتقال الأحمال والأوفرلاب:")
    st.write("---")
    
    # إدارة المساحات المقطعة للطابق الأرضي والطوابق العليا
    if "gf_segments" not in st.session_state:
        st.session_state.gf_segments = [{"x": 10.0, "y": 20.0}] # مقطع أساسي أول
    if "tf_segments" not in st.session_state:
        st.session_state.tf_segments = [{"x": 10.0, "y": 20.0}] # مقطع أساسي أول

    # 1. المساحات المقطعة للطابق الأرضي
    st.subheader("🏛️ 1. تقطيع مساحات الطابق الأرضي (Ground Floor Segments)")
    st.markdown("أضف المقاطع المستطيلة المكونة لقطعة الطابق الأرضي:")

    gf_total_area = 0.0
    for idx, seg in enumerate(st.session_state.gf_segments):
        c_x, c_y = st.columns(2)
        with c_x:
            st.session_state.gf_segments[idx]["x"] = st.number_input(f"عرض المقطع X_{idx+1} (متر):", value=seg["x"], step=0.5, key=f"gf_x_{idx}")
        with c_y:
            st.session_state.gf_segments[idx]["y"] = st.number_input(f"طول المقطع Y_{idx+1} (متر):", value=seg["y"], step=0.5, key=f"gf_y_{idx}")
        
        seg_a = st.session_state.gf_segments[idx]["x"] * st.session_state.gf_segments[idx]["y"]
        gf_total_area += seg_a
        st.caption(f"مساحة المقطع ({idx+1}): {seg_a:.1f} م²")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("➕ إضافة مقطع مساحة جديد للطابق الأرضي (X_n × Y_n)", key="btn_add_gf"):
            st.session_state.gf_segments.append({"x": 4.0, "y": 5.0})
            st.rerun()
    with col_btn2:
        if len(st.session_state.gf_segments) > 1:
            if st.button("🗑️ حذف آخر مقطع إضافي", key="btn_del_gf"):
                st.session_state.gf_segments.pop()
                st.rerun()

    st.success(f"إجمالي مساحة الطابق الأرضي الصافية: **{gf_total_area:.1f} م²**")

    st.write("---")
    # 2. المساحات المقطعة للطوابق المتكررة
    st.subheader("🏢 2. تقطيع مساحات الطوابق المتكررة (Upper Typical Floors Segments)")
    st.markdown("أضف مقاطع المساحات للطوابق العليا (مع حساب البروزات والبالكونات):")

    tf_total_area = 0.0
    for idx, seg in enumerate(st.session_state.tf_segments):
        c_tx, c_ty = st.columns(2)
        with c_tx:
            st.session_state.tf_segments[idx]["x"] = st.number_input(f"عرض المقطع المتكرر X_{idx+1} (متر):", value=seg["x"], step=0.5, key=f"tf_x_{idx}")
        with c_ty:
            st.session_state.tf_segments[idx]["y"] = st.number_input(f"طول المقطع المتكرر Y_{idx+1} (متر):", value=seg["y"], step=0.5, key=f"tf_y_{idx}")
        
        seg_ta = st.session_state.tf_segments[idx]["x"] * st.session_state.tf_segments[idx]["y"]
        tf_total_area += seg_ta
        st.caption(f"مساحة المقطع المتكرر ({idx+1}): {seg_ta:.1f} م²")

    col_tbtn1, col_tbtn2 = st.columns(2)
    with col_tbtn1:
        if st.button("➕ إضافة مقطع مساحة جديد للطوابق المتكررة", key="btn_add_tf"):
            st.session_state.tf_segments.append({"x": 2.0, "y": 5.0})
            st.rerun()
    with col_tbtn2:
        if len(st.session_state.tf_segments) > 1:
            if st.button("🗑️ حذف آخر مقطع متكرر", key="btn_del_tf"):
                st.session_state.tf_segments.pop()
                st.rerun()

    st.info(f"إجمالي مساحة الطابق المتكرر الصافية: **{tf_total_area:.1f} م²**")

    st.write("---")
    # 3. إعدادات التسليح والأوفرلاب للبناية
    st.subheader("🔩 3. أقطار التسليح وحساب الأوفرلاب الكلي لجميع الطوابق")
    
    col_st1, col_st2, col_st3 = st.columns(3)
    with col_st1:
        total_floors_cnt = st.number_input("عدد الطوابق الإجمالي:", min_value=1, max_value=10, value=3, step=1)
        col_count = st.number_input("عدد الأعمدة في الطابق:", min_value=4, max_value=40, value=12, step=1)
    with col_st2:
        c_dia = st.selectbox("قطر حديد الأعمدة الرئيسي:", [16, 20, 25, 32], format_func=lambda x: f"Ø{x} مم", index=1)
        c_bars = st.number_input("عدد الأسياخ في العمود الواحد:", min_value=4, max_value=20, value=8, step=2)
    with col_st3:
        bldg_use = st.selectbox("الغرض من الاستخدام:", ["سكني", "تجاري / محلات", "مكاتب", "خدمي"])

    if st.button("🚀 إجراء التحليل الهندسي، انتقال الأحمال، وحساب الأوفرلاب الكلي", use_container_width=True):
        st.success("تم حساب وتقسيم الأحمال الهندسية والأوفرلاب بنجاح ✅")

        # أطوال الأوفرلاب
        c_lap_cm = round(48 * c_dia / 10.0, 1) # سم
        c_unit_wt = (c_dia**2) / 162.0 # كغم/م
        
        tot_laps_count = col_count * c_bars * total_floors_cnt
        tot_lap_wt_kg = tot_laps_count * (c_lap_cm / 100.0) * c_unit_wt
        tot_lap_cost = (tot_lap_wt_kg / 1000.0) * live_steel_price

        st.subheader("📊 1. جدول أوزان وأطوال الأوفرلاب والتداخل لجميع الطوابق (Overall Lap Splice Summary):")
        lap_table = [
            {
                "العنصر الإنشائي": "حديد الأعمدة (Columns)",
                "طول الأوفرلاب للطابق الواحد": f"{c_lap_cm} سم (48Ø)",
                "الموقع التنفيذي الموصى به": "في منتصف ارتفاع العمود (Zone B) لتفادي العزوم العالية",
                "الوزن الإجمالي للتداخلات": f"{tot_lap_wt_kg:,.1f} كغم (~{tot_lap_wt_kg/1000:.2f} طن)",
                "الكلفة المادية لحديد الأوفرلاب": f"{tot_lap_cost:,.0f} دينار عراقي"
            }
        ]
        st.table(lap_table)

        st.write("---")
        st.subheader("🪜 2. جدول الأحمال المنتقلة طابقاً بطابق (من المساحات المقطعة):")
        
        unit_dl = 3.2 # kN/m2
        unit_ll = 2.0 if "سكني" in bldg_use else 4.0 # kN/m2
        tot_u = 1.2 * unit_dl + 1.6 * unit_ll
        
        cum_load_all = 0.0
        floor_tak_table = []
        
        for fl in range(total_floors_cnt, 0, -1):
            curr_area = gf_total_area if fl == 1 else tf_total_area
            fl_load = curr_area * tot_u
            cum_load_all += fl_load
            
            fl_title = "الطابق الأرضي (Ground Floor)" if fl == 1 else (f"الطابق ({fl})" if fl < total_floors_cnt else "السطح / السقف الأخير")
            floor_tak_table.append({
                "مستوى الطابق": fl_title,
                "إجمالي مساحة المقاطع": f"{curr_area:.1f} م²",
                "حمل الطابق الصافي": f"{fl_load:,.1f} kN",
                "الحمل التراكمي النازل للأعمدة": f"{cum_load_all:,.1f} kN (~{cum_load_all/10:.1f} طن)",
                "نصيب العمود الواحد": f"{(cum_load_all / col_count):,.1f} kN"
            })

        st.table(floor_tak_table)

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
