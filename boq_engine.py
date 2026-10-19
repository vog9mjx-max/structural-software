# boq_engine.py
# محرك حصر الكميات والتكلفة التقديرية حسب السوق العراقي

class BOQEngine:
    # أسعار السوق العراقي القياسية (بالدينار العراقي IQD)
    STEEL_PRICE_PER_TON_IQD = 1025000  # طن حديد التسليح شامل الفاقد والتوريد
    CONCRETE_PRICE_PER_M3_IQD = 105000  # متر مكعب خرسانة جاهزة مع البمب
    LABOR_PRICE_PER_M3_IQD = 45000      # أجور النجارة والحدادة والصب للمتر المكعب
    STEEL_DENSITY_KG_M3 = 7850          # كثافة حديد التسليح (كجم/م3)

    @classmethod
    def calculate_building_boq(cls, concrete_volume_m3, steel_volume_m3):
        """
        حساب أوزان الحديد، أحجام الخرسانة، والتكلفة الإجمالية بالدينار العراقي
        """
        # حساب أوزان الحديد بالطن
        steel_weight_kg = steel_volume_m3 * cls.STEEL_DENSITY_KG_M3
        steel_weight_tons = steel_weight_kg / 1000.0
        
        # إضافة نسبة فاقد (Wastage) بنسبة 5% للحديد و3% للخرسانة
        steel_weight_tons_with_waste = steel_weight_tons * 1.05
        concrete_volume_with_waste = concrete_volume_m3 * 1.03

        # حساب التكاليف
        cost_steel = steel_weight_tons_with_waste * cls.STEEL_PRICE_PER_TON_IQD
        cost_concrete = concrete_volume_with_waste * cls.CONCRETE_PRICE_PER_M3_IQD
        cost_labor = concrete_volume_with_waste * cls.LABOR_PRICE_PER_M3_IQD

        total_cost_iqd = cost_steel + cost_concrete + cost_labor

        # طباعة تقرير الكميات باللغة العربية والتفصيل العراقي
        print("\n" + "="*55)
        print("    جدول حصر الكميات والتكلفة التقديرية (السوق العراقي)    ")
        print("="*55)
        print(f"1. الحجم الكلي للخرسانة المسلحة : {concrete_volume_with_waste:.2f} m³ (شامل الهالك 3%)")
        print(f"2. الوزن الكلي لحديد التسليح  : {steel_weight_tons_with_waste:.2f} Ton (شامل الفاقد 5%)")
        print("-"*55)
        print(f" - تكلفة حديد التسليح الكلية   : {cost_steel:,.0f} IQD")
        print(f" - تكلفة الخرسانة الجاهزة (بمب) : {cost_concrete:,.0f} IQD")
        print(f" - أجور العمل والمصنعيات (نجارة/حدادة): {cost_labor:,.0f} IQD")
        print("="*55)
        print(f" إجمالي التكلفة التقديرية للمبنى: {total_cost_iqd:,.0f} دينار عراقي")
        print("="*55 + "\n")

        return {
            "concrete_volume_m3": concrete_volume_with_waste,
            "steel_weight_tons": steel_weight_tons_with_waste,
            "total_cost_iqd": total_cost_iqd
        }