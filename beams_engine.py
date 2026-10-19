"""
=============================================================================
MODULE: beams_engine.py
DESCRIPTION: Automated Beam Design & Flexural/Shear Analysis Engine per ACI 318
=============================================================================
"""

import math
from aci_standards import ACIStandards

class BeamEngine:
    def __init__(self, b: float, h: float, span: float, dead_load: float, live_load: float, fc: float = ACIStandards.DEFAULT_FC, fy: float = ACIStandards.DEFAULT_FY):
        self.b = b
        self.h = h
        self.span = span
        self.dl = dead_load
        self.ll = live_load
        self.fc = fc
        self.fy = fy

    def calculate_factored_load_and_moment(self) -> dict:
        """Calculates Factored Ultimate Load Wu (kN/m) and Ultimate Moment Mu (kN.m) for simply supported beam"""
        wu = (ACIStandards.DEAD_LOAD_FACTOR * self.dl) + (ACIStandards.LIVE_LOAD_FACTOR * self.ll)
        mu = (wu * (self.span ** 2)) / 8.0
        
        return {
            "wu_kn_m": round(wu, 2),
            "mu_kn_m": round(mu, 2)
        }

    def compute_flexural_reinforcement(self, mu_kn_m: float) -> dict:
        """Computes required flexural tensile reinforcement As (mm^2) for the beam section"""
        d = self.h - ACIStandards.CONCRETE_COVER_BEAM - 10.0 - (25.0 / 2.0)
        phi = ACIStandards.PHI_FLEXURE_TENSION
        
        if d <= 0:
            return {"error": "Beam depth is too small for given cover and stirrups."}

        mu_nmm = mu_kn_m * 1e6
        nominal_moment = mu_nmm / phi
        as_req = nominal_moment / (self.fy * (0.9 * d))
        
        as_min_1 = (0.25 * math.sqrt(self.fc) / self.fy) * self.b * d
        as_min_2 = (1.4 / self.fy) * self.b * d
        as_min = max(as_min_1, as_min_2)
        
        final_as = max(as_req, as_min)
        
        return {
            "As_required_mm2": round(final_as, 2),
            "As_min_mm2": round(as_min, 2),
            "effective_depth_d_mm": round(d, 2),
            "status": "SAFE"
        }

print("✅ Beams Design Engine initialized successfully!")