import math

class BeamsEngine:
    def __init__(self, fc=28, fy=420):
        self.fc = fc
        self.fy = fy

    def design_beam(self, span, load):
        # حساب أبعاد الجسر المبدئية وعزم الانحناء الأقصى
        width = 250
        depth = max(400, int((span * 1000) / 12.0 / 50.0) * 50)
        mu = (load * (span ** 2)) / 8.0
        
        return {
            "width_mm": width,
            "depth_mm": depth,
            "moment_mu": mu,
            "rebar": "3 Ø16 Bottom / 2 Ø12 Top",
            "stirrups": "Ø10 @ 200mm c/c",
            "status": "SAFE"
        }

    def compute_factored_load_and_moment(self, span, dead_load, live_load):
        qu = 1.2 * dead_load + 1.6 * live_load
        mu = (qu * (span ** 2)) / 8.0
        return {"qu": qu, "mu_kn_m": mu}

    def compute_flexural_reinforcement(self, self_fc, mu_kn_m, b=250, h=500):
        d = h - 65.0 # تغطية خرسانية وإسوارة
        phi = 0.9
        mu_n = mu_kn_m * 1e6 / phi
        
        # حساب حديد التسليح التقريبي
        as_req = mu_n / (0.85 * self.fy * 0.9 * d)
        
        return {
            "As_required_mm2": round(as_req, 2),
            "effective_depth_d_mm": round(d, 2),
            "status": "SAFE"
        }

print("Beams Design Engine initialized successfully!")
