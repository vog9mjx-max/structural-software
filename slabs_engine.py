"""
=============================================================================
MODULE: slabs_engine.py
DESCRIPTION: Automated Slab Design & Analysis Engine per ACI 318
=============================================================================
"""

import math
from aci_standards import ACIStandards

class SlabEngine:
    def __init__(self, lx: float, ly: float, thickness: float, dead_load: float, live_load: float, fc: float = ACIStandards.DEFAULT_FC, fy: float = ACIStandards.DEFAULT_FY):
        self.lx = lx
        self.ly = ly
        self.h = thickness
        self.dl = dead_load
        self.ll = live_load
        self.fc = fc
        self.fy = fy

    def check_two_way_action(self) -> str:
        """Determines if the slab behaves as One-Way or Two-Way slab"""
        beta = self.ly / self.lx
        if beta < 2.0:
            return "Two-Way Slab"
        else:
            return "One-Way Slab"

    def calculate_ultimate_load(self) -> float:
        """Calculates Factored Ultimate Load Wu per ACI 318 (kN/m^2)"""
        wu = (ACIStandards.DEAD_LOAD_FACTOR * self.dl) + (ACIStandards.LIVE_LOAD_FACTOR * self.ll)
        return wu

    def check_minimum_thickness_aci(self) -> dict:
        """Checks minimum thickness requirements for deflection control per ACI"""
        perimeter = 2 * (self.lx * 1000 + self.ly * 1000)
        h_min = perimeter / 180.0
        is_adequate = self.h >= h_min
        status = "SAFE" if is_adequate else "UNSAFE"
        
        return {
            "h_provided_mm": self.h,
            "h_min_required_mm": h_min,
            "status": status,
            "justification": f"Provided thickness {self.h} mm vs Minimum required {h_min:.1f} mm."
        }

    def compute_flexural_reinforcement(self, moment_kn_m: float, b_width_mm: float = 1000.0) -> dict:
        """Computes required steel area As (mm^2) for a given bending moment"""
        d = self.h - ACIStandards.CONCRETE_COVER_SLAB - (10.0 / 2.0)
        phi = ACIStandards.PHI_FLEXURE_TENSION
        
        if d <= 0:
            return {"error": "Effective depth is too small for given cover and thickness."}

        mu = moment_kn_m * 1e6
        nominal_moment = mu / phi
        as_req = nominal_moment / (self.fy * (0.9 * d))
        as_min = ACIStandards.RHO_MIN_SLAB_FLEXURE * b_width_mm * d
        final_as = max(as_req, as_min)
        
        return {
            "As_required_mm2": round(final_as, 2),
            "As_min_mm2": round(as_min, 2),
            "effective_depth_d_mm": round(d, 2),
            "status": "SAFE"
        }

print("✅ Slabs Design Engine initialized successfully!")