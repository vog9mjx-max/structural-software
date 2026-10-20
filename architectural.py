import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def render_architectural_design():
    st.header("🏡 قسم التصميم المعماري والتخطيط المرئي (2D Floor Plan)")
    st.write("---")

    # القسم الأول: مساحة الأرض وبناء الواجهة والنزال
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

    # القسم الثاني: تحديد الفضاءات الرئيسية للطابق الأرضي
    st.subheader("2️⃣ تحديد أبعاد الفضاءات المعمارية للطابق الأرضي")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("🔹 **الحديقة والكراج الأمامي:**")
        garden_depth = st.number_input("طول الحديقة/الكراج (متر)", value=5.0, step=0.5)
        
        st.markdown("🔹 **استقبال الضيوف (المضيف):**")
        rec_w = st.number_input("عرض الاستقبال (متر)", value=4.0, step=0.5)
        rec_l = st.number_input("طول الاستقبال (متر)", value=5.0, step=0.5)

        st.markdown("🔹 **المطبخ:**")
        kit_w = st.number_input("عرض المطبخ (متر)", value=4.0, step=0.5)
        kit_l = st.number_input("طول المطبخ (متر)", value=4.0, step=0.5)

    with col_f2:
        st.markdown("🔹 **الهول الداخلي (المعيشة):**")
        hall_w = st.number_input("عرض الهول (متر)", value=frontage, step=0.5)
        hall_l = st.number_input("طول الهول (متر)", value=6.0, step=0.5)

        st.markdown("🔹 **غرفة النوم الأرضية:**")
        room_w = st.number_input("عرض غرفة النوم (متر)", value=4.0, step=0.5)
        room_l = st.number_input("طول غرفة النوم (متر)", value=4.0, step=0.5)

    st.write("---")

    # زر توليد ورسم الخارطة الهندسية
    if st.button("🎨 توليد ورسم الخارطة الهندسية المعمارية (Generate Floor Plan)"):
        st.success("تم حساب الأبعاد وتوليد المخطط الهندسي بنجاح! ✅")

        # رسم الخريطة باستخدام Matplotlib
        fig, ax = plt.subplots(figsize=(8, 12))
        ax.set_xlim(0, frontage)
        ax.set_ylim(0, depth)
        ax.set_aspect('equal')
        ax.set_title(f"مخطط معماري مقترح - واجهة {frontage}م × نزال {depth}م", fontsize=14, fontweight='bold', pad=15)
        
        # رسم حدود قطعة الأرض الخارجية
        plot_boundary = patches.Rectangle((0, 0), frontage, depth, linewidth=3, edgecolor='black', facecolor='#fdfdfd', zorder=1)
        ax.add_patch(plot_boundary)

        # 1. رسم الحديقة / الكراج (في المقدمة y من depth-garden_depth إلى depth)
        garden_rect = patches.Rectangle((0, depth - garden_depth), frontage, garden_depth, linewidth=2, edgecolor='green', facecolor='#d4edda', alpha=0.7, zorder=2)
        ax.add_patch(garden_rect)
        ax.text(frontage/2, depth - garden_depth/2, f"الحديقة / الكراج\n({frontage}x{garden_depth}م)", color='darkgreen', fontsize=11, fontweight='bold', ha='center', va='center')

        # تتبع المؤشر للنزول تدريجياً من الأعلى للأسفل
        current_y = depth - garden_depth

        # 2. رسم الاستقبال والمطبخ على اليمين واليسار
        current_y -= max(rec_l, kit_l)
        rec_rect = patches.Rectangle((0, current_y), rec_w, rec_l, linewidth=2, edgecolor='blue', facecolor='#cce5ff', alpha=0.7, zorder=2)
        ax.add_patch(rec_rect)
        ax.text(rec_w/2, current_y + rec_l/2, f"الاستقبال\n({rec_w}x{rec_l}م)", color='darkblue', fontsize=10, fontweight='bold', ha='center', va='center')

        kit_rect = patches.Rectangle((frontage - kit_w, current_y), kit_w, kit_l, linewidth=2, edgecolor='orange', facecolor='#ffeeba', alpha=0.7, zorder=2)
        ax.add_patch(kit_rect)
        ax.text(frontage - kit_w/2, current_y + kit_l/2, f"المطبخ\n({kit_w}x{kit_l}م)", color='darkorange', fontsize=10, fontweight='bold', ha='center', va='center')

        # 3. رسم الهول الداخلي
        current_y -= hall_l
        hall_rect = patches.Rectangle((0, current_y), frontage, hall_l, linewidth=2, edgecolor='purple', facecolor='#e2d9f3', alpha=0.7, zorder=2)
        ax.add_patch(hall_rect)
        ax.text(frontage/2, current_y + hall_l/2, f"الهول الداخلي / المعيشة\n({frontage}x{hall_l}م)", color='purple', fontsize=11, fontweight='bold', ha='center', va='center')

        # 4. غرفة النوم في الخلف
        current_y -= room_l
        room_rect = patches.Rectangle((0, current_y), frontage, room_l, linewidth=2, edgecolor='brown', facecolor='#f5c6cb', alpha=0.7, zorder=2)
        ax.add_patch(room_rect)
        ax.text(frontage/2, current_y + room_l/2, f"غرفة النوم الرئيسية\n({frontage}x{room_l}م)", color='darkred', fontsize=11, fontweight='bold', ha='center', va='center')

        # إعدادات المحاور
        ax.set_xlabel("عرض الواجهة (متر)", fontsize=11)
        ax.set_ylabel("النزال (متر)", fontsize=11)
        ax.grid(True, linestyle='--', alpha=0.5)

        # عرض الرسم داخل ستاستريمت
        st.pyplot(fig)
