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
