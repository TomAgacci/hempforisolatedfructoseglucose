#!/usr/bin/env python3
"""
Simple bast-fiber pressure-chem conversion engine.

Models:
- Cellulose -> Glucose
- Hemicellulose -> Xylose
- Lignin -> Residue (non-reactive)

All masses in kg.
"""

from dataclasses import dataclass


@dataclass
class Reaction:
    name: str
    reactant_formula: str
    product_formula: str
    yield_factor: float  # kg product / kg reactant (theoretical)
    eff: float           # conversion efficiency (0–1)
    fraction: float      # mass fraction of this reactant in bast


@dataclass
class MassBalanceResult:
    bast_mass: float
    glucose: float
    xylose: float
    residue_cellulose: float
    residue_hemicellulose: float
    residue_lignin: float

    @property
    def total_sugars(self) -> float:
        return self.glucose + self.xylose

    @property
    def total_residue(self) -> float:
        return self.residue_cellulose + self.residue_hemicellulose + self.residue_lignin


def build_bast_reactions(
    cellulose_fraction: float = 0.70,
    hemicellulose_fraction: float = 0.15,
    lignin_fraction: float = 0.15,
    eff_cellulose: float = 0.85,
    eff_hemicellulose: float = 0.70,
) -> tuple[Reaction, Reaction, float]:
    """
    Create reaction objects for bast conversion.
    Returns: (cellulose_rxn, hemicellulose_rxn, lignin_fraction)
    """

    # Cellulose: C6H10O5 + H2O -> C6H12O6
    # MW cellulose unit: 162; MW glucose: 180 -> yield factor 180/162
    cellulose_yield_factor = 180.0 / 162.0

    cellulose_rxn = Reaction(
        name="Cellulose -> Glucose",
        reactant_formula="C6H10O5",
        product_formula="C6H12O6",
        yield_factor=cellulose_yield_factor,
        eff=eff_cellulose,
        fraction=cellulose_fraction,
    )

    # Hemicellulose (xylan): C5H8O4 + H2O -> C5H10O5 (xylose)
    # MW xylan unit: 132; MW xylose: 150 -> yield factor 150/132
    hemicellulose_yield_factor = 150.0 / 132.0

    hemicellulose_rxn = Reaction(
        name="Hemicellulose -> Xylose",
        reactant_formula="C5H8O4",
        product_formula="C5H10O5",
        yield_factor=hemicellulose_yield_factor,
        eff=eff_hemicellulose,
        fraction=hemicellulose_fraction,
    )

    return cellulose_rxn, hemicellulose_rxn, lignin_fraction


def run_mass_balance(
    bast_mass: float = 1.0,
    cellulose_fraction: float = 0.70,
    hemicellulose_fraction: float = 0.15,
    lignin_fraction: float = 0.15,
    eff_cellulose: float = 0.85,
    eff_hemicellulose: float = 0.70,
) -> MassBalanceResult:
    """
    Compute mass balance for bast conversion to sugars.
    """

    cellulose_rxn, hemicellulose_rxn, lignin_frac = build_bast_reactions(
        cellulose_fraction=cellulose_fraction,
        hemicellulose_fraction=hemicellulose_fraction,
        lignin_fraction=lignin_fraction,
        eff_cellulose=eff_cellulose,
        eff_hemicellulose=eff_hemicellulose,
    )

    # Reactant masses
    m_cellulose = cellulose_rxn.fraction * bast_mass
    m_hemicellulose = hemicellulose_rxn.fraction * bast_mass
    m_lignin = lignin_frac * bast_mass

    # Cellulose -> glucose
    m_glucose_th = m_cellulose * cellulose_rxn.yield_factor
    m_glucose = m_glucose_th * cellulose_rxn.eff
    m_cellulose_unconv = m_cellulose * (1.0 - cellulose_rxn.eff)

    # Hemicellulose -> xylose
    m_xylose_th = m_hemicellulose * hemicellulose_rxn.yield_factor
    m_xylose = m_xylose_th * hemicellulose_rxn.eff
    m_hemicellulose_unconv = m_hemicellulose * (1.0 - hemicellulose_rxn.eff)

    # Lignin residue
    m_lignin_res = m_lignin

    return MassBalanceResult(
        bast_mass=bast_mass,
        glucose=m_glucose,
        xylose=m_xylose,
        residue_cellulose=m_cellulose_unconv,
        residue_hemicellulose=m_hemicellulose_unconv,
        residue_lignin=m_lignin_res,
    )


def print_mass_balance(result: MassBalanceResult) -> None:
    """
    Pretty-print the mass balance.
    """
    print(f"=== Bast Mass Balance (Feed: {result.bast_mass:.3f} kg) ===")
    print(f"Glucose:          {result.glucose:.3f} kg")
    print(f"Xylose:           {result.xylose:.3f} kg")
    print(f"Total sugars:     {result.total_sugars:.3f} kg")
    print()
    print(f"Residue cellulose:{result.residue_cellulose:.3f} kg")
    print(f"Residue hemi:     {result.residue_hemicellulose:.3f} kg")
    print(f"Lignin residue:   {result.residue_lignin:.3f} kg")
    print(f"Total residue:    {result.total_residue:.3f} kg")
    print()
    print(f"Mass out (sugars + residue): {result.total_sugars + result.total_residue:.3f} kg")
    print("Note: mass increase vs feed is water incorporated into sugars.")


if __name__ == "__main__":
    # Example: 1 kg bast, 0.85 cellulose efficiency, 0.70 hemicellulose efficiency
    res = run_mass_balance(
        bast_mass=1.0,
        cellulose_fraction=0.70,
        hemicellulose_fraction=0.15,
        lignin_fraction=0.15,
        eff_cellulose=0.85,
        eff_hemicellulose=0.70,
    )
    print_mass_balance(res)
