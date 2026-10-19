import math

class ACIStandards:
    DEAD_LOAD_FACTOR: float = 1.2
    LIVE_LOAD_FACTOR: float = 1.6
    PHI_FLEXURE_TENSION: float = 0.90
    PHI_SHEAR: float = 0.75
    PHI_COMPRESSION_TIED: float = 0.65
    PHI_BEARING_SOIL: float = 0.50
    DEFAULT_FC: float = 28.0
    DEFAULT_FY: float = 420.0
    ES: float = 200000.0

    @staticmethod
    def get_ec(fc: float) -> float:
        return 4700.0 * math.sqrt(fc)

    @staticmethod
    def get_beta1(fc: float) -> float:
        if fc <= 28.0:
            return 0.85
        elif fc >= 55.0:
            return 0.65
        else:
            return 0.85 - (0.05 * (fc - 28.0) / 7.0)

    RHO_MIN_SLAB_FLEXURE: float = 0.0018
    RHO_MIN_COLUMN: float = 0.01
    RHO_MAX_COLUMN: float = 0.08
    CONCRETE_COVER_SLAB: float = 20.0
    CONCRETE_COVER_BEAM: float = 40.0
    CONCRETE_COVER_FOOTING: float = 75.0
    PHI_COLUMN_TIE: float = 0.65
print("ACI Standards Module initialized successfully!")