import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

st.set_page_config(page_title="المنظومة الهندسية الاستشارية المتكاملة", layout="wide")

st.title("🏛️ المنظومة الهندسية الاستشارية المتكاملة (معماري هندسي + إنشائي ACI 318)")
st.write("---")

# القائمة الجانبية للتنقل بين الأقسام
mode = st.sidebar.selectbox(
    "اختر قسم العمل المطلوب:", 
    ["🏡 التصميم المعماري ورسم الخرائط الهندسية", "🔍 تدقيق العناصر الإنشائية (عراقي)"]
)

# ==========================================
# 1. قسم التصميم المعماري ورسم المخطط الهندسي
# ==========================================
if "المعماري" in mode:
    st.header("🏡 قسم التصميم المعماري وتوليد المخططات الهندسية (AutoCAD Style)")
    st.write("---")

    # مساحة الأرض
    st.subheader("1️⃣ مساحة الأرض والأبعاد الكلية")
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        frontage = st.number_input("عرض الواجهة (متر)", min_value=4.0, value=10.0, step=0.5, key="arch_frontage")
    with col_a2:
        depth = st.number_input("النزال (متر)", min_value=6.0, value=20.0, step=0.5, key="arch_depth")
    
    total_plot_area = frontage * depth
    with col_a3:
        st.metric("مساحة قطعة الأرض الكلية", f"{total_plot_area:.1f} م²")

    st.write("---")

    # تحديد الفضاءات للطابق الأرضي
    st.subheader("2️⃣ تحديد أبعاد الفضاءات المعمارية للطابق الأرضي")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("🔹 **الحديقة والكراج الأمامي:**")
        garden_depth = st.number_input("طول الحديقة/الكراج (متر)", value=5.0, step=0.5)
        
        st.markdown("🔹 **الاستقبال (الصاحون / المضيف):**")
        rec_w = st.number_input("عرض الاستقبال (متر)", value=4.0, step=0.5)
        rec_l = st.number_input("طول الاستقبال (متر)", value=5.0, step=0.5)

        st.markdown("🔹 **المطبخ:**")
        kit_w = st.number_input("عرض المطبخ (متر)", value=4.0, step=0.5)
        kit_l = st.number_input("طول المطبخ (متر)", value=4.0, step=0.5)

    with col_f2:
        st.markdown("🔹 **صالة المعيشة (الهول الداخلي):**")
        hall_w = st.number_input("عرض الهول (متر)", value=frontage, step=0.5)
        hall_l = st.number_input("طول الهول (متر)", value=6.0, step=0.5)

        st.markdown("🔹 **غرفة النوم الرئيسية:**")
        room_w = st.number_input("عرض غرفة النوم (متر)", value=4.0, step=0.5)
        room_l = st.number_input("طول غرفة النوم (متر)", value=4.0, step=0.5)

    st.write("---")

    # زر توليد الخارطة الهندسية النمطية
    if st.button("📐 توليد المخطط الهندسي المعماري المعتمد"):
        st.success("تم توليد الخارطة الهندسية بالأسلوب المعماري الدقيق بنجاح! ✅")

        # إعداد لوحة الرسم بنمط مخطط هندسي (Blueprint / Architectural Drawing)
        fig, ax = plt.subplots(figsize=(9, 13))
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        
        ax.set_xlim(-0.5, frontage + 0.5)
        ax.set_ylim(-0.5, depth + 0.5)
        ax.set_aspect('equal')
        
        # العنوان الهندسي
        ax.set_title(f"المخطط المعماري للطابق الأرضي — مساحة الأرض: {total_plot_area:.1f} م²\n(واجهة {frontage}م × نزال {depth}م)", 
                     fontsize=13, fontweight='bold', color='black', pad=20)
        
        # رسم حدود الجدران الخارجية بlines سميكة وسوداء
        outer_wall = patches.Rectangle((0, 0), frontage, depth, linewidth=3.5, edgecolor='black', facecolor='none', zorder=5)
        ax.add_patch(outer_wall)

        current_y = depth

        # 1. الحديقة والكراج الأمامي
        if garden_depth > 0:
            current_y -= garden_depth
            garden_box = patches.Rectangle((0, current_y), frontage, garden_depth, linewidth=2, edgecolor='black', facecolor='#f8f9fa', hatch='//', zorder=2)
            ax.add_patch(garden_box)
            ax.text(frontage/2, current_y + garden_depth/2, f"الحديقة / الكراج\n({frontage}م × {garden_depth}م)", 
                    fontsize=11, fontweight='bold', color='black', ha='center', va='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

        # 2. الاستقبال والمطبخ (صف واحد متناسق)
        row_l = max(rec_l, kit_l)
        current_y -= row_l
        if rec_w > 0 and row_l > 0:
            rec_box = patches.Rectangle((0, current_y), rec_w, row_l, linewidth=2, edgecolor='black', facecolor='white', zorder=3)
            ax.add_patch(rec_box)
            ax.text(rec_w/2, current_y + row_l/2, f"استقبال / صالون\n({rec_w}م × {row_l}م)", 
                    fontsize=10, fontweight='bold', color='black', ha='center', va='center')
            
        if kit_w > 0 and row_l > 0:
            kit_box = patches.Rectangle((frontage - kit_w, current_y), kit_w, row_l, linewidth=2, edgecolor='black', facecolor='white', zorder=3)
            ax.add_patch(kit_box)
            ax.text(frontage - kit_w/2, current_y + row_l/2, f"مطبخ\n({kit_w}م × {row_l}م)", 
                    fontsize=10, fontweight='bold', color='black', ha='center', va='center')

        # 3. صالة المعيشة (الهول الداخلي)
        if hall_l > 0:
            current_y -= hall_l
            hall_box = patches.Rectangle((0, current_y), frontage, hall_l, linewidth=2, edgecolor='black', facecolor='white', zorder=3)
            ax.add_patch(hall_box)
            ax.text(frontage/2, current_y + hall_l/2, f"صالة المعيشة / الهول\n({frontage}م × {hall_l}م)", 
                    fontsize=11, fontweight='bold', color='black', ha='center', va='center')

        # 4. غرفة النوم الرئيسية في الخلف
        if room_l > 0:
            current_y -= room_l
            room_box = patches.Rectangle((0, current_y), frontage, room_l, linewidth=2, edgecolor='black', facecolor='white', zorder=3)
            ax.add_patch(room_box)
            ax.text(frontage/2, current_y + room_l/2, f"غرفة النوم الرئيسية\n({frontage}م × {room_l}م)", 
                    fontsize=11, fontweight='bold', color='black', ha='center', va='center')

        # ضبط إطارات ورسومات المحاور لتكون بنمط الهندسة المدنية
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        ax.set_xlabel("عرض الواجهة (متر)", fontsize=11, fontweight='bold')
        ax.set_ylabel("النزال (متر)", fontsize=11, fontweight='bold')
        ax.grid(True, linestyle=':', alpha=0.6, color='gray')

        st.pyplot(fig)

# ==========================================
# 2. قسم التدقيق الإنشائي الأصلي
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
