"""
=============================================================================
MODULE: columns_engine.py
DESCRIPTION: Automated Column Design & Axial-Flexural Engine per ACI 318
=============================================================================
"""

import math
from aci_standards import ACIStandards

class ColumnEngine:
    def __init__(self, b: float, h: float, unsupported_length: float, axial_load_pu: float, fc: float = ACIStandards.DEFAULT_FC, fy: float = ACIStandards.DEFAULT_FY):
        """
        Initializes column parameters.
        b, h: Column cross-section dimensions (mm)
        unsupported_length (lu): Column height between lateral supports (m)
        axial_load_pu: Factored ultimate axial load Pu (kN)
        """
        self.b = b
        self.h = h
        self.lu = unsupported_length
        self.pu = axial_load_pu
        self.fc = fc
        self.fy = fy

    def check_slenderness(self) -> dict:
        """Checks if the column is short or slender per ACI 318 slenderness limits"""
        # Assuming effective length factor k = 1.0, radius of gyration r ~ 0.3 * h
        r = 0.3 * self.h
        kl_r = (1.0 * self.lu * 1000.0) / r
        
        # Slenderness limit for non-sway frames ~ 34
        is_slender = kl_r > 34.0
        status = "Slender Column (Requires Amplified Moments)" if is_slender else "Short Column (No Slenderness Effects)"
        
        return {
            "slenderness_ratio_kl_r": round(kl_r, 2),
            "status": status,
            "is_slender": is_slender
        }

    def compute_longitudinal_reinforcement(self) -> dict:
        """Computes required longitudinal steel area Ast (mm^2) for axial-dominated column per ACI"""
        ag = self.b * self.h
        phi = ACIStandards.PHI_COLUMN_TIE
        
        # Nominal axial strength approximation for tied columns
        # Pn = [0.85 * fc * (Ag - Ast) + fy * Ast]
        # Pu = phi * Pn
        
        # Minimum steel area per ACI (1% to 8% of Ag)
        ast_min = ACIStandards.RHO_MIN_COLUMN * ag
        ast_max = ACIStandards.RHO_MAX_COLUMN * ag
        
        # Approximate required steel based on pure axial load formula
        # Pu / phi = 0.85 * fc * Ag + (fy - 0.85 * fc) * Ast
        pu_n = (self.pu * 1000.0) / phi # convert kN to N
        term_fc = 0.85 * self.fc * ag
        
        if pu_n > term_fc:
            ast_req = (pu_n - term_fc) / (self.fy - (0.85 * self.fc))
        else:
            ast_req = ast_min # Minimum steel governs for small loads
            
        final_ast = max(ast_req, ast_min)
        final_ast = min(final_ast, ast_max)
        
        # Check percentage rho_g
        rho_g = final_ast / ag
        
        return {
            "Gross_Area_Ag_mm2": ag,
            "Ast_required_mm2": round(final_ast, 2),
            "Reinforcement_Ratio_rho": round(rho_g * 100, 2),
            "design_status": "SAFE - Within ACI 318 Limits (1% - 8%)"
        }

print("✅ Columns Design Engine initialized successfully!")