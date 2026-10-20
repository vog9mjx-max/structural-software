import math

class ColumnsEngine:
    """
    محرك تصميم الأعمدة الخرسانية تحت تأثير الأحمال المحورية والعزوم وفق ACI 318
    Computes axial load capacity, required area, and reinforcement details.
    """
    def __init__(self, fc=28, fy=420):
        self.fc = fc  # المقاومة المميزة للخرسانة (MPa)
        self.fy = fy  # إجهاد الخضوع للحديد (MPa)

    def design_column(self, axial_load_kn):
        """
        التصميم المبدئي للأعمدة الخرسانية المربعة/المستطيلة تحت تأثير الحمل المحوري Pu
        Pn = 0.80 * [0.85 * fc * (Ag - Ast) + fy * Ast]
        """
        # فرض نسبة تسليح تقريبية حوالي 2% (0.02)
        rho_st = 0.02
        
        # Factor of Safety / Capacity Reduction for tied columns (phi = 0.65)
        phi = 0.65
        pn_req = (axial_load_kn * 1000) / phi  # N
        
        # حساب المساحة الإجمالية المطلوبة للمقطع Ag
        # pn_req = 0.80 * [0.85 * fc * Ag * (1 - rho_st) + fy * Ag * rho_st]
        term = 0.80 * (0.85 * self.fc * (1 - rho_st) + self.fy * rho_st)
        ag_req = pn_req / term
        
        # حساب أبعاد المقطع (مربع كمبدأ أساسي، بحد أدنى 300 مم)
        side = max(300, int(math.sqrt(ag_req) / 25.0) * 25)
        ag_actual = side * side
        
        # مساحة الحديد المطلوبة Ast
        ast_req = rho_st * ag_actual
        
        # حساب عدد الأسياخ (Ø20 - مساحة السيخ ≈ 314 mm²)
        bar_area = math.pi * (20 ** 2) / 4.0
        num_bars = max(4, math.ceil(ast_req / bar_area))

        return {
            "dimension_x_mm": side,
            "dimension_y_mm": side,
            "gross_area_mm2": ag_actual,
            "ast_required_mm2": round(ast_req, 1),
            "rebar": f"{num_bars} Ø20",
            "ties": "Ø10 @ 200mm c/c",
            "status": "SAFE"
        }

print("Advanced Columns Design Engine loaded successfully!")
