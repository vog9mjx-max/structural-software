import streamlit as st

def render_architectural_design():
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
        st.info(f"بناءً على مساحة أرضك ({total_plot_area:.1f} م²)، إليك عدة نماذج معمارية عراقية ممتازة وموزعة:")

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

        # تطبيق الإدخالات على الطابق الأرضي
        render_floor_inputs("الطابق الأرضي")

        # إذا اختار إضافة طابق أول
        if "نعم" in has_first_floor:
            st.write("---")
            render_floor_inputs("الطابق الأول")
