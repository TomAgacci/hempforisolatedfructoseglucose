#!/usr/bin/env python3
"""
Salt-aware PressureChem Conversion Engine
- Bast: cellulose, hemicellulose, lignin
- Salt: inert, but modifies environment (heat, water behavior)
- Water: hydrolysis medium
- Heat: drives conversion

All values are simulation-only, abstract mass-balance + environment modifiers.
"""

from dataclasses import dataclass


@dataclass
class BastComposition:
    cellulose: float
    hemicellulose: float
    lignin: float


@dataclass
class ConversionEff:
    cellulose_eff: float
    hemicellulose_eff: float


@dataclass
class Environment:
    bast_mass: float
    salt_mass: float
    water_mass: float
    heat_temp_target_c: float
    water_activity: float
    salt_environment_modifier: float
    thermal_diffusivity_factor: float


@dataclass
class ConversionResult:
    glucose: float
    xylose: float
    residue: float
    salt_out: float
    eff_cellulose_eff: float
    eff_hemicellulose_eff: float


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def build_default_environment() -> Environment:
    return Environment(
        bast_mass=1.0,
        salt_mass=0.10,
        water_mass=0.50,
        heat_temp_target_c=120.0,
        water_activity=0.95,
        salt_environment_modifier=0.98,
        thermal_diffusivity_factor=1.12,
    )


def compute_effective_efficiencies(base_eff: ConversionEff, env: Environment) -> ConversionEff:
    """
    Salt-aware, heat-aware effective efficiencies.
    Simple model:
      eff_eff = base_eff * salt_environment_modifier * f(heat, water)
    """

    # Heat/water drive factor (normalized)
    hydrolysis_drive = env.heat_temp_target_c * env.water_activity  # e.g. 120 * 0.95
    # Normalize to a 0–1 scale with a reference (say 100)
    drive_factor = clamp(hydrolysis_drive / 100.0)

    # Salt environment modifier (slightly reducing or enhancing)
    salt_mod = env.salt_environment_modifier

    eff_cellulose_eff = clamp(base_eff.cellulose_eff * salt_mod * drive_factor)
    eff_hemicellulose_eff = clamp(base_eff.hemicellulose_eff * salt_mod * drive_factor)

    return ConversionEff(
        cellulose_eff=eff_cellulose_eff,
        hemicellulose_eff=eff_hemicellulose_eff,
    )


def pressurechem_convert(
    comp: BastComposition,
    base_eff: ConversionEff,
    env: Environment,
) -> ConversionResult:
    """
    Salt-aware bast conversion:
    - Uses environment (salt, water, heat) to adjust effective efficiencies.
    - Salt remains inert in stoichiometry but modifies conversion environment.
    """

    bast_mass = env.bast_mass
    salt_mass = env.salt_mass

    # Bast fractions
    cellulose_mass = bast_mass * comp.cellulose
    hemi_mass      = bast_mass * comp.hemicellulose
    lignin_mass    = bast_mass * comp.lignin

    # Stoichiometric yield factors
    MW_CELLULOSE_UNIT = 162.0
    MW_GLUCOSE        = 180.0
    MW_XYLAN_UNIT     = 132.0
    MW_XYLOSE         = 150.0

    Y_GLUCOSE = MW_GLUCOSE / MW_CELLULOSE_UNIT   # ~1.111
    Y_XYLOSE  = MW_XYLOSE  / MW_XYLAN_UNIT       # ~1.136

    # Effective efficiencies (salt + heat + water)
    eff = compute_effective_efficiencies(base_eff, env)

    # Cellulose -> glucose
    glucose_theoretical = cellulose_mass * Y_GLUCOSE
    glucose_actual      = glucose_theoretical * eff.cellulose_eff
    cellulose_unconv    = cellulose_mass * (1.0 - eff.cellulose_eff)

    # Hemicellulose -> xylose
    xylose_theoretical = hemi_mass * Y_XYLOSE
    xylose_actual      = xylose_theoretical * eff.hemicellulose_eff
    hemi_unconv        = hemi_mass * (1.0 - eff.hemicellulose_eff)

    # Residue pool
    residue_total = lignin_mass + cellulose_unconv + hemi_unconv

    return ConversionResult(
        glucose=glucose_actual,
        xylose=xylose_actual,
        residue=residue_total,
        salt_out=salt_mass,
        eff_cellulose_eff=eff.cellulose_eff,
        eff_hemicellulose_eff=eff.hemicellulose_eff,
    )


def print_result(comp: BastComposition, base_eff: ConversionEff, env: Environment, result: ConversionResult) -> None:
    print("=== Salt-aware PressureChem Bast + Salt Simulation ===")
    print(f"Bast mass:        {env.bast_mass:.3f} kg")
    print(f"Salt mass:        {env.salt_mass:.3f} kg")
    print(f"Water mass:       {env.water_mass:.3f} kg")
    print(f"Heat target:      {env.heat_temp_target_c:.1f} °C")
    print(f"Water activity:   {env.water_activity:.3f}")
    print(f"Salt env modifier:{env.salt_environment_modifier:.3f}")
    print()
    print(f"Base eff cellulose:    {base_eff.cellulose_eff:.3f}")
    print(f"Base eff hemicellulose:{base_eff.hemicellulose_eff:.3f}")
    print(f"Effective eff cellulose:    {result.eff_cellulose_eff:.3f}")
    print(f"Effective eff hemicellulose:{result.eff_hemicellulose_eff:.3f}")
    print()
    print(f"Glucose:          {result.glucose:.3f} kg")
    print(f"Xylose:           {result.xylose:.3f} kg")
    print(f"Residue:          {result.residue:.3f} kg")
    print(f"Salt (inert):     {result.salt_out:.3f} kg")
    total_sugars = result.glucose + result.xylose
    total_out = total_sugars + result.residue + result.salt_out
    print(f"Total sugars:     {total_sugars:.3f} kg")
    print(f"Total out:        {total_out:.3f} kg")


def main():
    # Bast composition
    comp = BastComposition(
        cellulose=0.70,
        hemicellulose=0.15,
        lignin=0.15,
    )

    # Base conversion efficiencies (before salt/heat/water modifiers)
    base_eff = ConversionEff(
        cellulose_eff=0.85,
        hemicellulose_eff=0.70,
    )

    # Environment (salt + water + heat)
    env = build_default_environment()

    # Run salt-aware conversion
    result = pressurechem_convert(comp, base_eff, env)
    print_result(comp, base_eff, env, result)


if __name__ == "__main__":
    main()
