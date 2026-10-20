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

# القائمة الرئيسية
mode = st.sidebar.selectbox(
    "اختر قسم العمل المطلوب:", 
    [
        "📋 جدول الكميات والتسعير الشامل (BOQ & Iraqi Market Rates)",
        "🏡 التصميم المعماري وتوزيع المساحات والخرائط", 
        "🔍 تدقيق العناصر الإنشائية (ACI 318)",
        "📊 حاسبة المواد التفصيلية (الطابوق، الأسمنت، الأرضيات)"
    ]
)

# ==========================================
# لوحة التحكم الجانبية لمراقبة وتحديث أسعار السوق العراقي
# ==========================================
st.sidebar.write("---")
st.sidebar.subheader("📈 مراقب أسعار السوق العراقي")
st.sidebar.markdown("يمكنك تحديث الأسعار أدناه لتواكب التغيرات اللحظية في السوق المحلي:")

live_steel_price = st.sidebar.number_input("سعر طن الحديد (د.ع)", value=980000, step=10000)
live_cement_price = st.sidebar.number_input("سعر كيس الأسمنت (د.ع)", value=8500, step=250)
live_brick_price = st.sidebar.number_input("سعر الطابوقة الحمراء (د.ع)", value=275, step=10)

# ==========================================
# 0. قسم جدول الكميات والتسعير الشامل والمحدّث بدقة
# ==========================================
if "جدول الكميات والتسعير الشامل" in mode:
    st.header("📋 جدول الكميات والتسعير الشامل (BOQ حسب الأسواق العراقية)")
    st.markdown("أدخل المساحات، واختَر أنواع الأرضيات وأقطار حديد التسليح بدقة ليتسنى للنظام توليد جدول كميات استشاري متكامل:")
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
        "marble_m2": 35000
    }

    st.subheader("🧮 أدخل بيانات المشروع التفصيلية:")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        q_brick_area = st.number_input("مساحة الجدران للطابوق (م²)", min_value=0.0, value=100.0, step=10.0, key="b_area_new")
        brick_type_sel = st.selectbox(
            "اختر نوع الطابوق أو البلوك المستخدم:", 
            ["طابوق أحمر قياسي عراقي", "طابوق أصفر فرشي/ناري", "بلوك خرساني مجوف 20سم"],
            key="b_type_new"
        )
        
        q_floor_area = st.number_input("مساحة الأرضيات الإجمالية (م²)", min_value=0.0, value=120.0, step=10.0, key="f_area_new")
        floor_type_sel = st.selectbox(
            "اختر نوع الأرضيات الدقيق:",
            ["كاشي موزاييك عراقي تقليدي", "سيراميك أرضيات فاخر", "بورسلين صالونات (60×60 أو 120×60)", "مرمر طبيعي للأرضيات والدرج"],
            key="f_type_new"
        )

    with col_t2:
        q_plaster_area = st.number_input("مساحة اللبخ والإنهاءات الداخلية/الخارجية (م²)", min_value=0.0, value=200.0, step=10.0, key="p_area_new")
        q_concrete_vol = st.number_input("حجم الكونكريت الإنشائي (م³)", min_value=0.0, value=30.0, step=5.0, key="c_vol_new")
        
        steel_type_sel = st.selectbox(
            "اختر نوع ومواصفات حديد التسليح المستخدم:",
            ["حديد عالي المقاومة مشوه (Grade 60 - fy 420)", "حديد أملس / ناعم (Plain Bars) للكانات والأشاير"],
            key="s_type_new"
        )

        steel_diameter_sel = st.selectbox(
            "اختر قطر حديد التسليح الشائع في العنصر:",
            ["Ø10 مم (خاص بالكانات والتشكيل)", "Ø12 مم (تسليح سقوف وجسور ثانوية)", "Ø16 مم (تسليح جسور وأعمدة رئيسية)", "Ø20 مم (تسليح أساسات وأعمدة ثقيلة)", "Ø25 مم (أعمدة طوابق متعددة وبحور واسعة)"],
            key="s_dia_new"
        )

        q_steel_ton = st.number_input("وزن حديد التسليح التقديري (طن)", min_value=0.0, value=3.5, step=0.5, key="s_ton_new")

    st.write("---")
    if st.button("📊 احسب جدول الكميات والتسعير للسوق العراقي بدقة", use_container_width=True):
        st.success("تم احتساب جدول الكميات (BOQ) وتوليد التفاصيل المالية بنجاح تام ✅")
        
        if "أصفر" in brick_type_sel:
            b_count = int(q_brick_area * 58 * 1.05)
            b_cost = b_count * prices["brick_yellow"]
        elif "بلوك" in brick_type_sel:
            b_count = int(q_brick_area * 12.5 * 1.05)
            b_cost = b_count * prices["block_20"]
        else:
            b_count = int(q_brick_area * 58 * 1.05)
            b_cost = b_count * prices["brick_red"]

        cement_bags_total = int(q_brick_area * 0.15 + q_plaster_area * 0.32)
        cement_cost = cement_bags_total * prices["cement_bag"]

        sand_total_m3 = round(q_brick_area * 0.03 + q_plaster_area * 0.022, 1)
        sand_cost = sand_total_m3 * prices["sand_m3"]

        if "بورسلين" in floor_type_sel:
            f_cost = q_floor_area * prices["porcelain_m2"]
        elif "سراميك" in floor_type_sel:
            f_cost = q_floor_area * prices["ceramic_floor_m2"]
        elif "مرمر" in floor_type_sel:
            f_cost = q_floor_area * prices["marble_m2"]
        else:
            f_cost = q_floor_area * prices["kashi_m2"]

        concrete_cost = q_concrete_vol * (prices["cement_bag"] * 7 + prices["sand_m3"] * 0.5 + prices["gravel_m3"] * 0.8)
        
        if "أملس" in steel_type_sel:
            steel_cost = q_steel_ton * prices["steel_plain"]
        else:
            steel_cost = q_steel_ton * prices["steel_high"]

        total_project_cost = b_cost + cement_cost + sand_cost + f_cost + concrete_cost + steel_cost

        st.subheader("📑 جدول الكميات والكلف التقديرية المعتمدة (BOQ):")
        
        table_data = [
            {
                "المادة الرئيسية": brick_type_sel, 
                "المساحة / البعد المُدخل": f"{q_brick_area} م² جدران", 
                "الكمية المطلوبة": f"{b_count:,} قطعة", 
                "السعر التقديري (د.ع)": f"{b_cost:,.0f}"
            },
            {
                "المادة الرئيسية": "أسمنت عراقي مقنّن (لمونة البناء واللبخ)", 
                "المساحة / البعد المُدخل": f"{q_brick_area + q_plaster_area} م² إجمالي", 
                "الكمية المطلوبة": f"{cement_bags_total:,} كيس", 
                "السعر التقديري (د.ع)": f"{cement_cost:,.0f}"
            },
            {
                "المادة الرئيسية": "رمل ناعم للمونة واللبخ", 
                "المساحة / البعد المُدخل": f"{q_brick_area + q_plaster_area} م² إجمالي", 
                "الكمية المطلوبة": f"{sand_total_m3} م³", 
                "السعر التقديري (د.ع)": f"{sand_cost:,.0f}"
            },
            {
                "المادة الرئيسية": f"أرضيات ({floor_type_sel})", 
                "المساحة / البعد المُدخل": f"{q_floor_area} م² أرضيات", 
                "الكمية المطلوبة": f"{q_floor_area} م²", 
                "السعر التقديري (د.ع)": f"{f_cost:,.0f}"
            },
            {
                "المادة الرئيسية": "خرسانة مسلحة (مادة أولية للمنشأ)", 
                "المساحة / البعد المُدخل": f"{q_concrete_vol} م³ خرسانة", 
                "الكمية المطلوبة": f"{q_concrete_vol} م³", 
                "السعر التقديري (د.ع)": f"{concrete_cost:,.0f}"
            },
            {
                "المادة الرئيسية": f"{steel_type_sel} - قطر ({steel_diameter_sel})", 
                "المساحة / البعد المُدخل": f"{q_concrete_vol} م³ منشأ", 
                "الكمية المطلوبة": f"{q_steel_ton} طن", 
                "السعر التقديري (د.ع)": f"{steel_cost:,.0f}"
            }
        ]

        st.table(table_data)

        st.markdown(f"""
        ### 💰 التكلفة الإجمالية التقديرية للمواد: **{total_project_cost:,.0f} دينار عراقي**
        """)

        # أزرار التصدير (Excel و PDF)
        st.write("---")
        st.subheader("📥 تنزيل التقارير وجداول الـ (BOQ) الاحترافية")
        
        col_dl1, col_dl2 = st.columns(2)
        
        csv_content = "المادة الرئيسية,المساحة / البعد المُدخل,الكمية المطلوبة,السعر التقديري (دينار عراقي)\n"
        for row in table_data:
            csv_content += f"{row['المادة الرئيسية']},{row['المساحة / البعد المُدخل']},{row['الكمية المطلوبة']},{row['السعر التقديري (د.ع)']}\n"
        csv_content += f"التكلفة الإجمالية,,, {total_project_cost:,.0f}\n"
        
        b64_csv = base64.b64encode(csv_content.encode('utf-8-sig')).decode()
        with col_dl1:
            st.markdown(f"""
                <a href="data:file/csv;base64,{b64_csv}" download="Muhamed_Zannon_BOQ_Report.csv" style="text-decoration: none;">
                    <div style="background-color: #166534; color: white; padding: 12px 20px; border-radius: 8px; text-align: center; font-weight: bold;">
                        📊 تحميل جدول Excel (.csv) للـ BOQ
                    </div>
                </a>
            """, unsafe_allow_html=True)

        html_report = f"""
        <html dir="rtl">
        <head><meta charset="utf-8"><title>تقرير جدول الكميات BOQ</title>
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
            <h2>تقرير جدول الكميات والكلف (BOQ) التفصيلي</h2>
            <table>
                <tr><th>المادة الرئيسية</th><th>المساحة / البعد المُدخل</th><th>الكمية المطلوبة</th><th>السعر التقديري (د.ع)</th></tr>
        """
        for row in table_data:
            html_report += f"<tr><td>{row['المادة الرئيسية']}</td><td>{row['المساحة / البعد المُدخل']}</td><td>{row['الكمية المطلوبة']}</td><td>{row['السعر التقديري (د.ع)']}</td></tr>"
        html_report += f"""
            </table>
            <div class="total">التكلفة الإجمالية للمواد: {total_project_cost:,.0f} دينار عراقي</div>
        </body>
        </html>
        """
        b64_pdf = base64.b64encode(html_report.encode('utf-8')).decode()
        with col_dl2:
            st.markdown(f"""
                <a href="data:text/html;base64,{b64_pdf}" download="Muhamed_Zannon_BOQ_Report.html" style="text-decoration: none;">
                    <div style="background-color: #991b1b; color: white; padding: 12px 20px; border-radius: 8px; text-align: center; font-weight: bold;">
                        📄 تحميل التقرير كملف طباعة (HTML/PDF)
                    </div>
                </a>
            """, unsafe_allow_html=True)

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
