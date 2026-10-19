import KGOriginalMultiplierBinding
import KGOriginalUnitPhase
import KGOriginalBornInterface
import KGPhaseQuotientOriginal
import KGAERRepresentableBracket
import KGPhaseAERGradients

/-! Pointwise representable Poisson descent on the ORIGINAL KG core, with
actual normalized original-ray Hamiltonian and calibrated source bindings.
The H0 derivatives are actual affine/normalized tangent-line derivatives;
no global norm-C1 unbounded Hamiltonian or Poisson algebra is asserted. -/
noncomputable section
set_option autoImplicit false
set_option Elab.async false
set_option maxHeartbeats 1500000
namespace AASCKleinGordon
open KGQuantum W9 TopologicalSpace AASCSemanticExhaustion

local instance (a : Parameters) : (n : ℕ) → NormedSpace ℂ (bosonicHilbertSector a n) :=
  fun _ => inferInstance
local instance (a : Parameters) (n : ℕ) : NormedSpace ℝ (bosonicHilbertSector a n) :=
  NormedSpace.restrictScalars ℝ ℂ (bosonicHilbertSector a n)
local instance (a : Parameters) : NormedSpace ℝ (FockHilbert a) :=
  NormedSpace.restrictScalars ℝ ℂ (FockHilbert a)
local instance (a : Parameters) : NormedSpace ℝ (fockCoreDomain a) :=
  NormedSpace.restrictScalars ℝ ℂ (fockCoreDomain a)
local instance (a : Parameters) : Module ℝ (fockCoreDomain a) :=
  (inferInstance : NormedSpace ℝ (fockCoreDomain a)).toModule
attribute [local irreducible] kgConstraintEnergyOperator kgConstraintEnergyTime
  kgConstraintEnergyVector kgConstraintEnergyH0

private theorem kg_generic_phase_pullback_normalized
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    (f : KGUnitPhaseRay E → ℝ) (u : PureVector E) :
    f ((kgUnitPhaseOriginalEquiv (E := E)).symm (rayMap E u))=
      f (Quotient.mk _ (kgUnitPreparation u)) := by
  rw [← kg_unit_phase_original_normalized u,Equiv.symm_apply_apply]

private theorem kg_generic_homogeneous_normalization
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    (H : E → ℝ) (hom : ∀ (c : ℂ) (u : E),H (c • u)=‖c‖^2*H u)
    (u : PureVector E) : H (kgPreparationUnit u).val=H u.val/‖u.val‖^2 := by
  change H (kgPreparationUnitScalar u • u.val)=_
  rw [hom]
  have hn : ‖kgPreparationUnitScalar u‖=‖u.val‖⁻¹ := by
    simp only [kgPreparationUnitScalar,Complex.norm_real,Real.norm_eq_abs,
      abs_of_nonneg (inv_nonneg.mpr (norm_nonneg u.val))]
  rw [hn]
  simp only [div_eq_mul_inv,inv_pow,mul_comm]

private theorem kg_generic_symmetric_energy_tangent
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    (h : ℝ) (u w : E) (hsym : inner ℂ u w=inner ℂ w u) :
    (inner ℂ u (Translation.coefficient h • w)).re=0 := by
  have hz : (inner ℂ u w).im=0 := by
    have hi := inner_im_symm (𝕜 := ℂ) u w
    change (inner ℂ u w).im=-(inner ℂ w u).im at hi
    rw [← hsym] at hi
    linarith
  have hc : (Translation.coefficient h).re=0 := by
    rw [Translation.coefficient,Complex.div_re]
    simp
  rw [inner_smul_right,Complex.mul_re,hc,hz]
  ring

def kgOriginalH0UnitPhase (a : Parameters) : KGUnitPhaseRay (fockCoreDomain a) → ℝ :=
  Quotient.lift (fun x => kgConstraintEnergyH0 a x.val.val) (by
    rintro x y ⟨c,hc,hxy⟩
    change kgConstraintEnergyH0 a x.val.val=kgConstraintEnergyH0 a y.val.val
    rw [← hxy]
    exact (kg_constraint_energy_h0_phase_invariant a c hc x.val.val).symm)

def kgOriginalH0Ray (a : Parameters) : PhysicalRay (fockCoreDomain a) → ℝ :=
  fun r => kgOriginalH0UnitPhase a ((kgUnitPhaseOriginalEquiv (E := fockCoreDomain a)).symm r)

theorem kg_original_h0_ray_normalized (a : Parameters) (u : PureVector (fockCoreDomain a)) :
    kgOriginalH0Ray a (rayMap _ u)=kgConstraintEnergyH0 a (kgPreparationUnit u).val := by
  exact kg_generic_phase_pullback_normalized (kgOriginalH0UnitPhase a) u

theorem kg_original_h0_ray_unit (a : Parameters) (u : PureVector (fockCoreDomain a))
    (hu : ‖u.val‖=1) : kgOriginalH0Ray a (rayMap _ u)=kgConstraintEnergyH0 a u.val := by
  exact (kg_original_h0_ray_normalized a u).trans
    (congrArg (fun x : PureVector (fockCoreDomain a) => kgConstraintEnergyH0 a x.val)
      (kg_preparation_unit_retraction u hu))

theorem kg_original_h0_ray_ratio (a : Parameters) (u : PureVector (fockCoreDomain a)) :
    kgOriginalH0Ray a (rayMap _ u)=kgConstraintEnergyH0 a u.val/‖u.val‖^2 := by
  exact (kg_original_h0_ray_normalized a u).trans
    (kg_generic_homogeneous_normalization (kgConstraintEnergyH0 a)
      (kg_constraint_energy_h0_smul a) u)

theorem kg_original_h0_ray_source (a : Parameters) (u : PureVector (fockCoreDomain a))
    (hu : ‖u.val‖=1) :
    kgOriginalH0Ray a (rayMap _ u)=(1/(2*a.hbar)) *
      (inner ℂ u.val.val
        (wickOriginalStressEnergyCharge a (wickPositiveCalibratedAmplitude a) u.val)).re := by
  exact (kg_original_h0_ray_unit a u hu).trans
    (kg_original_h0_calibrated_source_quadratic a u.val)

theorem kg_original_h0_vector_tangent (a : Parameters) (u : fockCoreDomain a) :
    kgConstraintEnergyVector a u ∈ phaseAERTangent u := by
  change (inner ℂ u.val (kgConstraintEnergyVector a u).val).re=0
  unfold kgConstraintEnergyVector
  change (inner ℂ u.val (Translation.coefficient a.hbar • (kgConstraintEnergyOperator a u).val)).re=0
  have hs := kg_constraint_energy_operator_symmetric a u u
  change inner ℂ u.val (kgConstraintEnergyOperator a u).val=
    inner ℂ (kgConstraintEnergyOperator a u).val u.val at hs
  exact kg_generic_symmetric_energy_tangent a.hbar u.val (kgConstraintEnergyOperator a u).val hs

def kgOriginalH0Covector (a : Parameters) (u : fockCoreDomain a) (hu : ‖u‖=1) :
    KGAERRepresentableCovector u :=
  KGAERRepresentableCovectorOfTangent u hu (kgConstraintEnergyVector a u)
    (kg_original_h0_vector_tangent a u)

def kgOriginalH0Extension (a : Parameters) (u : fockCoreDomain a) (hu : ‖u‖=1) :
    KGAERRepresentableExtension u hu (kgOriginalH0Covector a u hu).functional :=
  KGAERRepresentableExtensionOfTangent u hu (kgConstraintEnergyVector a u)
    (kg_original_h0_vector_tangent a u)

theorem kg_original_h0_extension_actual (a : Parameters) (u : fockCoreDomain a) (hu : ‖u‖=1) :
    (kgOriginalH0Extension a u hu).vector=kgConstraintEnergyVector a u ∧
      (kgOriginalH0Extension a u hu).functional=phaseAERInnerImCLM (kgConstraintEnergyVector a u) :=
  ⟨rfl,rfl⟩

theorem kg_original_h0_extension_affine_derivative (a : Parameters)
    (u : fockCoreDomain a) (hu : ‖u‖=1) (v : fockCoreDomain a) :
    HasDerivAt (fun t : ℝ => kgConstraintEnergyH0 a (u+(t : ℂ) • v))
      ((kgOriginalH0Extension a u hu).functional v) 0 := by
  change HasDerivAt _ (phaseAEROmega (kgConstraintEnergyVector a u) v) 0
  rw [kg_constraint_energy_h0_hamiltonian]
  exact kg_constraint_energy_directional_derivative a u v

section GenericTangentDerivative
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
local instance : InnerProductSpace ℝ E := InnerProductSpace.rclikeToReal ℂ E

private theorem kg_generic_ray_tangent_derivative
    (H : E → ℝ) (R : PhysicalRay E → ℝ)
    (ratio : ∀ x : PureVector E,R (rayMap E x)=H x.val/‖x.val‖^2)
    (u : PureVector E) (hu : ‖u.val‖=1) (v : E) (hv : v ∈ phaseAERTangent u.val)
    (d : ℝ) (hd : HasDerivAt (fun t : ℝ => H (u.val+(t : ℂ) • v)) d 0) :
    HasDerivAt (fun t : ℝ => R (rayMap E (kgPreparationTangentLine u v hv t))) d 0 := by
  have he : HasDerivAt (fun t : ℝ => H (u.val+t • v)) d 0 := by
    simpa only [RCLike.real_smul_eq_coe_smul (K := ℂ)] using hd
  have hc : HasDerivAt (fun t : ℝ => u.val+t • v) v 0 := by
    simpa only [one_smul] using ((hasDerivAt_id (0 : ℝ)).smul_const v).const_add u.val
  have hn : HasDerivAt (fun t : ℝ => ‖u.val+t • v‖^2) 0 0 := by
    convert hc.norm_sq using 1
    simp only [zero_smul,add_zero]
    change 0=2*(inner ℂ u.val v).re
    rw [(phaseAER_mem_tangent u.val v).mp hv]
    ring
  have hden : ‖u.val+(0 : ℝ) • v‖^2≠0 := by simp [hu]
  have h := he.div hn hden
  have hf : (fun t : ℝ => R (rayMap E (kgPreparationTangentLine u v hv t)))=
      (fun t : ℝ => H (u.val+t • v)/‖u.val+t • v‖^2) := by
    funext t
    exact ratio (kgPreparationTangentLine u v hv t)
  rw [hf]
  simpa only [zero_smul,add_zero,hu,one_pow,mul_one,mul_zero,sub_zero,div_one] using h
end GenericTangentDerivative

theorem kg_original_h0_ray_tangent_derivative (a : Parameters)
    (u : PureVector (fockCoreDomain a)) (hu : ‖u.val‖=1)
    (v : fockCoreDomain a) (hv : v ∈ phaseAERTangent u.val) :
    HasDerivAt (fun t : ℝ => kgOriginalH0Ray a
      (rayMap _ (kgPreparationTangentLine u v hv t)))
      ((kgOriginalH0Extension a u.val hu).functional v) 0 :=
  kg_generic_ray_tangent_derivative (kgConstraintEnergyH0 a) (kgOriginalH0Ray a)
    (kg_original_h0_ray_ratio a) u hu v hv _
    (kg_original_h0_extension_affine_derivative a u.val hu v)

theorem kg_original_born_extension_tangent_derivative (a : Parameters)
    (u z : PureVector (fockCoreDomain a)) (hu : ‖u.val‖=1)
    (v : fockCoreDomain a) (hv : v ∈ phaseAERTangent u.val) :
    HasDerivAt (fun t : ℝ => transitionProbability z (kgPreparationTangentLine u v hv t))
      ((phaseAERBornCanonicalExtension u.val z.val hu).functional v) 0 :=
  phaseAER_born_canonical_extension_derivative u.val z.val hu z.property ⟨v,hv⟩

theorem kg_original_core_poisson_extensions_descend (a : Parameters)
    (u : fockCoreDomain a) (hu : ‖u‖=1) (ℓ η : KGAERRepresentableCovector u)
    (F F' : KGAERRepresentableExtension u hu ℓ.functional)
    (G G' : KGAERRepresentableExtension u hu η.functional) :
    KGAERRepresentableAmbientBracket u hu ℓ.functional η.functional F G=
        KGAERRepresentableBracket u ℓ η ∧
      KGAERRepresentableAmbientBracket u hu ℓ.functional η.functional F' G'=
        KGAERRepresentableBracket u ℓ η :=
  ⟨KGAERRepresentable_bracket_value u hu ℓ η F G,
    KGAERRepresentable_bracket_value u hu ℓ η F' G'⟩

theorem kg_original_core_poisson_actual_chart (a : Parameters)
    (u : fockCoreDomain a) (hu : ‖u‖=1) :
    HasFDerivAt (phaseQuotientRawCoordinate u) (phaseQuotientRealDerivative u) u ∧
      ∀ v : fockCoreDomain a,v ∈ phaseAERTangent u →
        phaseQuotientRealDerivative u v=phaseAERQ u v :=
  phaseQuotient_actual_unit_differential u hu

theorem kg_original_h0_born_extensions_exist (a : Parameters)
    (u z : PureVector (fockCoreDomain a)) (hu : ‖u.val‖=1) :
    ∃ F : KGAERRepresentableExtension u.val hu (kgOriginalH0Covector a u.val hu).functional,
    ∃ G : KGAERRepresentableExtension u.val hu
        (phaseAERBornRepresentableCovector u.val z.val hu).functional,
      F.vector=kgConstraintEnergyVector a u.val ∧
      G.vector=phaseAERBornHamiltonianVector u.val z.val ∧
      G.functional F.vector=KGAERRepresentableBracket u.val
        (kgOriginalH0Covector a u.val hu) (phaseAERBornRepresentableCovector u.val z.val hu) := by
  refine ⟨kgOriginalH0Extension a u.val hu,phaseAERBornCanonicalExtension u.val z.val hu,rfl,rfl,?_⟩
  exact KGAERRepresentable_bracket_value u.val hu
    (kgOriginalH0Covector a u.val hu) (phaseAERBornRepresentableCovector u.val z.val hu) _ _

theorem kg_original_h0_born_extensions_descend (a : Parameters)
    (u z : PureVector (fockCoreDomain a)) (hu : ‖u.val‖=1)
    (F F' : KGAERRepresentableExtension u.val hu (kgOriginalH0Covector a u.val hu).functional)
    (G G' : KGAERRepresentableExtension u.val hu
      (phaseAERBornRepresentableCovector u.val z.val hu).functional) :
    G.functional F.vector=KGAERRepresentableBracket u.val
        (kgOriginalH0Covector a u.val hu) (phaseAERBornRepresentableCovector u.val z.val hu) ∧
      G'.functional F'.vector=KGAERRepresentableBracket u.val
        (kgOriginalH0Covector a u.val hu) (phaseAERBornRepresentableCovector u.val z.val hu) :=
  kg_original_core_poisson_extensions_descend a u.val hu
    (kgOriginalH0Covector a u.val hu) (phaseAERBornRepresentableCovector u.val z.val hu) F F' G G'

end AASCKleinGordon

/- Lean 4.28's optional symbol-frequency exporter times out while indexing
these concrete Fock signatures. Exclude precisely these name components from
automatic premise suggestions. This metadata persists into importers; every
declaration remains subject to normal kernel checking and the independent
all-root axiom audit. No proof, hypothesis or checking budget is changed. -/
run_cmd do
  for component in #[
    "kg_original_h0_ray_normalized", "kg_original_h0_ray_unit",
    "kg_original_h0_ray_ratio", "kg_original_h0_ray_source",
    "kg_original_h0_vector_tangent", "kg_original_h0_extension_actual",
    "kg_original_h0_extension_affine_derivative", "kg_original_h0_ray_tangent_derivative",
    "kg_original_born_extension_tangent_derivative", "kg_original_core_poisson_extensions_descend",
    "kg_original_core_poisson_actual_chart", "kg_original_h0_born_extensions_exist",
    "kg_original_h0_born_extensions_descend"] do
    Lean.modifyEnv fun env => Lean.LibrarySuggestions.nameDenyListExt.addEntry env component
