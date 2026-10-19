import NativeClockHilbertSourceComponents
import NativeActionKernelSourceProfile

/-! The existing original-action extraction and actual clock action are reused.
Total metric stationarity derives source matching, conditional on the explicit
geometric first-variation identification. No gravitational action or occupied
solution is manufactured from the desired response. Only straight compact
variation rays are used; no arbitrary-curve/Hadamard claim is made here. -/
namespace AASCSemanticExhaustion
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2400000
open Filter TopologicalSpace MeasureTheory
open scoped Topology BigOperators
variable {Ω : Opens CoordinatePoint}

theorem continuousOn_scalar_source_tests_separate (Ω : Opens CoordinatePoint)
    (f : CoordinatePoint → ℝ) (hf : ContinuousOn f Ω)
    (zero_tests : ∀ ψ : ScalarSourceProbe Ω, (∫ x, f x * ψ x) = 0) :
    ∀ p ∈ Ω, f p = 0 := by
  have hae : ∀ᵐ x, x ∈ (Ω : Set CoordinatePoint) → f x = 0 :=
    Ω.isOpen.ae_eq_zero_of_integral_contDiff_smul_eq_zero
      (hf.locallyIntegrableOn Ω.isOpen.measurableSet) (by
        intro φ hφ hcompact hsupport
        let ψ : ScalarSourceProbe Ω := ⟨φ,hφ,hcompact,hsupport⟩
        simpa only [smul_eq_mul,mul_comm] using zero_tests ψ)
  have hr : f =ᵐ[volume.restrict (Ω : Set CoordinatePoint)] (fun _ => 0) :=
    (ae_restrict_iff' Ω.isOpen.measurableSet).mpr hae
  exact MeasureTheory.Measure.eqOn_open_of_ae_eq hr Ω.isOpen hf continuousOn_const

theorem native_scalar_clock_coefficients_continuousOn (g : MetricField)
    (χ : CoordinatePoint → ℝ) (μ : ℝ) (hg : Continuous g)
    (hχ : ContDiff ℝ 2 χ) (hn : ∀ p ∈ Ω, (g p).det ≠ 0) (i : Fin 10) :
    ContinuousOn (nativeClockSourceCoefficient g (nativeScalarClockGradient χ) χ μ i) Ω := by
  intro p hp
  have hc : ContinuousAt (fun p => 2 * nativeRealClockMetricVariation (g p)
      (nativeClockEntryProbe (sourceSymmetricPair i).2 (sourceSymmetricPair i).1)
      (nativeScalarClockGradient χ p) (χ p) μ) p :=
    continuousAt_const.mul (native_clock_variation_continuousAt g _ _ χ μ
      hg.continuousAt continuousAt_const
      (native_scalar_clock_gradient_continuous χ hχ).continuousAt hχ.continuous.continuousAt
      (hn p hp))
  simpa only [← native_clock_coefficient_is_computed_variation] using hc.continuousWithinAt

/-- The same actual total action supplies both derivatives. No independent
linear response is assigned to the clock action. -/
theorem original_total_action_stationarity_source_balance
    (Sgrav : MetricSourceProbe Ω → ℝ)
    (regular : NativeActionFiniteParamDifferentiable Sgrav)
    (metricLF : ∀ (K : Compacts CoordinatePoint) (hK : (K : Set CoordinatePoint) ⊆ Ω),
      Continuous (nativeActionDirectional Sgrav ∘ TestFunction.ofSupportedIn hK))
    (g : MetricField) (hs : MetricFieldSymmetric g)
    (χ : CoordinatePoint → ℝ) (μ : ℝ) (hg : Continuous g)
    (hχ : ContDiff ℝ 2 χ) (hn : ∀ p ∈ Ω, (g p).det ≠ 0)
    (metric_equation : ∀ h : MetricSourceProbe Ω,
      nativeActionDirectional (fun k => Sgrav k + nativeScalarClockRelativeAction g χ μ k) h = 0) :
    ∀ i ψ, representedMetricSource (nativeTestActionFunctional Sgrav regular metricLF) i ψ +
      representedMetricSource (nativeScalarClockMetricLF g χ μ hg hχ hn) i ψ = 0 := by
  have functional_balance (h : MetricSourceProbe Ω) :
      nativeTestActionFunctional Sgrav regular metricLF h +
        nativeScalarClockMetricLF g χ μ hg hχ hn h = 0 := by
    have hd := (native_action_directional_hasDerivAt Sgrav regular h).add
      (native_scalar_clock_action_derivative_constructed g hs χ μ hg hχ hn h)
    have hv := hd.deriv
    change nativeActionDirectional (fun k => Sgrav k + nativeScalarClockRelativeAction g χ μ k) h =
      nativeActionDirectional Sgrav h + nativeScalarClockMetricLF g χ μ hg hχ hn h at hv
    change nativeActionDirectional Sgrav h + nativeScalarClockMetricLF g χ μ hg hχ hn h = 0
    rw [← hv,metric_equation]
  intro i ψ
  change (2 / symmetricSourceWeight i) *
      nativeTestActionFunctional Sgrav regular metricLF (sourceTestInsertion i ψ) +
    (2 / symmetricSourceWeight i) *
      nativeScalarClockMetricLF g χ μ hg hχ hn (sourceTestInsertion i ψ) = 0
  rw [← mul_add,functional_balance,mul_zero]

theorem raised_source_tensor_density_smul (g T : MetricField) (κ : ℝ) :
    raisedSourceTensorDensity g (κ • T) = κ • raisedSourceTensorDensity g T := by
  funext p a b
  change coordinateVolumeDensity g p *
    (∑ i : Fin 4, ∑ j : Fin 4, (g p)⁻¹ a i * (g p)⁻¹ b j * (κ * T p i j)) =
      κ * (coordinateVolumeDensity g p *
        (∑ i : Fin 4, ∑ j : Fin 4, (g p)⁻¹ a i * (g p)⁻¹ b j * T p i j))
  simp_rw [show ∀ i j, (g p)⁻¹ a i * (g p)⁻¹ b j * (κ * T p i j) =
    κ * ((g p)⁻¹ a i * (g p)⁻¹ b j * T p i j) by intros; ring]
  simp only [← Finset.mul_sum]
  ring

/-- Nonzero Lorentzian volume and raising with this same metric are injective.
This is tensor recovery, not existence or uniqueness of a spacetime metric. -/
theorem raised_source_tensor_density_point_injective (g : MetricField)
    (hs : MetricFieldSymmetric g) (p : CoordinatePoint) (negative : (g p).det < 0)
    (E T : MetricField)
    (equal_density : raisedSourceTensorDensity g E p = raisedSourceTensorDensity g T p) :
    E p = T p := by
  have hG : (g p).transpose = g p := by ext a b; exact hs p b a
  have hB : (g p)⁻¹.transpose = (g p)⁻¹ := by rw [Matrix.transpose_nonsing_inv,hG]
  have hv : coordinateVolumeDensity g p ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.mpr (neg_pos.mpr negative))
  have hraise : (g p)⁻¹ * E p * (g p)⁻¹ = (g p)⁻¹ * T p * (g p)⁻¹ := by
    ext a b
    have hh := congrArg (fun M : Tensor2 => M a b) equal_density
    simp only [raisedSourceTensorDensity] at hh
    have hc := mul_left_cancel₀ hv hh
    simpa only [native_raise_source_matrix_identity _ _ hB] using hc
  have hunit : IsUnit (g p).det := isUnit_iff_ne_zero.mpr (ne_of_lt negative)
  have lowered := congrArg (fun M : Tensor2 => g p * M * g p) hraise
  simpa only [← Matrix.mul_assoc,Matrix.mul_nonsing_inv,Matrix.one_mul,
    Matrix.nonsing_inv_mul_cancel_right, hunit] using lowered

/-- Explicit geometric receipt: the ORIGINAL geometric action's constructed
source has normalized all-test density E. Total metric stationarity then
forces E = κ T_clock on Ω. The receipt is not proved by naming an action,
choosing E to be Einstein, or constructing a linear action from E. -/
theorem original_total_action_implies_scalar_clock_matching
    (Sgrav : MetricSourceProbe Ω → ℝ)
    (regular : NativeActionFiniteParamDifferentiable Sgrav)
    (metricLF : ∀ (K : Compacts CoordinatePoint) (hK : (K : Set CoordinatePoint) ⊆ Ω),
      Continuous (nativeActionDirectional Sgrav ∘ TestFunction.ofSupportedIn hK))
    (g : MetricField) (hs : MetricFieldSymmetric g)
    (χ : CoordinatePoint → ℝ) (μ κ : ℝ) (hg : Continuous g)
    (hχ : ContDiff ℝ 2 χ) (hn : ∀ p ∈ Ω, (g p).det ≠ 0)
    (frames : ∀ p ∈ Ω, ∃ B : CoordinatePoint ≃L[ℝ] CoordinatePoint, LorentzFrameAt g p B)
    (E : MetricField) (symmetric : MetricFieldSymmetric E)
    (density_regular : ∀ i, ContinuousOn (sourceDensityCoordinates (raisedSourceTensorDensity g E) i) Ω)
    (geometric_variation : ∀ i (ψ : ScalarSourceProbe Ω),
      (-κ) * representedMetricSource (nativeTestActionFunctional Sgrav regular metricLF) i ψ =
        ∫ p, sourceDensityCoordinates (raisedSourceTensorDensity g E) i p * ψ p)
    (metric_equation : ∀ h : MetricSourceProbe Ω,
      nativeActionDirectional (fun k => Sgrav k + nativeScalarClockRelativeAction g χ μ k) h = 0) :
    ∀ p ∈ Ω, E p = (κ • scalarFieldStress g χ μ) p := by
  have balance := original_total_action_stationarity_source_balance Sgrav regular metricLF
    g hs χ μ hg hχ hn metric_equation
  have coordinates (i : Fin 10) : ∀ p ∈ Ω,
      sourceDensityCoordinates (raisedSourceTensorDensity g E) i p =
        κ * nativeClockSourceCoefficient g (nativeScalarClockGradient χ) χ μ i p := by
    have hc := native_scalar_clock_coefficients_continuousOn g χ μ hg hχ hn i
    have hf : ContinuousOn (fun p => sourceDensityCoordinates (raisedSourceTensorDensity g E) i p -
        κ * nativeClockSourceCoefficient g (nativeScalarClockGradient χ) χ μ i p) Ω :=
      (density_regular i).sub (continuousOn_const.mul hc)
    have hz := continuousOn_scalar_source_tests_separate Ω _ hf (by
      intro ψ
      have hE := native_locally_integrable_test_product _
        ((density_regular i).locallyIntegrableOn Ω.isOpen.measurableSet) ψ
      have hT := native_locally_integrable_test_product _
        (hc.locallyIntegrableOn Ω.isOpen.measurableSet) ψ
      simp_rw [sub_mul,mul_assoc]
      rw [integral_sub hE (hT.const_mul κ),integral_const_mul,
        ← geometric_variation,← native_clock_constructed_source_integral_components
          g (nativeScalarClockGradient χ) χ μ hg
          (native_scalar_clock_gradient_continuous χ hχ) hχ.continuous hn]
      have hb := balance i ψ
      change _ + representedMetricSource (nativeClockMetricLF g
        (nativeScalarClockGradient χ) χ μ hg (native_scalar_clock_gradient_continuous χ hχ)
        hχ.continuous hn) i ψ = 0 at hb
      linear_combination -κ * hb)
    intro p hp
    exact sub_eq_zero.mp (hz p hp)
  have hT : MetricFieldSymmetric (scalarFieldStress g χ μ) := by
    intro p a b
    simp only [scalarFieldStress,hs p a b]
    ring
  have hscaled : MetricFieldSymmetric (κ • scalarFieldStress g χ μ) := by
    intro p a b
    change κ * scalarFieldStress g χ μ p a b = κ * scalarFieldStress g χ μ p b a
    rw [hT p a b]
  intro p hp
  obtain ⟨B,hB⟩ := frames p hp
  apply raised_source_tensor_density_point_injective g hs p
    (native_lorentz_frame_determinant_negative g p B hB) E (κ • scalarFieldStress g χ μ)
  have hrE := source_density_coordinates_recover _ (raised_source_tensor_density_symmetric g E symmetric)
  have hrT := source_density_coordinates_recover _ (raised_source_tensor_density_symmetric g _ hscaled)
  ext a b
  have he := congrArg (fun t : MetricField => t p a b) hrE
  have ht := congrArg (fun t : MetricField => t p a b) hrT
  dsimp only at he ht
  rw [← he,← ht,raised_source_tensor_density_smul]
  exact (coordinates _ p hp).trans (by
    rw [native_clock_coefficient_is_actual_raised_density g hs χ μ p B hB]
    rfl)

#print axioms continuousOn_scalar_source_tests_separate
#print axioms native_scalar_clock_coefficients_continuousOn
#print axioms original_total_action_stationarity_source_balance
#print axioms raised_source_tensor_density_smul
#print axioms raised_source_tensor_density_point_injective
#print axioms original_total_action_implies_scalar_clock_matching
end
end AASCSemanticExhaustion
