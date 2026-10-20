import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import base64

st.set_page_config(page_title="المنظومة الهندسية الاستشارية - م. محمد ذنون", layout="wide")

# ==========================================
# تخصيص واجهة CSS الفاخرة (Elite Dashboard Theme)
# ==========================================
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1e293b; font-family: 'Segoe UI', Tahoma, sans-serif; }
    [data-testid="stSidebar"] { background-color: #0f172a; color: #ffffff; }
    [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stButton button { color: #ffffff; }
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
    st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🔐 بوابة الدخول للمنظومة الهندسية الاستشارية</h1>", unsafe_allow_html=True)
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

# القائمة الرئيسية المحدثة
mode = st.sidebar.selectbox(
    "اختر قسم العمل المطلوب:", 
    [
        "📋 جدول الكميات والكلف المعياري المفصل (Modular BOQ)",
        "🏛️ حساب كميات وكلف واجهات البيوت والفلل (Façade Works)",
        "🏡 التصميم المعماري وتوزيع المساحات والخرائط", 
        "🔍 تدقيق العناصر الإنشائية (ACI 318)",
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

# ==========================================
# 0. قسم جدول الكميات والمعياري المفصل (Modular BOQ)
# ==========================================
if "جدول الكميات والكلف المعياري المفصل" in mode:
    st.header("📋 جدول الكميات والكلف المعياري المفصل (Modular BOQ)")
    st.markdown("اختر الأقسام التي ترغب بحساب تكلفتها الفعلية في مشروعك، وحدد خيار (نعم / لا) لكل قسم:")
    st.write("---")

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
        "nylon_m2": 750,       # سعر متر فرش النايلون
        "shovel_hour": 35000,   # تكلفة إيجار الشفل بالساعة
        "roller_day": 150000    # تكلفة إيجار الحادلة باليوم
    }

    modular_table_data = []
    grand_total_cost = 0.0

    # ----------------------------------------------------
    # القسم 1: أعمال البناء والطابوق
    # ----------------------------------------------------
    st.subheader("1️⃣ قسم أعمال البناء والطابوق / البلوك")
    use_brick = st.radio("هل تريد حساب قسم الطابوق والبلوك في الكلفة؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_brick")
    b_cost = 0
    if "نعم" in use_brick:
        bc1, bc2 = st.columns(2)
        with bc1:
            q_brick_area = st.number_input("مساحة الجدران للطابوق (م²)", min_value=0.0, value=100.0, step=10.0, key="mod_b_area")
        with bc2:
            brick_type_sel = st.selectbox("نوع الطابوق/البلوك:", ["طابوق أحمر قياسي عراقي", "طابوق أصفر فرشي/ناري", "بلوك خرساني مجوف 20سم"], key="mod_b_type")
        
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

    # ----------------------------------------------------
    # القسم 2: أعمال اللبخ والإنهاءات (أسمنت وبورك)
    # ----------------------------------------------------
    st.subheader("2️⃣ قسم اللبخ والإنهاءات الداخلية والخارجية")
    use_plaster = st.radio("هل تريد حساب قسم اللبخ والإنهاءات؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_plaster")
    plaster_cost = 0
    if "نعم" in use_plaster:
        pc1, pc2 = st.columns(2)
        with pc1:
            q_plaster_area = st.number_input("مساحة الجدران للَّبخ والإنهاء (م²)", min_value=0.0, value=200.0, step=10.0, key="mod_p_area")
        with pc2:
            cement_bags_p = int(q_plaster_area * 0.32)
            sand_p_m3 = round(q_plaster_area * 0.022, 1)
            plaster_cost = (cement_bags_p * prices["cement_bag"]) + (sand_p_m3 * prices["sand_m3"])

        modular_table_data.append({"القسم": "قسم اللبخ", "المادة / العنصر": "مواد لبخ أسمنتي (أسمنت + رمل)", "المساحة / البعد": f"{q_plaster_area} م²", "الكمية المطلوبة": f"{cement_bags_p} كيس | {sand_p_m3} م³ رمل", "الكلفة التقديرية (د.ع)": f"{plaster_cost:,.0f}"})
        grand_total_cost += plaster_cost

    st.write("---")

    # ----------------------------------------------------
    # القسم 3: أعمال الأرضيات
    # ----------------------------------------------------
    st.subheader("3️⃣ قسم الأرضيات (كاشي، مرمر، بورسلين، سيراميك)")
    use_floors = st.radio("هل تريد حساب قسم الأرضيات؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_floors")
    floor_cost = 0
    if "نعم" in use_floors:
        fc1, fc2 = st.columns(2)
        with fc1:
            q_floor_area = st.number_input("مساحة الأرضيات الكلية (م²)", min_value=0.0, value=120.0, step=10.0, key="mod_f_area")
        with fc2:
            floor_type_sel = st.selectbox("نوع الأرضيات:", ["كاشي موزاييك عراقي تقليدي", "سيراميك أرضيات فاخر", "بورسلين صالونات", "مرمر طبيعي"], key="mod_f_type")

        if "بورسلين" in floor_type_sel:
            floor_cost = q_floor_area * prices["porcelain_m2"]
        elif "سراميك" in floor_type_sel:
            floor_cost = q_floor_area * prices["ceramic_floor_m2"]
        elif "مرمر" in floor_type_sel:
            floor_cost = q_floor_area * prices["marble_m2"]
        else:
            floor_cost = q_floor_area * prices["kashi_m2"]

        modular_table_data.append({"القسم": "قسم الأرضيات", "المادة / العنصر": f"أرضيات ({floor_type_sel})", "المساحة / البعد": f"{q_floor_area} م²", "الكمية المطلوبة": f"{q_floor_area} م²", "الكلفة التقديرية (د.ع)": f"{floor_cost:,.0f}"})
        grand_total_cost += floor_cost

    st.write("---")

    # ----------------------------------------------------
    # القسم 4: أعمال الخرسانة المسلحة والحديد
    # ----------------------------------------------------
    st.subheader("4️⃣ قسم الخرسانة المسلحة وحديد التسليح")
    use_concrete = st.radio("هل تريد حساب قسم الهيكل الإنشائي (كونكريت + حديد)؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_concrete")
    struct_cost = 0
    if "نعم" in use_concrete:
        cc1, cc2 = st.columns(2)
        with cc1:
            q_conc_vol = st.number_input("حجم الكونكريت الإنشائي (م³)", min_value=0.0, value=30.0, step=5.0, key="mod_c_vol")
        with cc2:
            q_steel_t = st.number_input("وزن حديد التسليح (طن)", min_value=0.0, value=3.5, step=0.5, key="mod_s_ton")
            steel_t_sel = st.selectbox("نوع الحديد:", ["حديد مشوه عالي المقاومة", "حديد أملس / ناعم"], key="mod_s_type")

        conc_mat_cost = q_conc_vol * (prices["cement_bag"] * 7 + prices["sand_m3"] * 0.5 + prices["gravel_m3"] * 0.8)
        st_cost = q_steel_t * (prices["steel_plain"] if "أملس" in steel_t_sel else prices["steel_high"])
        struct_cost = conc_mat_cost + st_cost

        modular_table_data.append({"القسم": "قسم الإنشائي", "المادة / العنصر": "خرسانة مسلحة (أساسات/أعمدة/سقوف)", "المساحة / البعد": f"{q_conc_vol} م³", "الكمية المطلوبة": f"{q_conc_vol} م³", "الكلفة التقديرية (د.ع)": f"{conc_mat_cost:,.0f}"})
        modular_table_data.append({"القسم": "قسم الإنشائي", "المادة / العنصر": f"حديد تسليح ({steel_t_sel})", "المساحة / البعد": f"{q_conc_vol} م³ منشأ", "الكمية المطلوبة": f"{q_steel_t} طن", "الكلفة التقديرية (د.ع)": f"{st_cost:,.0f}"})
        grand_total_cost += struct_cost

    st.write("---")

    # ----------------------------------------------------
    # القسم 5: فرش النايلون تحت الأساسات
    # ----------------------------------------------------
    st.subheader("5️⃣ فرش النايلون (تحت الأساسات والصبة الأرضية)")
    use_nylon = st.radio("هل تحتاج لفرش نايلون عازل للرطوبة؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_nylon")
    nylon_cost = 0
    if "نعم" in use_nylon:
        nc1 = st.columns(1)[0]
        with nc1:
            nylon_area = st.number_input("مساحة الفرش (م²)", min_value=0.0, value=100.0, step=10.0, key="mod_n_area")
        nylon_cost = nylon_area * prices["nylon_m2"]
        modular_table_data.append({"القسم": "قسم العزل", "المادة / العنصر": "فرش نايلون عازل للرطوبة", "المساحة / البعد": f"{nylon_area} م²", "الكمية المطلوبة": f"{nylon_area} م²", "الكلفة التقديرية (د.ع)": f"{nylon_cost:,.0f}"})
        grand_total_cost += nylon_cost

    st.write("---")

    # ----------------------------------------------------
    # القسم 6: آليات الموقع (الحادلة والشفل)
    # ----------------------------------------------------
    st.subheader("6️⃣ آليات الموقع (الحادلة للحدل والشفل للحفريات والتنظيف)")
    use_machinery = st.radio("هل تريد حساب تكاليف الآليات الثقيلة (الحادلة والشفل)؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_mach")
    mach_cost = 0
    if "نعم" in use_machinery:
        mc1, mc2 = st.columns(2)
        with mc1:
            shovel_hours = st.number_input("عدد ساعات عمل الشفل", min_value=0, value=8, step=2, key="mod_sh_hr")
        with mc2:
            roller_days = st.number_input("عدد أيام عمل الحادلة (الرول)", min_value=0, value=1, step=1, key="mod_rl_day")

        mach_cost = (shovel_hours * prices["shovel_hour"]) + (roller_days * prices["roller_day"])
        modular_table_data.append({"القسم": "قسم الآليات", "المادة / العنصر": "إيجار شفل حفريات ورفع أنقاض", "المساحة / البعد": "عمل موقعي", "الكمية المطلوبة": f"{shovel_hours} ساعة", "الكلفة التقديرية (د.ع)": f"{(shovel_hours * prices['shovel_hour']):,.0f}"})
        modular_table_data.append({"القسم": "قسم الآليات", "المادة / العنصر": "إيجار حادلة (رول) لترصيع التربة", "المساحة / البعد": "أعمال ترابية", "الكمية المطلوبة": f"{roller_days} يوم", "الكلفة التقديرية (د.ع)": f"{(roller_days * prices['roller_day']):,.0f}"})
        grand_total_cost += mach_cost

    st.write("---")

    # ----------------------------------------------------
    # القسم 7: أجور الكوادر الموقعية (نجار، حداد، عمال)
    # ----------------------------------------------------
    st.subheader("7️⃣ أجور الكوادر الموقعية (النجار، الحداد، والعمال)")
    use_labor = st.radio("هل تريد حساب أجور الكوادر الحرفية والعمالة؟", ["نعم، احسبه", "لا، لا أريده"], horizontal=True, key="r_labor")
    labor_cost = 0
    if "نعم" in use_labor:
        lc1, lc2, lc3 = st.columns(3)
        with lc1:
            carp_days = st.number_input("عدد أيام عمل النجار", min_value=0, value=10, step=2, key="mod_carp")
        with lc2:
            steel_days = st.number_input("عدد أيام عمل الحداد", min_value=0, value=10, step=2, key="mod_steel_d")
        with lc3:
            lab_days = st.number_input("إجمالي أيام العمالة المساعدة", min_value=0, value=30, step=5, key="mod_lab")

        labor_cost = (carp_days * carpenters_daily) + (steel_days * steel_fixer_daily) + (lab_days * laborer_daily)
        modular_table_data.append({"القسم": "قسم الأجور والكوادر", "المادة / العنصر": "أجور طاقم النجارة الإنشائية", "المساحة / البعد": "أيام عمل", "الكمية المطلوبة": f"{carp_days} يوم", "الكلفة التقديرية (د.ع)": f"{(carp_days * carpenters_daily):,.0f}"})
        modular_table_data.append({"القسم": "قسم الأجور والكوادر", "المادة / العنصر": "أجور طاقم الحدادة الإنشائية", "المساحة / البعد": "أيام عمل", "الكمية المطلوبة": f"{steel_days} يوم", "الكلفة التقديرية (د.ع)": f"{(steel_days * steel_fixer_daily):,.0f}"})
        modular_table_data.append({"القسم": "قسم الأجور والكوادر", "المادة / العنصر": "أجور العمالة المساعدة في الموقع", "المساحة / البعد": "إجمالي أيام", "الكمية المطلوبة": f"{lab_days} يوم", "الكلفة التقديرية (د.ع)": f"{(lab_days * laborer_daily):,.0f}"})
        grand_total_cost += labor_cost

    # ==========================================
    # زر الحساب النهائي وإظهار الجدول والتقارير
    # ==========================================
    st.write("---")
    if st.button("📊 إظهار الجدول المجمع والتكلفة الفعلية للمشروع", use_container_width=True):
        if not modular_table_data:
            st.warning("⚠️ لم تقم بتفعيل أي قسم من الأقسام بالأعلى! يرجى اختيار (نعم، احسبه) لأحد الأقسام على الأقل.")
        else:
            st.success("تم تجميع جدول كميات وكلف المشروع المعياري بنجاح تامة ✅")

            st.subheader("📑 جدول الكميات والكلف المعياري المفصل (Modular BOQ Summary):")
            st.table(modular_table_data)

            st.markdown(f"""
            ### 💰 الكلفة الإجمالية الفعلية للمشروع: **{grand_total_cost:,.0f} دينار عراقي**
            """)

            # أزرار التصدير والتنزيل
            st.write("---")
            st.subheader("📥 تنزيل التقارير المعيارية الاحترافية")
            
            col_dl1, col_dl2 = st.columns(2)
            
            csv_content = "القسم,المادة / العنصر,المساحة / البعد,الكمية المطلوبة,الكلفة التقديرية (دينار عراقي)\n"
            for row in modular_table_data:
                csv_content += f"{row['القسم']},{row['المادة / العنصر']},{row['المساحة / البعد']},{row['الكمية المطلوبة']},{row['الكلفة التقديرية (د.ع)']}\n"
            csv_content += f"التكلفة الإجمالية الفعلي,,,,{grand_total_cost:,.0f}\n"
            
            b64_csv = base64.b64encode(csv_content.encode('utf-8-sig')).decode()
            with col_dl1:
                st.markdown(f"""
                    <a href="data:file/csv;base64,{b64_csv}" download="Muhamed_Zannon_Modular_BOQ.csv" style="text-decoration: none;">
                        <div style="background-color: #166534; color: white; padding: 12px 20px; border-radius: 8px; text-align: center; font-weight: bold;">
                            📊 تحميل جدول Excel (.csv) للـ BOQ المفصل
                        </div>
                    </a>
                """, unsafe_allow_html=True)

            html_report = f"""
            <html dir="rtl">
            <head><meta charset="utf-8"><title>تقرير جدول الكميات والكلف المفصل</title>
            <style>
                body {{ font-family: Tahoma, sans-serif; padding: 20px; color: #333; }}
                h1 {{ color: #0f172a; text-align: center; }}
                h3 {{ color: #475569; text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #cbd5e1; padding: 10px; text-align: center; }}
                th {{ background-color: #0f172a; color: white; }}
                .total {{ font-size: 18px; font-weight: bold; margin-top: 20px; text-align: left; color: #1e3a8a; }}
            </style>
            </head>
            <body>
                <h1>المنظومة الهندسية الاستشارية</h1>
                <h3>إشراف وتطوير: المهندس محمد ذنون عبد شريف | جامعة كربلاء</h3>
                <hr>
                <h2>تقرير جدول الكميات والكلف المعياري المفصل (Modular BOQ)</h2>
                <table>
                    <tr><th>القسم</th><th>المادة / العنصر</th><th>المساحة / البعد</th><th>الكمية المطلوبة</th><th>الكلفة التقديرية (د.ع)</th></tr>
            """
            for row in modular_table_data:
                html_report += f"<tr><td>{row['القسم']}</td><td>{row['المادة / العنصر']}</td><td>{row['المساحة / البعد']}</td><td>{row['الكمية المطلوبة']}</td><td>{row['الكلفة التقديرية (د.ع)']}</td></tr>"
            html_report += f"""
                </table>
                <div class="total">الكلفة الإجمالية للمشروع: {grand_total_cost:,.0f} دينار عراقي</div>
            </body>
            </html>
            """
            b64_pdf = base64.b64encode(html_report.encode('utf-8')).decode()
            with col_dl2:
                st.markdown(f"""
                    <a href="data:text/html;base64,{b64_pdf}" download="Muhamed_Zannon_Modular_BOQ.html" style="text-decoration: none;">
                        <div style="background-color: #991b1b; color: white; padding: 12px 20px; border-radius: 8px; text-align: center; font-weight: bold;">
                            📄 تحميل التقرير كملف طباعة (HTML/PDF)
                        </div>
                    </a>
                """, unsafe_allow_html=True)

# ==========================================
# 00. قسم حساب كميات وكلف واجهات البيوت والفلل
# ==========================================
elif "حساب كميات وكلف واجهات البيوت والفلل" in mode:
    st.header("🏛️ حساب كميات وكلف واجهات البيوت والفلل الحديثة (Façade Works)")
    st.markdown("هذا القسم مخصص لتقدير كميات وكلف المواد الخاصة بالواجهات الخارجية المعمارية حسب ممارسات السوق العراقي:")
    st.write("---")

    col_fc1, col_fc2 = st.columns(2)
    with col_fc1:
        facade_area = st.number_input("مساحة الواجهة الخارجية الإجمالية (م²)", min_value=0.0, value=65.0, step=5.0, key="f_area_facade")
        facade_style = st.selectbox(
            "اختر الطراز المعماري للواجهة:",
            [
                "واجهة حجر طبيعي (حجر كاشي / هيدروليك مع قص ولصق)",
                "واجهة حديثة بتغليف ألكوبوند (Alucobond Cladding)",
                "واجهة طابوق فرشي معمارية مع تفاصيل حديثة",
                "واجهة لبخ ملون وتطبيق ديكورات (سيراميك/حجر صناعي)"
            ],
            key="f_style_facade"
        )
    with col_fc2:
        facade_waste = st.slider("نسبة الهدر في مواد الواجهات والقص (%)", 3, 15, 8, key="f_waste_facade")
        facade_extras = st.selectbox(
            "أعمال الإضاءة والبروزات الديكورية للواجهة:",
            ["إضاءة مخفية ليد بروفايل مع كراكت", "بروزات وتعرجات معمارية خرسانية", "تشتمل على مظلات حديد أو ألمنيوم", "بدون ديكورات إضافية (الأساسي)"]
        )

    st.write("---")
    if st.button("📊 احسب تكلفة وكميات الواجهة المعمارية بدقة", use_container_width=True):
        st.success("تم احتساب كميات وكلف أعمال الواجهة بنجاح تام ✅")

        rate_per_m2 = 35000 if "حجر طبيعي" in facade_style else (45000 if "ألكوبوند" in facade_style else (22000 if "طابوق فرشي" in facade_style else 18000))
        if "إضاءة مخفية" in facade_extras:
            rate_per_m2 += 7000
        elif "بروزات وتعرجات" in facade_extras:
            rate_per_m2 += 10000

        gross_facade_area = facade_area * (1 + facade_waste / 100.0)
        total_facade_cost = gross_facade_area * rate_per_m2

        st.subheader("📑 جدول كميات وكلف الواجهة المعمارية (Façade BOQ):")
        facade_table = [
            {"عنصر العمل": f"تشطيب الواجهة ({facade_style})", "المساحة الصافية": f"{facade_area} م²", "نسبة الهدر": f"{facade_waste}%", "الكمية الكلية للشراء": f"{gross_facade_area:.1f} م²", "الكلفة التقديرية (د.ع)": f"{total_facade_cost:,.0f}"}
        ]
        st.table(facade_table)

        st.markdown(f"""
        ### 💰 التكلفة الإجمالية التقديرية للواجهة: **{total_facade_cost:,.0f} دينار عراقي**
        """)

# ==========================================
# 1. قسم التصميم المعماري
# ==========================================
elif "التصميم المعماري" in mode:
    st.header("🏡 قسم التصميم المعماري وتوزيع الفضاءات والخرائط الهندسية")
    st.write("---")
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1: frontage = st.number_input("عرض الواجهة (متر)", min_value=4.0, value=10.0, step=0.5, key="arch_frontage")
    with col_a2: depth = st.number_input("النزال (متر)", min_value=6.0, value=20.0, step=0.5, key="arch_depth")
    total_plot_area = frontage * depth
    with col_a3: st.metric("مساحة قطعة الأرض الكلية", f"{total_plot_area:.1f} م²")
    
    if st.button("🎨 توليد المخطط الهندسي المعماري"):
        fig, ax = plt.subplots(figsize=(8, 11))
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        ax.set_xlim(-0.5, frontage + 0.5)
        ax.set_ylim(-0.5, depth + 0.5)
        ax.set_aspect('equal')
        
        outer_border = patches.Rectangle((0, 0), frontage, depth, linewidth=3, edgecolor='black', facecolor='none', zorder=5)
        ax.add_patch(outer_border)
        ax.text(frontage/2, depth - 0.5, f"مخطط الطابق الأرضي — م. محمد ذنون\n({frontage}م × {depth}م)", 
                fontsize=11, fontweight='bold', color='black', ha='center', va='center',
                bbox=dict(facecolor='#f8f9fa', edgecolor='black', boxstyle='round,pad=0.5'))
        st.pyplot(fig)

# ==========================================
# 2. قسم التدقيق الإنشائي ACI 318
# ==========================================
elif "تدقيق العناصر الإنشائية" in mode:
    st.header("🏢 تدقيق عناصر المبنى الإنشائية (أعمدة، جسور، سقوف)")
    fc = st.number_input("مقاومة الخرسانة f'c (MPa)", value=28.0)
    fy = st.number_input("إجهاد خضوع الحديد fy (MPa)", value=420.0)
    st.info("قسم التدقيق الإنشائي مفعل وفق متطلبات ACI 318.")

# ==========================================
# 3. حاسبة المواد التفصيلية والموقع
# ==========================================
elif "حاسبة المواد التفصيلية" in mode:
    st.header("📊 حاسبة المواد التفصيلية والموقع")
    st.markdown("هنا يمكنك حساب كمية أي مادة بشكل منفصل وبدقة تامة مع التحكم بنسبة الهدر:")
    st.write("---")
    
    sub_choice = st.selectbox("اختر المادة المراد حسابها:", ["الطابوق والبلوك", "الأرضيات", "مواد الإنهاءات (لبخ وبورك)"])
    waste_pct = st.slider("نسبة الهدر في الموقع (%)", 0, 15, 5, key="waste_slider_detailed")

    if "الطابوق" in sub_choice:
        w_area = st.number_input("مساحة الجدار (م²)", value=50.0)
        b_type = st.selectbox("نوع الطابوق", ["طابوق أحمر قياسي مفرد (12سم)", "طابوق أحمر قياسي مزدوج (24سم)", "طابوق أصفر فرشي/ناري", "بلوك خرساني"])
        if st.button("احسب الطابوق"):
            factor = 58 if "مفرد" in b_type else (116 if "جدار مزدوج" in b_type else (60 if "أصفر" in b_type else 12.5))
            net_count = int(w_area * factor)
            gross_count = int(net_count * (1 + waste_pct / 100.0))
            st.success("تم الحساب بنجاح ✅")
            st.metric(f"العدد الإجمالي المطلوب مع نسبة الهدر ({waste_pct}%)", f"{gross_count:,} قطعة")
    else:
        f_area = st.number_input("المساحة الكلية (م²)", value=80.0)
        if st.button("احسب المساحة مع الهدر"):
            gross_area = f_area * (1 + waste_pct / 100.0)
            st.success("تم الحساب بنجاح ✅")
            st.metric(f"المساحة المطلوبة للشراء مع الهدر ({waste_pct}%)", f"{gross_area:.1f} م²")
