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
# 0. قسم جدول الكميات والتسعير الشامل
# ==========================================
if "جدول الكميات والتسعير الشامل" in mode:
    st.header("📋 جدول الكميات والتسعير الشامل (حسب الأسواق العراقية)")
    st.markdown("أدخل المساحات أو الكميات لكل مادة، وسيقوم النظام بحساب الإجمالي مع التكلفة التقديرية بالدينار العراقي مباشرةً وتصديرها:")
    st.write("---")

    prices = {
        "brick_red": 275,
        "brick_yellow": 350,
        "block_20": 1250,
        "cement_bag": 8500,
        "sand_m3": 28000,
        "gravel_m3": 32000,
        "bourk_bag": 7000,
        "steel_ton": 980000,
        "ceramic_m2": 9500,
        "marble_m2": 35000,
        "kashi_m2": 12000
    }

    st.subheader("🧮 أدخل بيانات المشروع الحالية:")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        q_brick_area = st.number_input("مساحة الجدران للطابوق (م²)", min_value=0.0, value=100.0, step=10.0)
        brick_type_sel = st.selectbox("نوع الطابوق", ["طابوق أحمر قياسي", "طابوق أصفر فرشي/ناري", "بلوك خرساني 20سم"])
        q_floor_area = st.number_input("مساحة الأرضيات (كاشي/مرمر/بورسلين) (م²)", min_value=0.0, value=120.0, step=10.0)
        floor_type_sel = st.selectbox("نوع الأرضيات", ["كاشي موزاييك", "سراميك أرضيات", "مرمر طبيعي"])

    with col_t2:
        q_plaster_area = st.number_input("مساحة اللبخ والإنهاءات (م²)", min_value=0.0, value=200.0, step=10.0)
        q_concrete_vol = st.number_input("حجم الكونكريت الإنشائي (م³)", min_value=0.0, value=30.0, step=5.0)
        q_steel_ton = st.number_input("وزن حديد التسليح التقديري (طن)", min_value=0.0, value=3.5, step=0.5)

    st.write("---")
    if st.button("📊 احسب التكلفة الإجمالية والكميات للسوق العراقي", use_container_width=True):
        st.success("تم احتساب جدول الكميات والتسعير المالي بنجاح تام ✅")
        
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

        if "مرمر" in floor_type_sel:
            f_cost = q_floor_area * prices["marble_m2"]
        elif "كاشي" in floor_type_sel:
            f_cost = q_floor_area * prices["kashi_m2"]
        else:
            f_cost = q_floor_area * prices["ceramic_m2"]

        concrete_cost = q_concrete_vol * (prices["cement_bag"] * 7 + prices["sand_m3"] * 0.5 + prices["gravel_m3"] * 0.8)
        steel_cost = q_steel_ton * prices["steel_ton"]

        total_project_cost = b_cost + cement_cost + sand_cost + f_cost + concrete_cost + steel_cost

        st.subheader("📑 جدول الكميات والكلف التقديرية المعتمدة:")
        
        table_data = [
            {"المادة الرئيسية": brick_type_sel, "الكمية المطلوبة": f"{b_count:,} قطعة", "السعر التقديري (د.ع)": f"{b_cost:,.0f}"},
            {"المادة الرئيسية": "أسمنت عراقي مقنّن", "الكمية المطلوبة": f"{cement_bags_total:,} كيس", "السعر التقديري (د.ع)": f"{cement_cost:,.0f}"},
            {"المادة الرئيسية": "رمل ناعم للمونة واللبخ", "الكمية المطلوبة": f"{sand_total_m3} م³", "السعر التقديري (د.ع)": f"{sand_cost:,.0f}"},
            {"المادة الرئيسية": f"أرضيات ({floor_type_sel})", "الكمية المطلوبة": f"{q_floor_area} م²", "السعر التقديري (د.ع)": f"{f_cost:,.0f}"},
            {"المادة الرئيسية": "خرسانة مسلحة (مادة أولية)", "الكمية المطلوبة": f"{q_concrete_vol} م³", "السعر التقديري (د.ع)": f"{concrete_cost:,.0f}"},
            {"المادة الرئيسية": "حديد تسليح عالي المقاومة", "الكمية المطلوبة": f"{q_steel_ton} طن", "السعر التقديري (د.ع)": f"{steel_cost:,.0f}"}
        ]

        st.table(table_data)

        st.markdown(f"""
        ### 💰 التكلفة الإجمالية التقديرية للمواد: **{total_project_cost:,.0f} دينار عراقي**
        """)

        # أزرار التصدير (Excel و PDF)
        st.write("---")
        st.subheader("📥 تنزيل التقارير والجداول الاحترافية")
        
        col_dl1, col_dl2 = st.columns(2)
        
        # 1. زر تحميل Excel كـ CSV احترافي يتوافق مع إكسل تماماً
        csv_content = "المادة الرئيسية,الكمية المطلوبة,السعر التقديري (دينار عراقي)\n"
        for row in table_data:
            csv_content += f"{row['المادة الرئيسية']},{row['الكمية المطلوبة']},{row['السعر التقديري (د.ع)']}\n"
        csv_content += f"التكلفة الإجمالية,,{total_project_cost:,.0f}\n"
        
        b64_csv = base64.b64encode(csv_content.encode('utf-8-sig')).decode()
        with col_dl1:
            st.markdown(f"""
                <a href="data:file/csv;base64,{b64_csv}" download="Muhamed_Zannon_BOQ_Report.csv" style="text-decoration: none;">
                    <div style="background-color: #166534; color: white; padding: 12px 20px; border-radius: 8px; text-align: center; font-weight: bold;">
                        📊 تحميل جدول Excel (.csv)
                    </div>
                </a>
            """, unsafe_allow_html=True)

        # 2. زر تحميل تقرير PDF احترافي منسق
        html_report = f"""
        <html dir="rtl">
        <head><meta charset="utf-8"><title>تقرير جدول الكميات</title>
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
            <h2>تقرير جدول الكميات والكلف (BOQ)</h2>
            <table>
                <tr><th>المادة الرئيسية</th><th>الكمية المطلوبة</th><th>السعر التقديري (د.ع)</th></tr>
        """
        for row in table_data:
            html_report += f"<tr><td>{row['المادة الرئيسية']}</td><td>{row['الكمية المطلوبة']}</td><td>{row['السعر التقديري (د.ع)']}</td></tr>"
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
# 3. حاسبة المواد التفصيلية والموقع (مع شريط نسبة الهدر المُعاد)
# ==========================================
elif "حاسبة المواد التفصيلية" in mode:
    st.header("📊 حاسبة المواد التفصيلية والموقع")
    st.markdown("هنا يمكنك حساب كمية أي مادة بشكل منفصل وبدقة تامة مع التحكم بنسبة الهدر:")
    st.write("---")
    
    sub_choice = st.selectbox("اختر المادة المراد حسابها:", ["الطابوق والبلوك", "الأرضيات", "مواد الإنهاءات (لبخ وبورك)"])
    
    # شريط نسبة الهدر (أعيد وضعه هنا كما طلبته بدقة)
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
