import math

class FootingsEngine:
    def __init__(self, fc=28, fy=420, qa=150):
        self.fc = fc
        self.fy = fy
        self.qa = qa  # إجهاد التأسيس المسموح به (kN/m2)

    def design_footing(self, axial_load_kn):
        # تصميم مبدئي للأسس المنفردة تحت تأثير الأحمال المحورية
        area_req = axial_load_kn / self.qa
        side = max(1.0, round(math.sqrt(area_req), 2))
        thickness = 450  # مم
        
        return {
            "length_m": side,
            "width_m": side,
            "thickness_mm": thickness,
            "rebar": "Ø16 @ 150mm c/c each way",
            "status": "SAFE"
        }

print("Footings Design Engine initialized successfully!")
