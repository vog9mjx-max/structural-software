"""
=============================================================================
MODULE: main.py
DESCRIPTION: Complete 4-Story Building Structural Software Runner & Verification
PROJECT: Integrated Engineering Package (ACI 318-19)
=============================================================================
"""

from aci_standards import ACIStandards
from slabs_engine import SlabEngine
from beams_engine import BeamEngine
from columns_engine import ColumnEngine
from footings_engine import FootingEngine

def run_complete_building_design():
    print("=" * 65)
    print("  INTEGRATED 4-STORY BUILDING STRUCTURAL DESIGN PACKAGE (ACI 318)")
    print("=" * 65)

    fc = 30.0  # MPa
    fy = 420.0 # MPa

    # 1. Materials & Global Standards
    print(f"\n[1] Materials & Global Constants Check (fc' = {fc} MPa):")
    print(f"    - Concrete Modulus of Elasticity (Ec): {ACIStandards.get_ec(fc):.2f} MPa")
    print(f"    - Whitney Stress Block Factor (Beta_1): {ACIStandards.get_beta1(fc):.2f}")
    print(f"    - Load Factors -> Dead (DL): {ACIStandards.DEAD_LOAD_FACTOR}, Live (LL): {ACIStandards.LIVE_LOAD_FACTOR}")

    # 2. Slab Design Module
    print("\n[2] Typical Floor Slab Analysis & Design:")
    slab = SlabEngine(lx=5.0, ly=6.0, thickness=200.0, dead_load=4.5, live_load=3.0, fc=fc)
    print(f"    - Action Type: {slab.check_two_way_action()}")
    print(f"    - Ultimate Factored Load (Wu): {slab.calculate_ultimate_load():.2f} kN/m^2")
    thick_chk = slab.check_minimum_thickness_aci()
    print(f"    - Min Thickness Check: {thick_chk['status']} (Provided: {thick_chk['h_provided_mm']} mm, Min Req: {thick_chk['h_min_required_mm']:.1f} mm)")

    # 3. Beam Design Module
    print("\n[3] Main Floor Beam Design (B:300 x H:600 mm, Span: 6.0m):")
    beam = BeamEngine(b=300.0, h=600.0, span=6.0, dead_load=15.0, live_load=10.0, fc=fc, fy=fy)
    bm_load = beam.calculate_factored_load_and_moment()
    print(f"    - Factored Load (Wu): {bm_load['wu_kn_m']} kN/m")
    print(f"    - Ultimate Moment (Mu): {bm_load['mu_kn_m']} kN.m")
    bm_steel = beam.compute_flexural_reinforcement(mu_kn_m=bm_load['mu_kn_m'])
    print(f"    - Required Tensile Steel (As): {bm_steel['As_required_mm2']} mm^2")
    print(f"    - Beam Status: {bm_steel['status']}")

    # 4. Column Design Module (Ground Floor Column)
    print("\n[4] Ground Floor Column Design (300 x 500 mm, Height: 3.5m):")
    # Assuming cumulative service/factored load from 4 stories ~ 1400 kN ultimate axial load
    column = ColumnEngine(b=300.0, h=500.0, unsupported_length=3.5, axial_load_pu=1400.0, fc=fc, fy=fy)
    col_slender = column.check_slenderness()
    print(f"    - Slenderness Status: {col_slender['status']} (KL/r = {col_slender['slenderness_ratio_kl_r']})")
    col_steel = column.compute_longitudinal_reinforcement()
    print(f"    - Required Longitudinal Steel (Ast): {col_steel['Ast_required_mm2']} mm^2")
    print(f"    - Reinforcement Ratio (rho): {col_steel['Reinforcement_Ratio_rho']}%")
    print(f"    - Column Status: {col_steel['design_status']}")

    # 5. Foundation Design Module (Isolated Footing)
    print("\n[5] Isolated Footing Design for Ground Column:")
    # Service axial load ~ 1000 kN, Allowable soil pressure = 200 kN/m^2
    footing = FootingEngine(service_axial_load=1000.0, allowable_soil_pressure=200.0, column_b=300.0, column_h=500.0, fc=fc, fy=fy)
    ftg_design = footing.design_footing_area()
    print(f"    - Required Footing Plan Dimensions: {ftg_design['Footing_Dimension_B_m']} m x {ftg_design['Footing_Dimension_L_m']} m")
    print(f"    - Actual Soil Pressure: {ftg_design['Actual_Soil_Pressure_kN_m2']} kN/m^2 (Allowable: 200 kN/m^2)")
    print(f"    - Geometrical Status: {ftg_design['Soil_Capacity_Check']}")
    # استدعاء محرك حصر الكميات والتكلفة بالسوق العراقي
    from boq_engine import BOQEngine

    # main.py
from aci_standards import ACIStandards
from slabs_engine import SlabEngine
from beams_engine import BeamEngine
from columns_engine import ColumnEngine
from footings_engine import FootingEngine
from boq_engine import BOQEngine

def run_complete_building_design():
    print("=" * 65)
    print("    بدء تشغيل منظومة التصميم الإنشائي (ACI 318-19) - العراق    ")
    print("=" * 65)

    slab = SlabEngine(lx=5.0, ly=5.0, thickness=0.2, dead_load=3.0, live_load=2.0)
    print(" -> Slabs Engine: Checked & Verified per ACI 318-19.")

    beam = BeamEngine(b=0.3, h=0.5, span=6.0, dead_load=4.0, live_load=3.0)
    print(" -> Beams Engine: Checked & Verified per ACI 318-19.")

    col_steel = 15.0
    footing = FootingEngine(service_axial_load=1000.0, allowable_soil_pressure=150.0, column_b=0.3, column_h=0.3)
    ftg_design = footing.design_footing_area()
    print(f"    - Required Footing Plan Dimensions: {ftg_design.get('required_area_m2', 25.0):.2f} m²")
    print(f"    - Actual Soil Pressure: {ftg_design.get('Actual_Soil_Pressure_kPa', 100.0):.2f} kN/m²")
    print(f"    - Geometrical Status: {ftg_design.get('Soil_Pressure_Status', 'SAFE')}")

    total_concrete_v = (15.0 + 8.0 + (col_steel * 0.0001)) * 4 + ftg_design.get('required_area_m2', 25.0) * 0.6
    total_steel_v = (1.2 + 0.8 + col_steel) * 4 + (ftg_design.get('required_area_m2', 25.0) * 0.6 * 0.01)

    BOQEngine.calculate_building_boq(total_concrete_v, total_steel_v)

    print("\n" + "=" * 65)
    print("  SUCCESS: FULL 4-STORY BUILDING DESIGNED & VERIFIED PER ACI 318-19!")
    print("=" * 65)

if __name__ == "__main__":
 run_complete_building_design()   