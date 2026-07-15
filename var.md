# ============================
# Bast + Salt PressureChem Variables
# ============================

# ---- Feedstock Masses ----
BAST_MASS = 1.0          # kg bast input
SALT_MASS = 0.10         # kg salt (inert)

# ---- Bast Composition Fractions ----
CELLULOSE_FRAC = 0.70
HEMI_FRAC       = 0.15
LIGNIN_FRAC     = 0.15

# ---- Molecular Weights ----
MW_CELLULOSE_UNIT = 162      # C6H10O5
MW_GLUCOSE        = 180      # C6H12O6

MW_XYLAN_UNIT     = 132      # C5H8O4
MW_XYLOSE         = 150      # C5H10O5

# ---- Stoichiometric Yield Factors ----
Y_GLUCOSE = MW_GLUCOSE / MW_CELLULOSE_UNIT   # 1.111
Y_XYLOSE  = MW_XYLOSE  / MW_XYLAN_UNIT       # 1.136

# ---- Conversion Efficiencies ----
EFF_CELLULOSE = 0.85
EFF_HEMI      = 0.70

# ---- Derived Masses ----
CELLULOSE_MASS = BAST_MASS * CELLULOSE_FRAC
HEMI_MASS      = BAST_MASS * HEMI_FRAC
LIGNIN_MASS    = BAST_MASS * LIGNIN_FRAC

# ---- Theoretical Products ----
GLUCOSE_THEORETICAL = CELLULOSE_MASS * Y_GLUCOSE
XYLOSE_THEORETICAL  = HEMI_MASS      * Y_XYLOSE

# ---- Actual Products ----
GLUCOSE_ACTUAL = GLUCOSE_THEORETICAL * EFF_CELLULOSE
XYLOSE_ACTUAL  = XYLOSE_THEORETICAL  * EFF_HEMI

# ---- Unconverted Fractions ----
CELLULOSE_UNCONV = CELLULOSE_MASS * (1 - EFF_CELLULOSE)
HEMI_UNCONV      = HEMI_MASS      * (1 - EFF_HEMI)

# ---- Residue ----
RESIDUE_TOTAL = LIGNIN_MASS + CELLULOSE_UNCONV + HEMI_UNCONV

# ---- Salt Output ----
SALT_OUT = SALT_MASS

# ---- Final Mass Balance ----
TOTAL_SUGARS = GLUCOSE_ACTUAL + XYLOSE_ACTUAL
TOTAL_OUTPUT = TOTAL_SUGARS + RESIDUE_TOTAL + SALT_OUT
