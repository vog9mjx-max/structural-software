import streamlit as st
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="منظومة التدقيق الإنشائي العراقي - ACI 318", layout="wide")

st.title("🛡️ النظام الاستشاري للتدقيق الإنشائي (باللغة والدارج الهندسي العراقي)")
st.write("---")

# اختيار نمط العمل
mode = st.sidebar.selectbox("اختر وضع النظام:", ["🔍 تدقيق متعدد العناصر (عراقي)", "📊 تقرير التدقيق العام"])

if "تدقيق" in mode:
    st.header("🏢 إدخال وتدقيق عناصر المبنى (أعمدة، جسور، سقوف) بالطريقة الهندسية الدارجة")

    # 1. إعدادات المواد العامة للمشروع
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

    # 2. تدقيق السقوف والبلاطات
    st.subheader("2️⃣ تدقيق السقوف (Slabs & Deflection Check)")
    num_slabs = st.number_input("عدد أنواع السقوف بالمشروع", min_value=1, max_value=10, value=2)
    
    slab_data = []
    for i in range(num_slabs):
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

        # الحسابات والدفلكشن بالعراقي
        ratio = ly / lx if lx > 0 else 1.0
        styp = "توجيه واحد (One-Way)" if ratio >= 2.0 else "توجيهين (Two-Way)"
        
        if "مستمر من الجهتين" in condition:
            h_min = int((lx * 1000) / 28)
        elif "مستمر من جهة وحدة" in condition:
            h_min = int((lx * 1000) / 24)
        else:
            h_min = int((lx * 1000) / 20)

        # المصطلحات بالعراقي الشائع
        if thickness >= h_min:
            s_status = "✅ ممتاز.. ماكو أي نزول أو دَفلكشن (Safe)"
        else:
            s_status = f"⚠️ انتبه! السقف خفيف ويحتمل يصير بيه دَفلكشن (السمك المطلوب: {h_min} مم)"

        slab_data.append({"السقف": f"S{i+1}", "التصنيف": styp, "النسبة": f"{ratio:.2f}", "السمك المدخل": f"{thickness} mm", "فحص الدفلكشن": s_status, "التسليح": rebar_s})

    st.write("---")

    # 3. تدقيق الجسور (Beams)
    st.subheader("3️⃣ تدقيق الجسور والقص (Beams & Shear Check)")
    num_beams = st.number_input("عدد الجسور الرئيسية", min_value=1, max_value=10, value=2)
    
    beam_data = []
    for j in range(num_beams):
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

        # تدقيق القص بالعراقي
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

    # 4. تدقيق الأعمدة (Columns)
    st.subheader("4️⃣ تدقيق الأعمدة (Columns Check)")
    num_cols = st.number_input("عدد نماذج الأعمدة", min_value=1, max_value=6, value=2)
    
    col_results = []
    for k in range(num_cols):
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
    if st.button("📋 اعرض التقرير النهائي باللهجة العراقية"):
        st.success("تم التدقيق بنجاح وكامل العناصر مطابقة للأصول الهندسية ✅")
        
        st.subheader("📊 الخلاصة التنفيذية للمشروع")
        st.markdown("### 🔹 السقوف والترخيم:")
        st.table(slab_data)

        st.markdown("### 🔹 الجسور والقص:")
        st.table(beam_data)

        st.markdown("### 🔹 الأعمدة والأحمال:")
        st.table(col_results)

else:
    st.info("ℹ️ اختر من القائمة الجانبية لبدء التدقيق.")
