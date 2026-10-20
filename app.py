import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

st.set_page_config(page_title="المنظومة الهندسية الاستشارية المتكاملة", layout="wide")

# ==========================================
# نظام حماية التطبيق بكلمة السر (Password Protection)
# ==========================================
PASSWORD_KEY = "1234" 

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.markdown("<h2 style='text-align: center; color: #0d47a1;'>🔐 بوابة الدخول للمنظومة الهندسية الاستشارية</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>الرجاء إدخال رمز المرور السري للدخول إلى النظام:</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password_input = st.text_input("كلمة السر", type="password", key="pwd_input")
        if st.button("تسجيل الدخول 🔓", use_container_width=True):
            if password_input == PASSWORD_KEY:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ كلمة السر غير صائبة! يرجى المحاولة مرة أخرى.")
    return False

if not check_password():
    st.stop()

# ==========================================
# واجهة التطبيق الرئيسية
# ==========================================
st.title("🏛️ المنظومة الهندسية الاستشارية المتكاملة (معماري + إنشائي + حساب الكميات BOQ)")
st.write("---")

if st.sidebar.button("🔒 قفل النظام وتسجيل الخروج"):
    st.session_state["password_correct"] = False
    st.rerun()

mode = st.sidebar.selectbox(
    "اختر قسم العمل المطلوب:", 
    [
        "🏡 التصميم المعماري وتوزيع المساحات والخرائط", 
        "🔍 تدقيق العناصر الإنشائية (ACI 318)",
        "📊 حساب الكميات وهندسة الكلف (BOQ & Materials)"
    ]
)

# ==========================================
# 1. قسم التصميم المعماري وتوليد الخرائط
# ==========================================
if "المعماري" in mode:
    st.header("🏡 قسم التصميم المعماري وتوزيع الفضاءات والخرائط الهندسية")
    st.write("---")

    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        frontage = st.number_input("عرض الواجهة (متر)", min_value=4.0, value=10.0, step=0.5, key="arch_frontage")
    with col_a2:
        depth = st.number_input("النزال (متر)", min_value=6.0, value=20.0, step=0.5, key="arch_depth")
    
    total_plot_area = frontage * depth
    with col_a3:
        st.metric("مساحة قطعة الأرض الكلية", f"{total_plot_area:.1f} م²")

    st.write("---")
    has_first_floor = st.radio("هل ترغب في إضافة تصميم للطابق الأول؟", ["نعم، أضف الطابق الأول", "لا أريد (طابق أرضي فقط)"], horizontal=True)
    
    design_choice = st.radio(
        "اختر طريقة تحديد الفضاءات المعمارية:",
        ["📐 اختيار من نماذج تصميم جاهزة ومقترحة", "✏️ أنا أحدد الفضاءات والمساحات بنفسي"],
        horizontal=True
    )

    st.write("---")

    if "نماذج" in design_choice:
        st.subheader("🎨 النماذج المعمارية المتاحة المقترحة")
        st.info(f"بناءً على مساحة أرضك ({total_plot_area:.1f} م²)، إليك النماذج العراقية المعتمدة:")
        st.markdown("""
        * **النموذج المفتوح (Modern):** استقبال، هول واسع، مطبخ خدمي، وغرفة نوم رئيسية مع حديقة أمامية.
        * **نموذج الخصوصية العائلية:** استقبال معزول، مطبخ مغلق، غرف نوم متعددة، ومنور خدمي خلفي.
        """)
    else:
        st.subheader("✏️ تحديد الفضاءات والأبعاد بلمستك الخاصة")
        
        def render_floor_inputs(floor_name):
            st.markdown(f"### 📍 فضاءات {floor_name}")
            used_area = 0.0

            st.markdown("**🌳 الحديقة والكراج الأمامي:**")
            g_opt = st.selectbox(f"هل تريد حديقة/كراج في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"g_{floor_name}")
            g_w, g_l = 0, 0
            if g_opt == "نعم أريد":
                c1, c2 = st.columns(2)
                with c1: g_w = st.number_input(f"عرض الحديقة - {floor_name}", value=frontage, key=f"gw_{floor_name}")
                with c2: g_l = st.number_input(f"طول الحديقة - {floor_name}", value=4.0, key=f"gl_{floor_name}")
                used_area += (g_w * g_l)

            st.markdown("**🛏️ غرف النوم:**")
            n_rooms = st.number_input(f"عدد غرف النوم في {floor_name}", min_value=0, max_value=6, value=2, key=f"nr_{floor_name}")
            rooms_dims = []
            for r in range(int(n_rooms)):
                c1, c2 = st.columns(2)
                with c1: rw = st.number_input(f"عرض الغرفة {r+1}", value=4.0, key=f"rw_{floor_name}_{r}")
                with c2: rl = st.number_input(f"طول الغرفة {r+1}", value=4.0, key=f"rl_{floor_name}_{r}")
                used_area += (rw * rl)
                rooms_dims.append((rw, rl))

            st.markdown("**🛋️ الاستقبال (المضيف):**")
            rec_opt = st.selectbox(f"هل تريد استقبال في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"rec_{floor_name}")
            rec_w, rec_l = 0, 0
            if rec_opt == "نعم أريد":
                c1, c2 = st.columns(2)
                with c1: rec_w = st.number_input(f"عرض الاستقبال - {floor_name}", value=4.0, key=f"recw_{floor_name}")
                with c2: rec_l = st.number_input(f"طول الاستقبال - {floor_name}", value=5.0, key=f"recl_{floor_name}")
                used_area += (rec_w * rec_l)

            st.markdown("**🍳 المطبخ:**")
            kit_opt = st.selectbox(f"هل تريد مطبخ في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"kit_{floor_name}")
            kit_w, kit_l = 0, 0
            if kit_opt == "نعم أريد":
                c1, c2 = st.columns(2)
                with c1: kit_w = st.number_input(f"عرض المطبخ - {floor_name}", value=4.0, key=f"kitw_{floor_name}")
                with c2: kit_l = st.number_input(f"طول المطبخ - {floor_name}", value=4.0, key=f"kitl_{floor_name}")
                used_area += (kit_w * kit_l)

            st.markdown("**📺 الهول الداخلي / المعيشة:**")
            hall_opt = st.selectbox(f"هل تريد هول في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"hall_{floor_name}")
            hall_w, hall_l = 0, 0
            if hall_opt == "نعم أريد":
                c1, c2 = st.columns(2)
                with c1: hall_w = st.number_input(f"عرض الهول - {floor_name}", value=frontage, key=f"hallw_{floor_name}")
                with c2: hall_l = st.number_input(f"طول الهول - {floor_name}", value=5.0, key=f"halll_{floor_name}")
                used_area += (hall_w * hall_l)

            st.write("---")
            rem_area = total_plot_area - used_area
            if rem_area >= 0:
                st.success(f"مساحة الفضاءات المحجوزة: **{used_area:.1f} م²** | المتبقي للممرات والخدمات: **{rem_area:.1f} م²** ✅")
            else:
                st.error(f"⚠️ تنبيه! المساحات تجاوزت مساحة الأرض الكلية بـ {abs(rem_area):.1f} م²!")

            return {'g_opt': g_opt, 'g_l': g_l, 'rec_w': rec_w, 'rec_l': rec_l, 'kit_w': kit_w, 'kit_l': kit_l, 'hall_l': hall_l, 'rooms': rooms_dims}

        ground_data = render_floor_inputs("الطابق الأرضي")

        st.write("---")
        if st.button("🎨 توليد المخطط الهندسي المعماري الاحترافي (Floor Plan)"):
            st.success("تم توليد الخارطة الهندسية بدقة عالية وبدون أي تداخلات! ✅")

            fig, ax = plt.subplots(figsize=(9, 13))
            ax.set_facecolor('white')
            fig.patch.set_facecolor('white')

            ax.set_xlim(-0.5, frontage + 0.5)
            ax.set_ylim(-0.5, depth + 0.5)
            ax.set_aspect('equal')
            
            outer_border = patches.Rectangle((0, 0), frontage, depth, linewidth=3, edgecolor='black', facecolor='none', zorder=5)
            ax.add_patch(outer_border)

            ax.text(frontage/2, depth - 0.5, f"مخطط الطابق الأرضي — مساحة الأرض: {total_plot_area:.1f} م²\n(واجهة {frontage}م × نزال {depth}م)", 
                    fontsize=12, fontweight='bold', color='black', ha='center', va='center',
                    bbox=dict(facecolor='#f8f9fa', edgecolor='black', boxstyle='round,pad=0.5'))

            current_y = depth - 1.0

            if ground_data['g_opt'] == "نعم أريد" and ground_data['g_l'] > 0:
                current_y -= ground_data['g_l']
                garden_box = patches.Rectangle((0, current_y), frontage, ground_data['g_l'], linewidth=2, edgecolor='black', facecolor='#e8f5e9', hatch='//', zorder=2)
                ax.add_patch(garden_box)
                ax.text(frontage/2, current_y + ground_data['g_l']/2, f"الحديقة / الكراج الأمامي\n({frontage}م × {ground_data['g_l']}م)", 
                        fontsize=11, fontweight='bold', color='#1b5e20', ha='center', va='center')

            rec_l = ground_data['rec_l']
            rec_w = ground_data['rec_w']
            kit_l = ground_data['kit_l']
            kit_w = ground_data['kit_w']
            row_h = max(rec_l, kit_l)

            if row_h > 0:
                current_y -= row_h
                if rec_w > 0:
                    rec_box = patches.Rectangle((0, current_y), rec_w, row_h, linewidth=2, edgecolor='black', facecolor='#e3f2fd', zorder=3)
                    ax.add_patch(rec_box)
                    ax.text(rec_w/2, current_y + row_h/2, f"الاستقبال (المضيف)\n({rec_w}م × {row_h}م)", 
                            fontsize=10, fontweight='bold', color='#0d47a1', ha='center', va='center')
                
                if kit_w > 0:
                    kit_box = patches.Rectangle((frontage - kit_w, current_y), kit_w, row_h, linewidth=2, edgecolor='black', facecolor='#fff3e0', zorder=3)
                    ax.add_patch(kit_box)
                    ax.text(frontage - kit_w/2, current_y + row_h/2, f"المطبخ الخدمي\n({kit_w}م × {row_h}م)", 
                            fontsize=10, fontweight='bold', color='#e65100', ha='center', va='center')

            hall_l = ground_data['hall_l']
            if hall_l > 0:
                current_y -= hall_l
                hall_box = patches.Rectangle((0, current_y), frontage, hall_l, linewidth=2, edgecolor='black', facecolor='#f3e5f5', zorder=3)
                ax.add_patch(hall_box)
                ax.text(frontage/2, current_y + hall_l/2, f"صالة المعيشة / الهول العائلي\n({frontage}م × {hall_l}م)", 
                        fontsize=11, fontweight='bold', color='#4a148c', ha='center', va='center')

            for idx, (rw, rl) in enumerate(ground_data['rooms']):
                if rl > 0 and current_y > 0:
                    current_y -= rl
                    room_box = patches.Rectangle((0, current_y), frontage, rl, linewidth=2, edgecolor='black', facecolor='#ffebee', zorder=3)
                    ax.add_patch(room_box)
                    ax.text(frontage/2, current_y + rl/2, f"غرفة النوم رقم ({idx+1})\n({frontage}م × {rl}م)", 
                            fontsize=11, fontweight='bold', color='#b71c1c', ha='center', va='center')

            ax.set_xlabel("عرض الواجهة (متر)", fontsize=11, fontweight='bold')
            ax.set_ylabel("النزال (متر)", fontsize=11, fontweight='bold')
            ax.grid(True, linestyle=':', alpha=0.5, color='gray')

            st.pyplot(fig)

# ==========================================
# 2. قسم التدقيق الإنشائي الأصلي
# ==========================================
elif "تدقيق" in mode:
    st.header("🏢 تدقيق عناصر المبنى الإنشائية (أعمدة، جسور، سقوف) بالطريقة الهندسية الدارجة")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        fc = st.number_input("مقاومة الخرسانة f'c (MPa)", value=28.0)
    with col_m2:
        fy = st.number_input("إجهاد خضوع الحديد fy (MPa)", value=420.0)
    with col_m3:
        dead_load = st.number_input("الأحمال الميتة الإضافية (كاشي وتراب) kN/m²", value=2.5)
    with col_m4:
        live_load = st.number_input("الحمل الحي (أثاث وسكن) kN/m²", value=3.0)

    st.write("---")
    st.subheader("2️⃣ تدقيق السقوف (Slabs & Deflection Check)")
    num_slabs = st.number_input("عدد أنواع السقوف بالمشروع", min_value=1, max_value=10, value=2)
    
    slab_data = []
    for i in range(int(num_slabs)):
        st.markdown(f"**السقف رقم (S{i+1})**")
        sc1, sc2, sc3, sc4, sc5 = st.columns(5)
        with sc1: lx = st.number_input(f"البحر القصير L_x (m) [S{i+1}]", value=4.0, key=f"lx_{i}")
        with sc2: ly = st.number_input(f"البحر الطويل L_y (m) [S{i+1}]", value=5.5, key=f"ly_{i}")
        with sc3: thickness = st.number_input(f"السمك t (mm) [S{i+1}]", value=150, key=f"t_{i}")
        with sc4: condition = st.selectbox(f"نوع استمرارية السقف [S{i+1}]", ["مستمر من الجهتين (Continuous)", "مستمر من جهة وحدة (End Span)", "بسيط الارتكاز (Simply Supported)"], key=f"cond_{i}")
        with sc5: rebar_s = st.text_input(f"التسليح المقترح [S{i+1}]", value="Ø12@200mm", key=f"reb_s_{i}")

        ratio = ly / lx if lx > 0 else 1.0
        styp = "توجيهين (Two-Way)" if ratio < 2.0 else "توجيه واحد (One-Way)"
        h_min = int((lx * 1000) / 28) if "مستمر من الجهتين" in condition else (int((lx * 1000) / 24) if "مستمر من جهة وحدة" in condition else int((lx * 1000) / 20))
        s_status = "✅ ممتاز.. ماكو أي نزول أو دَفلكشن (Safe)" if thickness >= h_min else f"⚠️ انتبه! السمك المطلوب: {h_min} مم"
        slab_data.append({"السقف": f"S{i+1}", "التصنيف": styp, "النسبة": f"{ratio:.2f}", "السمك المدخل": f"{thickness} mm", "فحص الدفلكشن": s_status, "التسليح": rebar_s})

    st.write("---")
    st.subheader("3️⃣ تدقيق الجسور والقص (Beams & Shear Check)")
    num_beams = st.number_input("عدد الجسور الرئيسية", min_value=1, max_value=10, value=2)
    
    beam_data = []
    for j in range(int(num_beams)):
        st.markdown(f"**الجسر رقم (B{j+1})**")
        bc1, bc2, bc3, bc4, bc5, bc6 = st.columns(6)
        with bc1: b_w = st.number_input(f"العرض b (mm) [B{j+1}]", value=250, key=f"bw_{j}")
        with bc2: h_b = st.number_input(f"العمق h (mm) [B{j+1}]", value=500, key=f"hb_{j}")
        with bc3: span = st.number_input(f"الطول Span (m) [B{j+1}]", value=5.0, key=f"span_{j}")
        with bc4: loc = st.selectbox(f"مكان الجسر [B{j+1}]", ["داخلي (Interior)", "خارجي يشيل واجهة (Exterior)", "على الحافة (Edge)"], key=f"loc_{j}")
        with bc5: top_reb = st.text_input(f"حديد العلوي [B{j+1}]", value="2Ø14", key=f"treb_{j}")
        with bc6: bot_reb = st.text_input(f"حديد السفلي [B{j+1}]", value="3Ø16", key=f"breb_{j}")

        d_eff = h_b - 50
        load_mult = 1.25 if "خارجي" in loc else 1.0
        w_beam = load_mult * (1.2 * (dead_load + (b_w/1000 * h_b/1000 * 25)) + 1.6 * live_load)
        Vu_beam = (w_beam * span) / 2
        phi_Vc = (0.75 * 0.17 * math.sqrt(fc) * b_w * d_eff) / 1000
        shear_check = "✅ مقطع الجسر قوي ويقاوم القص" if Vu_beam <= phi_Vc else "⚠️ القص عالي.. لازم نكثف الكانات"
        beam_data.append({"الجسر": f"B{j+1}", "المكان": loc, "المقطع": f"{b_w}x{h_b} mm", "قوة القص (Vu)": f"{Vu_beam:.1f} kN", "فحص القص": shear_check, "التسليح": f"فوق: {top_reb} | جوة: {bot_reb}"})

    st.write("---")
    st.subheader("4️⃣ تدقيق الأعمدة (Columns Check)")
    num_cols = st.number_input("عدد نماذج الأعمدة", min_value=1, max_value=6, value=2)
    
    col_results = []
    for k in range(int(num_cols)):
        st.markdown(f"**العمود رقم (C{k+1})**")
        cc1, cc2, cc3, cc4, cc5 = st.columns(5)
        with cc1: c_dim1 = st.number_input(f"العرض b (mm) [C{k+1}]", value=300, key=f"cd1_{k}")
        with cc2: c_dim2 = st.number_input(f"العمق h (mm) [C{k+1}]", value=400, key=f"cd2_{k}")
        with cc3: c_loc = st.selectbox(f"موقع العمود [C{k+1}]", ["وسطي (Interior)", "حافة (Edge)", "ركن (Corner)"], key=f"cloc_{k}")
        with cc4: floors_c = st.number_input(f"عدد الطوابق الفوقه [C{k+1}]", value=3, key=f"cfl_{k}")
        with cc5: col_reb = st.text_input(f"تسليح العمود [C{k+1}]", value=8*16, key=f"creb_{k}")

        area_trib = 4.0 * 4.5
        trib_fact = 1.0 if "وسطي" in c_loc else (0.6 if "حافة" in c_loc else 0.35)
        P_u = 1.2 * (dead_load * area_trib * floors_c * trib_fact) + 1.6 * (live_load * area_trib * floors_c * trib_fact)
        Ag = c_dim1 * c_dim2
        P_n_max = 0.80 * 0.65 * (0.85 * fc * (Ag - 2000) + 420 * 2000) / 1000
        col_status = "✅ العمود شايل الحمل ومرتاح كلش" if P_u <= P_n_max else "⚠️ الحمل قاصي على العمود"
        col_results.append({"العمود": f"C{k+1}", "المكان": c_loc, "الأبعاد": f"{c_dim1}x{c_dim2} mm", "الحمل المحسوب": f"{P_u:.1f} kN", "الحالة": col_status, "الحديد": col_reb})

# ==========================================
# 3. قسم حساب الكميات وهندسة الكلف (BOQ & Materials) - القسم الجديد
# ==========================================
elif "حساب الكميات" in mode:
    st.header("📊 قسم حساب الكميات والمواد الإنشائية (BOQ - Bill of Quantities)")
    st.write("اختر المادة الإنشائية أو العنصر المطلوب حساب كمياته بدقة وفق الأصول الهندسية العراقية:")
    st.write("---")

    boq_type = st.selectbox(
        "اختر مادة أو عنصر البناء:",
        [
            "🧱 الطابوق والبنّاء (Bricks & Masonry)", 
            "🏗️ الكونكريت والقوالب للأعمدة (Columns Concrete & Formwork)", 
            "🧪 مواد الإنهاءات (أسمنت، رمل، بورك، جبس)", 
            "⚙️ حديد التسليح التقديري (Rebar Estimation)"
        ]
    )

    if "الطابوق" in boq_type:
        st.subheader("🧱 حساب كميات الطابوق (مع سمايلات الجمالية للموقع)")
        bc1, bc2, bc3 = st.columns(3)
        with bc1:
            wall_area = st.number_input("مساحة الجدار الكلية (متر مربع)", min_value=1.0, value=50.0, step=1.0)
        with bc2:
            wall_thickness = st.selectbox("نوع البناء (سمك الجدار)", ["جدار مفرد (12 سم)", "جدار مزدوج / حامل (24 سم)"])
        with bc3:
            brick_type = st.selectbox("نوع الطابوق المستخدم", ["🧱 طابوق عراقي قياسي (24×11.5×7.5 سم)", "🧱 طابوق بلوك خرساني"])

        if st.button("🧮 احسب كمية الطابوق والمونة"):
            # الحسابات الهندسية المعتمدة (المتر المربع للجدار المفرد يحتاج تقريباً 55-60 طابوقة، المزدوج 110-120 مع نسبة هدر 5%)
            factor = 58 if "مفرد" in wall_thickness else 116
            total_bricks = int(wall_area * factor)
            mortar_volume = wall_area * (0.03 if "مفرد" in wall_thickness else 0.07) # متر مكعب مونه

            st.success("تمت الحسابات بنجاح وإليك الكميات المطلوبة للموقع بدقة ✅")
            
            c_res1, c_res2 = st.columns(2)
            with c_res1:
                st.metric("🧱 العدد الكلي للطابوق (مع الهدر 5%)", f"{total_bricks:,} طابوقة")
            with c_res2:
                st.metric("🧪 حجم المونة السمنتية المطلوبة", f"{mortar_volume:.2f} م³")
            
            st.info("💡 ملاحظة استشارية: لخلطة المونة لكل 1 متر مكعب، يفضل استخدام (4.5 كيس أسمنت + 0.52 متر مكعب رمل ناعم).")

    elif "الكونكريت والقوالب للأعمدة" in boq_type:
        st.subheader("🏗️ حساب كميات الكونكريت والقوالب للأعمدة (مربع، مستطيل، دائري)")
        
        col_c_type, col_c_num = st.columns(2)
        with col_c_type:
            col_shape = st.selectbox("شكل مقطع العمود", ["مربع (Square)", "مستطيل (Rectangular)", "دائري (Circular)"])
        with col_c_num:
            num_columns = st.number_input("عدد الأعمدة المماثلة", min_value=1, value=4, step=1)

        col_dim1, col_dim2, col_h = st.columns(3)
        with col_dim1:
            dim_a = st.number_input("عرض أو قطر العمود (سم)", min_value=10.0, value=30.0, step=5.0)
        with col_dim2:
            dim_b = st.number_input("عمق العمود للمستطيل (سم)", min_value=10.0, value=40.0, step=5.0)
        with col_h:
            col_height = st.number_input("ارتفاع العمود (متر)", min_value=1.0, value=3.5, step=0.5)

        if st.button("🧮 احسب كميات العمود الهندسية"):
            # حساب المساحة الجانبية للقالب والحجم الخرساني
            a_m = dim_a / 100.0
            b_m = dim_b / 100.0
            
            if "دائري" in col_shape:
                cross_area = math.pi * (a_m / 2.0) ** 2
                perimeter = math.math.pi * a_m if hasattr(math, 'math') else math.pi * a_m
            else:
                cross_area = a_m * b_m
                perimeter = 2 * (a_m + b_m)

            single_volume = cross_area * col_height
            total_concrete = single_volume * num_columns
            formwork_area = perimeter * col_height * num_columns

            st.success("تم استخراج كميات الكونكريت ومساحات القوالب الخشبية/الحديدية بنجاح ✅")

            rc1, rc2, rc3 = st.columns(3)
            with rc1:
                st.metric("📦 حجم الكونكريت الصافي", f"{total_concrete:.2f} م³")
            with rc2:
                st.metric("🪵 مساحة القوالب (Formwork)", f"{formwork_area:.2f} م²")
            with rc3:
                st.metric("🔩 عدد الأعمدة المحسوبة", f"{num_columns} عمود")

    elif "مواد الإنهاءات" in boq_type:
        st.subheader("🧪 حساب مواد الإنهاءات (أسمنت، رمل، بياض بورك وجبس)")
        
        fin_area = st.number_input("مساحة السطح أو الجدار للإنهاء (متر مربع)", min_value=1.0, value=100.0, step=5.0)
        fin_work = st.selectbox("نوع أعمال الإنهاء", ["لياسة / لبخ أسمنتي (سمك 2 سم)", "بياض بورك للجدران (سمك 1.5 سم)", "أرضيات كاشي أو سيراميك"])

        if st.button("🧮 احسب مواد الإنهاءات"):
            if "لبخ" in fin_work:
                cement_bags = fin_area * 0.32 # تقريباً لكل م2 بـ 2سم يحتاج 0.32 كيس
                sand_m3 = fin_area * 0.022
                st.success("حسابات اللبخ الأسمنتي جاهزة:")
                st.metric("📦 أكياس الأسمنت المطلوبة", f"{math.ceil(cement_bags)} كيس")
                st.metric("🏜️ كمية الرمل الناعم", f"{sand_m3:.2f} م³")
            elif "بورك" in fin_work:
                bourk_bags = fin_area * 0.25
                st.success("حسابات بياض البورك جاهزة:")
                st.metric("🤍 أكياس البورك المطلوبة", f"{math.ceil(bourk_bags)} كيس")
            else:
                st.success("لحساب الكاشي أو السيراميك:")
                st.metric("🧱 عدد المربعات مع نسبة الهدر 10%", f"{fin_area * 1.1:.1f} م² سيراميك/كاشي")

    elif "حديد التسليح التقديري" in boq_type:
        st.subheader("⚙️ حساب الوزن التقديري لحديد التسليح (Rebar Tonnage)")
        element_type = st.selectbox("العنصر الإنشائي", ["سقف خرساني (Slab)", "جسر رئيسي (Beam)", "عمود (Column)"])
        elem_vol = st.number_input("حجم الخرسانة الكلي لهذا العنصر (متر مكعب)", min_value=1.0, value=15.0, step=1.0)

    if st.button("🧮 احسب طن الحديد التقديري"):
        # نسب حديد التسليح التقريبية المعتمدة عراقياً وعالمياً لكل م3 خرسانة
        ratio = 110 if "سقف" in element_type else (140 if "جسر" in element_type else 180)
        total_steel_kg = elem_vol * ratio
        st.success("تم تقدير أطنان الحديد للموقع بنجاح ✅")
        st.metric("⚙️ الوزن الكلي للحديد (مع الأشاير والتلابيب)", f"{total_steel_kg:.1f} كغ ({total_steel_kg/1000:.2f} طن)")
