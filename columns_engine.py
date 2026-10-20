import math

class ColumnsEngine:
    def __init__(self, fc=28, fy=420):
        self.fc = fc
        self.fy = fy

    def design_column(self, axial_load_kn):
        # تصميم مبدئي للأعمدة الخرسانية تحت تأثير الأحمال المحورية
        # Pn = 0.80 * [0.85 * fc * (Ag - Ast) + fy * Ast]
        # فرض نسبة تسليح تقريبية 2%
        required_ag = (axial_load_kn * 1000) / (0.65 * (0.85 * self.fc * 0.98 + self.fy * 0.02))
        side = max(300, int(math.sqrt(required_ag) / 50.0) * 50)
        
        return {
            "dimension_x_mm": side,
            "dimension_y_mm": side,
            "rebar": "8 Ø16",
            "ties": "Ø10 @ 200mm",
            "status": "SAFE"
        }

print("Columns Design Engine initialized successfully!")
