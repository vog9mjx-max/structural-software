import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
        
        def get_floor_data(floor_name):
            st.markdown(f"### 📍 فضاءات {floor_name}")
            floor_dict = {}
            used_area = 0.0

            # 1. الحديقة والكراج
            st.markdown("**🌳 الحديقة والكراج الأمامي:**")
            garden_opt = st.selectbox(f"هل تريد حديقة/كراج في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"g_opt_{floor_name}")
            g_w, g_l = 0, 0
            if garden_opt == "نعم أريد":
                cg1, cg2 = st.columns(2)
                with cg1:
                    g_w = st.number_input(f"عرض الحديقة (متر) - {floor_name}", value=frontage, key=f"gw_{floor_name}")
                with cg2:
                    g_l = st.number_input(f"طول الحديقة/النزال (متر) - {floor_name}", value=4.0, key=f"gl_{floor_name}")
                g_area = g_w * g_l
                used_area += g_area
                st.caption(f"مساحة الحديقة: {g_area:.1f} م²")
            floor_dict['garden'] = {'opt': garden_opt, 'w': g_w, 'l': g_l}

            # 2. غرف النوم
            st.markdown("**🛏️ غرف النوم:**")
            num_rooms = st.number_input(f"حدد عدد غرف النوم في {floor_name}", min_value=0, max_value=6, value=1, key=f"n_rooms_{floor_name}")
            rooms_list = []
            for r in range(int(num_rooms)):
                st.markdown(f"*غرفة نوم رقم ({r+1}):*")
                cr1, cr2 = st.columns(2)
                with cr1:
                    rw = st.number_input(f"عرض الغرفة {r+1} (متر)", value=4.0, key=f"rw_{floor_name}_{r}")
                with cr2:
                    rl = st.number_input(f"طول الغرفة {r+1} (متر)", value=5.0, key=f"rl_{floor_name}_{r}")
                r_area = rw * rl
                used_area += r_area
                rooms_list.append({'w': rw, 'l': rl})
                st.caption(f"مساحة الغرفة {r+1}: {r_area:.1f} م²")
            floor_dict['rooms'] = rooms_list

            # 3. الاستقبال
            st.markdown("**🛋️ الاستقبال (المضيف):**")
            rec_opt = st.selectbox(f"هل تريد استقبال في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"rec_opt_{floor_name}")
            rec_w, rec_l = 0, 0
            if rec_opt == "نعم أريد":
                cr1, cr2 = st.columns(2)
                with cr1:
                    rec_w = st.number_input(f"عرض الاستقبال (متر) - {floor_name}", value=4.0, key=f"recw_{floor_name}")
                with cr2:
                    rec_l = st.number_input(f"طول الاستقبال (متر) - {floor_name}", value=5.5, key=f"recl_{floor_name}")
                rec_area = rec_w * rec_l
                used_area += rec_area
                st.caption(f"مساحة الاستقبال: {rec_area:.1f} م²")
            floor_dict['reception'] = {'opt': rec_opt, 'w': rec_w, 'l': rec_l}

            # 4. المطبخ
            st.markdown("**🍳 المطبخ:**")
            kit_opt = st.selectbox(f"هل تريد مطبخ في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"kit_opt_{floor_name}")
            kit_w, kit_l = 0, 0
            if kit_opt == "نعم أريد":
                ck1, ck2 = st.columns(2)
                with ck1:
                    kit_w = st.number_input(f"عرض المطبخ (متر) - {floor_name}", value=3.5, key=f"kitw_{floor_name}")
                with ck2:
                    kit_l = st.number_input(f"طول المطبخ (متر) - {floor_name}", value=4.0, key=f"kitl_{floor_name}")
                kit_area = kit_w * kit_l
                used_area += kit_area
                st.caption(f"مساحة المطبخ: {kit_area:.1f} م²")
            floor_dict['kitchen'] = {'opt': kit_opt, 'w': kit_w, 'l': kit_l}

            # 5. الهول الداخلي
            st.markdown("**📺 الهول الداخلي / المعيشة:**")
            hall_opt = st.selectbox(f"هل تريد هول في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"hall_opt_{floor_name}")
            hall_w, hall_l = 0, 0
            if hall_opt == "نعم أريد":
                ch1, ch2 = st.columns(2)
                with ch1:
                    hall_w = st.number_input(f"عرض الهول (متر) - {floor_name}", value=4.0, key=f"hallw_{floor_name}")
                with ch2:
                    hall_l = st.number_input(f"طول الهول (متر) - {floor_name}", value=6.0, key=f"halll_{floor_name}")
                hall_area = hall_w * hall_l
                used_area += hall_area
                st.caption(f"مساحة الهول: {hall_area:.1f} م²")
            floor_dict['hall'] = {'opt': hall_opt, 'w': hall_w, 'l': hall_l}

            # 6. المناوير والتهوية
            st.markdown("**☀️ المنور والتهوية:**")
            shaft_opt = st.selectbox(f"هل تريد منور في {floor_name}؟", ["نعم أريد", "لا أريد"], key=f"sh_opt_{floor_name}")
            sh_w, sh_l = 0, 0
            if shaft_opt == "نعم أريد":
                cs1, cs2 = st.columns(2)
                with cs1:
                    sh_w = st.number_input(f"عرض المنور (متر) - {floor_name}", value=1.5, key=f"shw_{floor_name}")
                with cs2:
                    sh_l = st.number_input(f"طول المنور (متر) - {floor_name}", value=3.0, key=f"shl_{floor_name}")
                sh_area = sh_w * sh_l
                used_area += sh_area
                st.caption(f"مساحة المنور: {sh_area:.1f} م²")
            floor_dict['shaft'] = {'opt': shaft_opt, 'w': sh_w, 'l': sh_l}

            st.write("---")
            remaining_area = total_plot_area - used_area
            if remaining_area >= 0:
                st.success(f"مجموع المساحات الصافية المحجوزة في {floor_name}: **{used_area:.1f} م²** | المساحة المتبقية للممرات والخدمات: **{remaining_area:.1f} م²** ✅")
            else:
                st.error(f"⚠️ تنبيه! مجموع الفضاءات ({used_area:.1f} م²) تجاوز مساحة الأرض الكلية ({total_plot_area:.1f} م²) بـ {abs(remaining_area):.1f} م²!")

            return floor_dict

        # جلب بيانات الطابق الأرضي
        ground_data = get_floor_data("الطابق الأرضي")

        first_data = None
        if "نعم" in has_first_floor:
            st.write("---")
            first_data = get_floor_data("الطابق الأول")

        # زر توليد الخارطة الهندسية المرئية
        st.write("---")
        if st.button("🎨 توليد ورسم الخارطة الهندسية (2D Floor Plan)"):
            st.success("تم توليد المخطط الهندسي للطابق الأرضي بنجاح! ✅")

            fig, ax = plt.subplots(figsize=(8, 12))
            ax.set_xlim(0, frontage)
            ax.set_ylim(0, depth)
            ax.set_aspect('equal')
            ax.set_title(f"مخطط معماري مقترح - واجهة {frontage}م × نزال {depth}م", fontsize=14, fontweight='bold', pad=15)
            
            # حدود الأرض
            plot_boundary = patches.Rectangle((0, 0), frontage, depth, linewidth=3, edgecolor='black', facecolor='#fdfdfd', zorder=1)
            ax.add_patch(plot_boundary)

            current_y = depth
            
            # رسم الحديقة إذا وجدت
            if ground_data['garden']['opt'] == "نعم أريد":
                gw = frontage
                gl = ground_data['garden']['l']
                current_y -= gl
                garden_rect = patches.Rectangle((0, current_y), gw, gl, linewidth=2, edgecolor='green', facecolor='#d4edda', alpha=0.7, zorder=2)
                ax.add_patch(garden_rect)
                ax.text(frontage/2, current_y + gl/2, f"الحديقة / الكراج\n({gw}x{gl}م)", color='darkgreen', fontsize=10, fontweight='bold', ha='center', va='center')

            # رسم الاستقبال والمطبخ
            rec_w = ground_data['reception']['w'] if ground_data['reception']['opt'] == "نعم أريد" else 0
            rec_l = ground_data['reception']['l'] if ground_data['reception']['opt'] == "نعم أريد" else 0
            kit_w = ground_data['kitchen']['w'] if ground_data['kitchen']['opt'] == "نعم أريد" else 0
            kit_l = ground_data['kitchen']['l'] if ground_data['kitchen']['opt'] == "نعم أريد" else 0
            
            row_l = max(rec_l, kit_l)
            if row_l > 0:
                current_y -= row_l
                if rec_w > 0:
                    rec_rect = patches.Rectangle((0, current_y), rec_w, row_l, linewidth=2, edgecolor='blue', facecolor='#cce5ff', alpha=0.7, zorder=2)
                    ax.add_patch(rec_rect)
                    ax.text(rec_w/2, current_y + row_l/2, f"الاستقبال\n({rec_w}x{row_l}م)", color='darkblue', fontsize=9, fontweight='bold', ha='center', va='center')
                if kit_w > 0:
                    kit_rect = patches.Rectangle((frontage - kit_w, current_y), kit_w, row_l, linewidth=2, edgecolor='orange', facecolor='#ffeeba', alpha=0.7, zorder=2)
                    ax.add_patch(kit_rect)
                    ax.text(frontage - kit_w/2, current_y + row_l/2, f"المطبخ\n({kit_w}x{row_l}م)", color='darkorange', fontsize=9, fontweight='bold', ha='center', va='center')

            # رسم الهول الداخلي
            if ground_data['hall']['opt'] == "نعم أريد":
                hw = frontage
                hl = ground_data['hall']['l']
                current_y -= hl
                hall_rect = patches.Rectangle((0, current_y), hw, hl, linewidth=2, edgecolor='purple', facecolor='#e2d9f3', alpha=0.7, zorder=2)
                ax.add_patch(hall_rect)
                ax.text(hw/2, current_y + hl/2, f"الهول الداخلي\n({hw}x{hl}م)", color='purple', fontsize=10, fontweight='bold', ha='center', va='center')

            # رسم غرف النوم
            for idx, rm in enumerate(ground_data['rooms']):
                rw = frontage
                rl = rm['l']
                current_y -= rl
                room_rect = patches.Rectangle((0, current_y), rw, rl, linewidth=2, edgecolor='brown', facecolor='#f5c6cb', alpha=0.7, zorder=2)
                ax.add_patch(room_rect)
                ax.text(rw/2, current_y + rl/2, f"غرفة نوم ({idx+1})\n({rw}x{rl}م)", color='darkred', fontsize=10, fontweight='bold', ha='center', va='center')

            ax.set_xlabel("عرض الواجهة (متر)", fontsize=11)
            ax.set_ylabel("النزال (متر)", fontsize=11)
            ax.grid(True, linestyle='--', alpha=0.5)

            st.pyplot(fig)
