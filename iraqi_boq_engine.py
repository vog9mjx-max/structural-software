class IraqiBOQEngine:
    def __init__(self, concrete_price_iqd=110000, steel_price_iqd=1050000):
        """
        محرك حصر الكميات والتسليح المخصص للسوق العراقي
        :param concrete_price_iqd: سعر المتر المكعب للخرسانة الجاهزة بالدينار العراقي (افتراضي: 110,000 د.ع)
        :param steel_price_iqd: سعر طن حديد التسليح بالدينار العراقي (افتراضي: 1,050,000 د.ع)
        """
        self.concrete_price = concrete_price_iqd
        self.steel_price = steel_price_iqd

    def calculate_project_cost(self, total_concrete_m3, total_steel_tons):
        """
        حساب التكلفة الإجمالية للخرسانة والحديد بالدينار العراقي
        """
        concrete_cost = total_concrete_m3 * self.concrete_price
        steel_cost = total_steel_tons * self.steel_price
        total_cost = concrete_cost + steel_cost

        return {
            "concrete_volume_m3": total_concrete_m3,
            "concrete_cost_iqd": concrete_cost,
            "steel_weight_tons": total_steel_tons,
            "steel_cost_iqd": steel_cost,
            "total_cost_iqd": total_cost
        }

    def print_boq_report(self, total_concrete_m3, total_steel_tons):
        results = self.calculate_project_cost(total_concrete_m3, total_steel_tons)
        
        print("\n" + "=" * 60)
        print("         جدول الكميات والتخمين المالي (السوق العراقي)")
        print("=" * 60)
        print(f"1. كمية الخرسانة المسلحة  : {results['concrete_volume_m3']:.2f} م³")
        print(f"   تكلفة الخرسانة         : {results['concrete_cost_iqd']:,.0f} دينار عراقي")
        print("-" * 60)
        print(f"2. كمية حديد التسليح       : {results['steel_weight_tons']:.2f} طن")
        print(f"   تكلفة حديد التسليح     : {results['steel_cost_iqd']:,.0f} دينار عراقي")
        print("=" * 60)
        print(f"التكلفة الإجمالية التقديرية: {results['total_cost_iqd']:,.0f} دينار عراقي")
        print("=" * 60 + "\n")