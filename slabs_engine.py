import math

class SlabEngine:
    def __init__(self, fc=28, fy=420):
        self.fc = fc
        self.fy = fy

    def design_one_way_slab(self, span, dead_load_extra=2.5, live_load=2.0):
        # حساب سمك البلاطة الأدنى وفق ACI 318
        min_thickness = (span * 1000) / 20.0
        thickness = max(120, math.ceil(min_thickness / 10.0) * 10)
        
        # أوزان الأحمال
        self_weight = (thickness / 1000.0) * 24.0  # kN/m2
        total_dead = self_weight + dead_load_extra
        qu = 1.2 * total_dead + 1.6 * live_load
        
        # حساب العزم
        mu = (qu * (span ** 2)) / 8.0
        
        return {
            "thickness_mm": thickness,
            "dead_load": total_dead,
            "live_load": live_load,
            "ultimate_load_qu": qu,
            "moment_mu": mu,
            "rebar": "Ø10@200mm Bottom / Ø10@250mm Top"
        }

    def design_slab(self, span_x, span_y):
        # دالة شاملة تحدد نوع البلاطة تلقائياً وتصممها
        ratio = max(span_x, span_y) / min(span_x, span_y)
        if ratio >= 2.0:
            return self.design_one_way_slab(span=min(span_x, span_y))
        else:
            # Two-way slab calculation
            thickness = max(150, math.ceil(((span_x + span_y) * 1000 / 180) / 10.0) * 10)
            total_dead = (thickness / 1000.0) * 24.0 + 2.5
            live_load = 2.0
            return {
                "thickness_mm": thickness,
                "dead_load": total_dead,
                "live_load": live_load,
                "rebar": "Ø12@200mm Mesh T&B"
            }
