"""
=============================================================================
MODULE: footings_engine.py
DESCRIPTION: Automated Isolated Footing Design & Geometrical Sizing per ACI 318
=============================================================================
"""

import math
from aci_standards import ACIStandards

class FootingEngine:
    def __init__(self, service_axial_load: float, allowable_soil_pressure: float, column_b: float, column_h: float, fc: float = ACIStandards.DEFAULT_FC, fy: float = ACIStandards.DEFAULT_FY):
        """
        Initializes footing parameters.
        service_axial_load (P_service): Unfactored service axial load (kN)
        allowable_soil_pressure (qa): Allowable bearing capacity of soil (kN/m^2)
        column_b, column_h: Column dimensions resting on footing (mm)
        """
        self.p_service = service_axial_load
        self.qa = allowable_soil_pressure
        self.col_b = column_b / 1000.0  # convert to meters
        self.col_h = column_h / 1000.0  # convert to meters
        self.fc = fc
        self.fy = fy

    def design_footing_area(self) -> dict:
        """Determines required footing plan dimensions (B x L assuming square footing)"""
        # Estimated footing weight ~ 10% of service load
        total_service_load = self.p_service * 1.10
        
        # Required area A = P / qa
        required_area = total_service_load / self.qa
        
        # Side length for square footing
        side_length = math.sqrt(required_area)
        # Round up to nearest 0.05m (50mm) for practical construction
        side_length_rounded = math.ceil(side_length * 20.0) / 20.0
        
        provided_area = side_length_rounded ** 2
        actual_soil_pressure = total_service_load / provided_area
        
        return {
            "Required_Area_m2": round(required_area, 2),
            "Footing_Dimension_B_m": side_length_rounded,
            "Footing_Dimension_L_m": side_length_rounded,
            "Provided_Area_m2": round(provided_area, 2),
            "Actual_Soil_Pressure_kN_m2": round(actual_soil_pressure, 2),
            "Soil_Capacity_Check": "SAFE - Pressure within allowable limits" if actual_soil_pressure <= self.qa else "UNSAFE - Increase dimensions"
        }

print("✅ Footing Design Engine initialized successfully!")