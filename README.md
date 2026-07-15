Licensed Under Creative Commons Attribution Non Commercial Open Source

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
