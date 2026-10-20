import streamlit as st
import math

st.set_page_config(page_title="المنظومة الهندسية الاستشارية المتكاملة", layout="wide")

st.title("🏛️ المنظومة الهندسية الاستشارية المتكاملة (معماري + إنشائي ACI 318)")
st.write("---")

# القائمة الجانبية للتنقل بين الأقسام
mode = st.sidebar.selectbox(
    "اختر قسم العمل المطلوب:", 
    ["🏡 التصميم المعماري وتوزيع المساحات", "🔍 تدقيق العناصر الإنشائية (عراقي)"]
)

# ==========================================
# 1. قسم التصميم المعماري
# ==========================================
if "المعماري" in mode:
    st.header("🏡 قسم التصميم المعماري وتوزيع الفضاءات")
    st.write("---")

    # القسم الأول: مساحة البناء الأفقية
    st.subheader("1️⃣ مساحة الأرض والبناء")
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        frontage = st.number_input("عرض الواجهة (متر)", min_value=3.0, value=10.0, step=0.5, key="arch_frontage")
    with col_a2:
        depth = st.number_input("النزال (متر)", min_value=5.0, value=20.0, step=0.5, key="arch_depth")
    
    total_plot_area = frontage * depth
    with col_a3:
        st.metric("مساحة قطعة الأرض الكلية", f"{total_plot_area:.1f} م²")

    st.write("---")

    # اختيار الطوابق
    st.subheader("2️⃣ تحديد الطوابق المطلوب تصميمها")
    has_first_floor = st.radio(
        "هل ترغب في إضافة تصميم للطابق الأول؟", 
        ["نعم، أضف الطابق الأول", "لا أريد (طابق أرضي فقط)"], 
        horizontal=True, 
        key="arch_has_first"
    )

    st.write("---")

    # القسم الثاني: أسلوب وتحديد التصميم
    st.subheader("3️⃣ خيارات أسلوب التصميم المعماري")
    design_choice = st.radio(
        "اختر طريقة تحديد الفضاءات المعمارية:",
        ["📐 اختيار من نماذج تصميم جاهزة ومقترحة", "✏️ أنا أحدد الفضاءات والمساحات بنفسي"],
        horizontal=True,
        key="arch_design_choice"
    )

    st.write("---")

    # حالة الخيار الأول: نماذج جاهزة
    if "نماذج" in design_choice:
        st.subheader("🎨 النماذج المعمارية المتاحة المقترحة")
        st.info(f"بناءً على مساحة أرضك ({total_plot_area:.1f} م²), إليك عدة نماذج معمارية عراقية ممتازة وموزعة:")

        st.markdown("""
        * **النموذج الأول (تصميم مفتوح Modern):**
          - استقبال مع ضيوف (5m × 4m)
          - هول داخلي مفتوح على المطبخ (6m × 4m)
          - مطبخ حار/بارد (4m × 3.5m)
          - غرفة نوم رئيسية ماستر (5m × 4m)
          - حديقة أماميّة كراج (5m × 4m) + مناوير جانبية وخلفية.

        * **النموذج الثاني (تصميم الخصوصية العائلية):**
          - استقبال معزول تماماً مع مدخل خاص (5.5m × 4m)
          - مطبخ منفصل مغلق (4m × 4m)
          - غرفتين نوم بالطابق الأرضي (كل غرفة 4m × 4m)
          - منور خلفي متصل بالخدمات (3m × 1.5m) + حديقة ومدخل سيارة.
        """)

    # حالة الخيار الثاني: المستخدم يحدد التفاصيل بنفسه
    else:
        st.subheader("✏️ تحديد الفضاءات والأبعاد بلمستك الخاصة")
        
        def render_floor_inputs(floor_name):
            st.markdown(f"### 📍 فضاءات {floor_name}")
            used_area = 0.0

            # 1. الحديقة والكراج
            st.markdown("**🌳 الحديقة والكراج الأمامي:**")
            garden_opt = st.selectbox(f"هل تريد حديقة/كراج في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"g_opt_{floor_name}")
            if garden_opt == "نعم أريد":
                cg1, cg2 = st.columns(2)
                with cg1:
                    g_w = st.number_input(f"عرض الحديقة (متر) - {floor_name}", value=frontage, key=f"gw_{floor_name}")
                with cg2:
                    g_l = st.number_input(f"طول الحديقة/النزال (متر) - {floor_name}", value=4.0, key=f"gl_{floor_name}")
                g_area = g_w * g_l
                used_area += g_area
                st.caption(f"مساحة الحديقة: {g_area:.1f} م²")

            # 2. غرف النوم
            st.markdown("**🛏️ غرف النوم:**")
            num_rooms = st.number_input(f"حدد عدد غرف النوم في {floor_name}", min_value=0, max_value=6, value=1, key=f"n_rooms_{floor_name}")
            
            for r in range(int(num_rooms)):
                st.markdown(f"*غرفة نوم رقم ({r+1}):*")
                cr1, cr2 = st.columns(2)
                with cr1:
                    rw = st.number_input(f"عرض الغرفة {r+1} (متر)", value=4.0, key=f"rw_{floor_name}_{r}")
                with cr2:
                    rl = st.number_input(f"طول الغرفة {r+1} (متر)", value=5.0, key=f"rl_{floor_name}_{r}")
                r_area = rw * rl
                used_area += r_area
                st.caption(f"مساحة الغرفة {r+1}: {r_area:.1f} م²")

            # 3. الاستقبال
            st.markdown("**🛋️ الاستقبال (المضيف):**")
            rec_opt = st.selectbox(f"هل تريد استقبال في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"rec_opt_{floor_name}")
            if rec_opt == "نعم أريد":
                cr1, cr2 = st.columns(2)
                with cr1:
                    rec_w = st.number_input(f"عرض الاستقبال (متر) - {floor_name}", value=4.0, key=f"recw_{floor_name}")
                with cr2:
                    rec_l = st.number_input(f"طول الاستقبال (متر) - {floor_name}", value=5.5, key=f"recl_{floor_name}")
                rec_area = rec_w * rec_l
                used_area += rec_area
                st.caption(f"مساحة الاستقبال: {rec_area:.1f} م²")

            # 4. المطبخ
            st.markdown("**🍳 المطبخ:**")
            kit_opt = st.selectbox(f"هل تريد مطبخ في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"kit_opt_{floor_name}")
            if kit_opt == "نعم أريد":
                ck1, ck2 = st.columns(2)
                with ck1:
                    kit_w = st.number_input(f"عرض المطبخ (متر) - {floor_name}", value=3.5, key=f"kitw_{floor_name}")
                with ck2:
                    kit_l = st.number_input(f"طول المطبخ (متر) - {floor_name}", value=4.0, key=f"kitl_{floor_name}")
                kit_area = kit_w * kit_l
                used_area += kit_area
                st.caption(f"مساحة المطبخ: {kit_area:.1f} م²")

            # 5. الهول الداخلي
            st.markdown("**📺 الهول الداخلي / المعيشة:**")
            hall_opt = st.selectbox(f"هل تريد هول في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"hall_opt_{floor_name}")
            if hall_opt == "نعم أريد":
                ch1, ch2 = st.columns(2)
                with ch1:
                    hall_w = st.number_input(f"عرض الهول (متر) - {floor_name}", value=4.0, key=f"hallw_{floor_name}")
                with ch2:
                    hall_l = st.number_input(f"طول الهول (متر) - {floor_name}", value=6.0, key=f"halll_{floor_name}")
                hall_area = hall_w * hall_l
                used_area += hall_area
                st.caption(f"مساحة الهول: {hall_area:.1f} م²")

            # 6. المناوير والتهوية
            st.markdown("**☀️ المنور والتهوية:**")
            shaft_opt = st.selectbox(f"هل تريد منور في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"sh_opt_{floor_name}")
            if shaft_opt == "نعم أريد":
                cs1, cs2 = st.columns(2)
                with cs1:
                    sh_w = st.number_input(f"عرض المنور (متر) - {floor_name}", value=1.5, key=f"shw_{floor_name}")
                with cs2:
                    sh_l = st.number_input(f"طول المنور (متر) - {floor_name}", value=3.0, key=f"shl_{floor_name}")
                sh_area = sh_w * sh_l
                used_area += sh_area
                st.caption(f"مساحة المنور: {sh_area:.1f} م²")

            # تدقيق ومراعاة المساحات
            st.write("---")
            remaining_area = total_plot_area - used_area
            if remaining_area >= 0:
                st.success(f"مجموع المساحات الصافية المحجوزة في {floor_name}: **{used_area:.1f} م²** | المساحة المتبقية للممرات والخدمات: **{remaining_area:.1f} م²** ✅")
            else:
                st.error(f"⚠️ تنبيه! مجموع الفضاءات ({used_area:.1f} م²) تجاوز مساحة الأرض الكلية ({total_plot_area:.1f} م²) بـ {abs(remaining_area):.1f} م²! يرجى تقليل أبعاد بعض الغرف.")

        render_floor_inputs("الطابق الأرضي")

        if "نعم" in has_first_floor:
            st.write("---")
            render_floor_inputs("الطابق الأول")

# ==========================================
# 2. قسم التدقيق الإنشائي الأصلي (كما هو تماماً)
# ==========================================
elif "تدقيق" in mode:
    st.header("🏢 تدقيق عناصر المبنى الإنشائية (أعمدة، جسور، سقوف) بالطريقة الهندسية الدارجة")

    st.subheader("1️⃣ مواصفات المواد والأحمال بالموقع")
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
        with sc1:
            lx = st.number_input(f"البحر القصير L_x (m) [S{i+1}]", value=4.0, key=f"lx_{i}")
        with sc2:
            ly = st.number_input(f"البحر الطويل L_y (m) [S{i+1}]", value=5.5, key=f"ly_{i}")
        with sc3:
            thickness = st.number_input(f"السمك t (mm) [S{i+1}]", value=150, key=f"t_{i}")
        with sc4:
            condition = st.selectbox(f"نوع استمرارية السقف [S{i+1}]", ["مستمر من الجهتين (Continuous)", "مستمر من جهة وحدة (End Span)", "بسيط الارتكاز (Simply Supported)"], key=f"cond_{i}")
        with sc5:
            rebar_s = st.text_input(f"التسليح المقترح [S{i+1}]", value="Ø12@200mm", key=f"reb_s_{i}")

        ratio = ly / lx if lx > 0 else 1.0
        styp = "توجيهين (Two-Way)" if ratio < 2.0 else "توجيه واحد (One-Way)"
        
        if "مستمر من الجهتين" in condition:
            h_min = int((lx * 1000) / 28)
        elif "مستمر من جهة وحدة" in condition:
            h_min = int((lx * 1000) / 24)
        else:
            h_min = int((lx * 1000) / 20)

        if thickness >= h_min:
            s_status = "✅ ممتاز.. ماكو أي نزول أو دَفلكشن (Safe)"
        else:
            s_status = f"⚠️ انتبه! السقف خفيف ويحتمل يصير بيه دَفلكشن (السمك المطلوب: {h_min} مم)"

        slab_data.append({"السقف": f"S{i+1}", "التصنيف": styp, "النسبة": f"{ratio:.2f}", "السمك المدخل": f"{thickness} mm", "فحص الدفلكشن": s_status, "التسليح": rebar_s})

    st.write("---")

    st.subheader("3️⃣ تدقيق الجسور والقص (Beams & Shear Check)")
    num_beams = st.number_input("عدد الجسور الرئيسية", min_value=1, max_value=10, value=2)
    
    beam_data = []
    for j in range(int(num_beams)):
        st.markdown(f"**الجسر رقم (B{j+1})**")
        bc1, bc2, bc3, bc4, bc5, bc6 = st.columns(6)
        with bc1:
            b_w = st.number_input(f"العرض b (mm) [B{j+1}]", value=250, key=f"bw_{j}")
        with bc2:
            h_b = st.number_input(f"العمق h (mm) [B{j+1}]", value=500, key=f"hb_{j}")
        with bc3:
            span = st.number_input(f"الطول Span (m) [B{j+1}]", value=5.0, key=f"span_{j}")
        with bc4:
            loc = st.selectbox(f"مكان الجسر [B{j+1}]", ["داخلي (Interior)", "خارجي يشيل واجهة (Exterior)", "على الحافة (Edge)"], key=f"loc_{j}")
        with bc5:
            top_reb = st.text_input(f"حديد العلوي [B{j+1}]", value="2Ø14", key=f"treb_{j}")
        with bc6:
            bot_reb = st.text_input(f"حديد السفلي [B{j+1}]", value="3Ø16", key=f"breb_{j}")

        d_eff = h_b - 50
        load_mult = 1.25 if "خارجي" in loc else 1.0
        w_beam = load_mult * (1.2 * (dead_load + (b_w/1000 * h_b/1000 * 25)) + 1.6 * live_load)
        Vu_beam = (w_beam * span) / 2
        phi_Vc = (0.75 * 0.17 * math.sqrt(fc) * b_w * d_eff) / 1000

        if Vu_beam <= phi_Vc:
            shear_check = "✅ مقطع الجسر قوي ويقاوم القص وحددنا الكانات للربط وبس"
        else:
            shear_check = "⚠️ القص عالي.. لازم نكثف الكانات أو نكبر مقطع الجسر"

        beam_data.append({"الجسر": f"B{j+1}", "المكان": loc, "المقطع": f"{b_w}x{h_b} mm", "قوة القص (Vu)": f"{Vu_beam:.1f} kN", "فحص القص": shear_check, "التسليح": f"فوق: {top_reb} | جوة: {bot_reb}"})

    st.write("---")

    st.subheader("4️⃣ تدقيق الأعمدة (Columns Check)")
    num_cols = st.number_input("عدد نماذج الأعمدة", min_value=1, max_value=6, value=2)
    
    col_results = []
    for k in range(int(num_cols)):
        st.markdown(f"**العمود رقم (C{k+1})**")
        cc1, cc2, cc3, cc4, cc5 = st.columns(5)
        with cc1:
            c_dim1 = st.number_input(f"العرض b (mm) [C{k+1}]", value=300, key=f"cd1_{k}")
        with cc2:
            c_dim2 = st.number_input(f"العمق h (mm) [C{k+1}]", value=400, key=f"cd2_{k}")
        with cc3:
            c_loc = st.selectbox(f"موقع العمود [C{k+1}]", ["وسطي (Interior)", "حافة (Edge)", "ركن (Corner)"], key=f"cloc_{k}")
        with cc4:
            floors_c = st.number_input(f"عدد الطوابق الفوقه [C{k+1}]", value=3, key=f"cfl_{k}")
        with cc5:
            col_reb = st.text_input(f"تسليح العمود [C{k+1}]", value="8Ø16", key=f"creb_{k}")

        area_trib = 4.0 * 4.5
        trib_fact = 1.0 if "وسطي" in c_loc else (0.6 if "حافة" in c_loc else 0.35)
        P_u = 1.2 * (dead_load * area_trib * floors_c * trib_fact) + 1.6 * (live_load * area_trib * floors_c * trib_fact)
        
        Ag = c_dim1 * c_dim2
        P_n_max = 0.80 * 0.65 * (0.85 * fc * (Ag - 2000) + 420 * 2000) / 1000
        
        if P_u <= P_n_max:
            col_status = "✅ العمود شايل الحمل ومرتاح كلش"
        else:
            col_status = "⚠️ الحمل قاصي على العمود، لازم نكبر أبعاده"

        col_results.append({"العمود": f"C{k+1}", "المكان": c_loc, "الأبعاد": f"{c_dim1}x{c_dim2} mm", "الحمل المحسوب": f"{P_u:.1f} kN", "الحالة": col_status, "الحديد": col_reb})

    st.write("---")
    if st.button("📋 اعرض التقرير النهائي والتوصيات الاقتصادية"):
        st.success("تم التدقيق بنجاح واستخراج التوصيات الاقتصادية للمشروع ✅")
        
        st.subheader("📊 الخلاصة التنفيذية للمشروع")
        st.markdown("### 🔹 السقوف والترخيم:")
        st.table(slab_data)

        st.markdown("### 🔹 الجسور والقص:")
        st.table(beam_data)

        st.markdown("### 🔹 الأعمدة والأحمال:")
        st.table(col_results)

        st.write("---")
        st.subheader("💡 التوصيات الاقتصادية وهندسة القيمة (Value Engineering)")
        st.info("""
        **🔍 ملحوظات وتحليلات المقاول والاستشاري لتوفير الكلفة:**
        1. **السقوف:** زيادة سمك السقف بمقدار 10 مم يسمح ببدائل تسليح أقل كثافة، مما يعطي اقتصادية ممتازة في أطنان حديد التسليح.
        2. **الجسور:** الاعتماد على مقاطع 250×500 مم يغطي متطلبات القص والعزم لمعظم البحور الاعتيادية دون حاجة لحديد إضافي مبالغ فيه.
        3. **الأعمدة:** الحفاظ على الأبعاد الحالية مع توزيع التسليح المتناظر يمنع أي عزم إضافي ناتج عن الترحيل (Eccentricity).
        """)
