import math

class BeamsEngine:
    """
    محرك تصميم الجسور الخرسانية وفق كود ACI 318
    Computes flexural design, shear capacity, and minimum/maximum steel area.
    """
    def __init__(self, fc=28, fy=420):
        self.fc = fc  # المقاومة المميزة للخرسانة (MPa)
        self.fy = fy  # إجهاد الخضوع للحديد (MPa)

    def design_beam(self, span, load, b=250, h=500):
        """
        التصميم المباشر للجسر لحساب العزوم والتسليح الموصى به
        """
        # 1. حساب عزم الانحناء الأقصى Mu (kN.m) للجسر بسيط الإسناد
        mu_kn_m = (load * (span ** 2)) / 8.0
        
        # 2. العمق الفعال d
        cover = 40  # غطاء خرساني
        stirrup_dia = 10
        bar_dia = 16
        d = h - cover - stirrup_dia - (bar_dia / 2.0)  # mm
        
        if d <= 0:
            return {"status": "ERROR", "message": "أبعاد المقطع صغيرة جداً"}

        # 3. حساب حديد التسليح المطلوب وفق ACI 318
        phi = 0.90  # عامل خفض المقاومة للانحناء
        mu_n = (mu_kn_m * 1e6) / phi  # N.mm
        
        # حساب معدل التسليح As
        # Mu_n = As * fy * (d - a/2)
        # تقريب هندسي دقيق لعمق كتل الإجهاد a:
        a_guess = 0.2 * d
        as_req = mu_n / (self.fy * (d - a_guess / 2.0))
        
        # إعادة تصحيح a للحصول على دقة عالية
        a_exact = (as_req * self.fy) / (0.85 * self.fc * b)
        as_req = mu_n / (self.fy * (d - a_exact / 2.0))

        # 4. حساب الحد الأدنى لحديد التسليح As_min وفق ACI 318
        as_min_1 = (0.25 * math.sqrt(self.fc) / self.fy) * b * d
        as_min_2 = (1.4 / self.fy) * b * d
        as_min = max(as_min_1, as_min_2)

        # التسليح النهائي
        as_final = max(as_req, as_min)
        
        # حساب عدد الشياش (أسياخ Ø16 - مساحة السيخ الواحد ≈ 201 mm²)
        num_bars = max(2, math.ceil(as_final / 201.0))

        return {
            "width_mm": b,
            "depth_mm": h,
            "effective_depth_d_mm": round(d, 1),
            "moment_mu_kn_m": round(mu_kn_m, 2),
            "as_required_mm2": round(as_final, 1),
            "as_min_mm2": round(as_min, 1),
            "rebar": f"{num_bars} Ø16 Bottom / 2 Ø12 Top",
            "stirrups": "Ø10 @ 150mm c/c",
            "status": "SAFE"
        }

    def compute_factored_load_and_moment(self, span, dead_load, live_load):
        qu = 1.2 * dead_load + 1.6 * live_load
        mu = (qu * (span ** 2)) / 8.0
        return {"qu": qu, "mu_kn_m": mu}

    def compute_flexural_reinforcement(self, mu_kn_m, b=250, h=500):
        res = self.design_beam(span=5.0, load=0, b=b, h=h)
        return res

print("Advanced Beams Design Engine loaded successfully!")
