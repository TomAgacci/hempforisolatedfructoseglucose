Licensed Under Creative Commons Attribution Non Commercial Open Source

FLOWCHART: Bast + Salt PressureChem Conversion

STEP 1: INPUT_FEED
  - Receive bast mass (kg)
  - Receive salt mass (kg)

STEP 2: FRACTIONATE_BAST
  - Compute cellulose_mass = bast_mass * cellulose_fraction
  - Compute hemicellulose_mass = bast_mass * hemicellulose_fraction
  - Compute lignin_mass = bast_mass * lignin_fraction

STEP 3: CELLULOSE_TO_GLUCOSE
  - Compute theoretical_glucose = cellulose_mass * (180 / 162)
  - Compute actual_glucose = theoretical_glucose * cellulose_eff
  - Compute cellulose_unconverted = cellulose_mass * (1 - cellulose_eff)

STEP 4: HEMICELLULOSE_TO_XYLOSE
  - Compute theoretical_xylose = hemicellulose_mass * (150 / 132)
  - Compute actual_xylose = theoretical_xylose * hemicellulose_eff
  - Compute hemicellulose_unconverted = hemicellulose_mass * (1 - hemicellulose_eff)

STEP 5: RESIDUE_POOL
  - residue_mass = lignin_mass
                  + cellulose_unconverted
                  + hemicellulose_unconverted

STEP 6: SALT_PASS_THROUGH
  - salt_out = salt_mass  (no reaction)

STEP 7: MASS_BALANCE_OUTPUT
  - Output glucose_mass = actual_glucose
  - Output xylose_mass = actual_xylose
  - Output residue_mass
  - Output salt_out
  - Compute total_sugars = glucose_mass + xylose_mass
  - Compute total_out = total_sugars + residue_mass + salt_out

END

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



Simulated Operational Model to plugin
Below is the complete step sequence your computational engine would follow when “processing” bast + salt.

1
Define the Bast and Salt Inputs
Start Here
Establish the mass and composition of bast and treat salt as an inert modifier.

Set bast_mass (e.g., 1.0 kg)

Assign bast fractions: cellulose, hemicellulose, lignin

Set salt_mass (e.g., 0.10 kg)

Salt is marked as non-reactive

2
Apply Stoichiometric Models
Convert cellulose and hemicellulose into theoretical sugar yields.

Cellulose → glucose using 180/162 mass ratio

Hemicellulose → xylose using 150/132 mass ratio

Lignin remains unchanged

3
Introduce Efficiency Parameters
Simulate pressure-chem effects by applying conversion efficiencies.

Use cellulose_eff (e.g., 0.85)

Use hemicellulose_eff (e.g., 0.70)

Multiply theoretical yields by efficiencies

4
Compute Actual Product Masses
Calculate glucose, xylose, and unconverted fractions.

glucose = cellulose_mass × yield_factor × cellulose_eff

xylose = hemi_mass × yield_factor × hemi_eff

residue = lignin + unconverted cellulose + unconverted hemicellulose

5
Carry Salt Through the System
Salt remains unchanged and exits as inert mass.

salt_out = salt_in

No reaction lines include NaCl

Salt affects no stoichiometry

6
Assemble Final Mass Balance
Combine sugars, residue, and salt into a complete output dataset.

total_sugars = glucose + xylose

total_residue = lignin + unconverted fractions

total_output = sugars + residue + salt

Water incorporation explains mass increase
