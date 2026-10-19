# Exact endpoint statements and assumptions

These are exact source excerpts from accepted retained modules, with proof bodies omitted for theorem signatures. Definitions and comparator data are shown in full. They are not a pretty-printed expansion of elaborated expressions, and no new theorem is compiled in this reconciliation.

For the EH restricted-source module, the generalized section parameters are `(a : Parameters) (s : ℝ) (Ω : Opens CoordinatePoint)`. Other implicit region/carrier/universe variables remain as stated in the originating source. All full spans, source hashes and line locations are in `EXACT_ENDPOINT_ROOTS.json`.

## Parameters

Module `KGMassShell`, source line 11, SHA256 `99db76d716920482d6b67f8fcd6dda91569abc2dd60c72289e1a744a0c2426c1`.

```lean
structure Parameters where
  mass : ℝ
  speed : ℝ
  hbar : ℝ
  mass_pos : 0 < mass
  speed_pos : 0 < speed
  hbar_pos : 0 < hbar
```

## kernel_necessity_of_partialReference

Module `AASC.Core.KernelNecessity`, source line 82, SHA256 `b0296353e2e91a31a150345adafb7449c015e19626589aea4fbc25795eefe86d`.

```lean
theorem kernel_necessity_of_partialReference
    {Carrier : Type u}
    {Scope : Type v}
    {Value : Type w}
    (R : PartialReferenceSystem Carrier Scope Value)
    (hBoundary : exists carrier scope,
      R.referenceAt carrier scope = none) :
    exists K : Kernel R.incidenceSystem,
      K.ReferenceUnique ∧ K.Nontrivial
```

## kg_family_kernel_objecthood

Module `KGFamilyNondegeneracy`, source line 127, SHA256 `3029cef0216aa89653a9cb93a9594640af44de1574b766aabc922210d238ce6c`.

```lean
theorem kg_family_kernel_objecthood (a : Parameters) (s : ℝ) (Ω : Opens CoordinatePoint) :
    let D := kgRawRegisteredOrbit a s Ω
      (kgFamilyTensor (kgOriginalObject a) (kgOriginalObject a))
    D.references.incidenceSystem.Determinate ∧ D.references.incidenceSystem.Nondegenerate ∧
      D.kernel.ReferenceUnique ∧ D.kernel.Nontrivial ∧
      AASC.Asymmetric D.kernel.StandingToFailure
```

## kg_specific_raw_to_standing_source

Module `KGConstraintStandingSource`, source line 215, SHA256 `1091decff6973d1ea819c986efe06a3f774e5de5c1d8365e5b30e8b075d0e3b5`.

```lean
theorem kg_specific_raw_to_standing_source (a : Parameters) (s : ℝ) (Ω : Opens CoordinatePoint) :
    KGSpecificRawQP a s Ω ∧ KGSpecificStandingSource a s Ω
```

## original_curvature_general_response_has_unique_einstein_form

Module `EinsteinOriginalCurvatureResponse`, source line 78, SHA256 `898c45edb24977642fc1efb74bea9f6f7761d15db8dcfed7d2fe4253172a9c91`.

```lean
theorem original_curvature_general_response_has_unique_einstein_form
    (E : MetricFieldResponse) (natural : RegularLorentzResponseNatural E)
    (locality : RegularLorentzTwoJetLocal E) (original : OriginalCurvatureFirstResponse E)
    (symmetric : ∀ g p,C2LorentzMetricAt g p → ∀ i j,E g p i j=E g p j i)
    (general_closure : GeneralNormalMetricResponseClosure E)
    (active : FullLorentzEnvelopeResponseActive E) :
    ∃! ac : ℝ × ℝ,ac.1≠0 ∧ CoordinateEinsteinResponseForm E ac.1 ac.2
```

## restricted_original_eh_kernel_einstein_receiving

Module `OriginalRestrictedEHKernelReceiving`, source line 116, SHA256 `d9804ac7dca712e11f53f3c6299d6baa5f76b1db1218175cbedfb36ee1eaaca3`.

```lean
theorem restricted_original_eh_kernel_einstein_receiving (κ Λ : ℝ) (coupling : κ ≠ 0) :
    (∀ (q : RestrictedOriginalResponse a s Ω) (i : Fin 10) (φ : ScalarSourceProbe Ω),
      restrictedEHKernelSource a s Ω κ Λ coupling
        (ContextualQuotient.classify (restrictedEHObserve a s Ω κ Λ) q) i φ =
        ∫ p, sourceDensityCoordinates (raisedSourceTensorDensity (restrictedEHMetric a s Ω q)
          (originalEHGeometricResponse κ Λ (restrictedEHMetric a s Ω q))) i p * φ p) ∧
    (∃! ac : ℝ × ℝ, ac.1 ≠ 0 ∧
      CoordinateEinsteinResponseForm (originalEHGeometricResponse κ Λ) ac.1 ac.2)
```

## kg_nr_free_receiving_ssq1

Module `KGNRFreeReceivingAssembly`, source line 15, SHA256 `d9a71147bf539e2622476ba80059f3c94829ead7a320a8e8eb608638239ae489`.

```lean
theorem kg_nr_free_receiving_ssq1
    (a : Parameters) (s : ℝ) (Ω : Opens CoordinatePoint) :
    KGNRReceivingQS a s Ω ∧
    SameScopeQuantumSpatial1 a
      (kgNRSpatialKinetic a)
      (0 : KGSpatialSpace → ℝ)
```

## kg_nr_free_receiving_exact_graph

Module `KGNRFreeReceivingAssembly`, source line 23, SHA256 `d9a71147bf539e2622476ba80059f3c94829ead7a320a8e8eb608638239ae489`.

```lean
theorem kg_nr_free_receiving_exact_graph (a : Parameters) :
    GlobalCharge.ExactGenerator (Translation.coefficient a.hbar)
      (kgNRSpatialFreeFlow a) (kgNRSpatialKinetic a) ∧
    (∀ f g : KGNRSpatialHilbert,(f,g) ∈ (kgNRSpatialKinetic a).graph ↔
      ∀ test : 𝓢(KGSpatialSpace,ℂ),
        (g : KGSpatialDistribution) test =
          (f : KGSpatialDistribution) (kgNRSpatialTestResponse a test)) ∧
    (∀ f : KGNRSpatialHilbert,f ∈ (kgNRPotentialOperator (0 : KGSpatialSpace → ℝ)).domain) ∧
    (kgNRPrincipalCoefficient a = -(a.hbar^2/(2*a.mass)) ∧ kgNRPrincipalCoefficient a < 0)
```

## KGScalarFreeComparator

Module `KGScalarFreeComparator`, source line 13, SHA256 `4a1af48dbb7742703eccbc4d8d58cbbe2fdf84684433871e06489e99a0a800a7`.

```lean
structure KGScalarFreeComparator (H : KGNRSpatialHilbert →ₗ.[ℂ] KGNRSpatialHilbert) where
  data : KGScalarDifferentialData
  response : 𝓢(KGSpatialSpace,ℂ) →L[ℂ] 𝓢(KGSpatialSpace,ℂ)
  response_data : ∀ f x,response f x = kgScalarJetResponse data f x
  complete_graph : ∀ f g,(f,g) ∈ H.graph ↔ ∀ test : 𝓢(KGSpatialSpace,ℂ),
    (g : KGSpatialDistribution) test = (f : KGSpatialDistribution) (response test)
  uniform_principal : ∃ c : ℝ,c ≠ 0 ∧ ∀ x i j,
    data.principal x i j = if i=j then (c : ℂ) else 0
  no_first : ∀ x i,data.first x i = 0
  free_zeroth : ∀ x,data.zeroth x = 0
```

## KGFreeAnchoredDispersionAt

Module `KGScalarComparatorFourier`, source line 118, SHA256 `3bdd60469bca14a142d8f088836de60ae586824487dce771d6fe921b784a266c`.

```lean
def KGFreeAnchoredDispersionAt (a : Parameters)
    {H : KGNRSpatialHilbert →ₗ.[ℂ] KGNRSpatialHilbert} (C : KGScalarFreeComparator H) : Prop :=
  kgScalarPrincipalFourierSymbol C.data kgScalarCalibrationFrequency =
    (kgNRFrequencyKineticEnergy a kgScalarCalibrationFrequency : ℂ)

/-- The full free dispersion ledger of the source; one nonzero frequency
suffices only after the uniform one-parameter normal form is proved. -/
```

## KGFreeInertialDispersion

Module `KGScalarComparatorFourier`, source line 125, SHA256 `3bdd60469bca14a142d8f088836de60ae586824487dce771d6fe921b784a266c`.

```lean
def KGFreeInertialDispersion (a : Parameters)
    {H : KGNRSpatialHilbert →ₗ.[ℂ] KGNRSpatialHilbert} (C : KGScalarFreeComparator H) : Prop :=
  ∀ ξ,kgScalarPrincipalFourierSymbol C.data ξ = (kgNRFrequencyKineticEnergy a ξ : ℂ)
```

## kg_source_free_s36_comparator_endpoint

Module `KGS36FreeComparatorAssembly`, source line 14, SHA256 `2ae99f83a32805ad712a1e708d1094b8bd013917385e5c9b3609da3794ff4396`.

```lean
theorem kg_source_free_s36_comparator_endpoint
    (a : Parameters) (s : ℝ) (Ω : Opens CoordinatePoint) :
    KGNRReceivingQS a s Ω ∧
    KGFreeInertialDispersion a (kgNRFreeComparator a) ∧
    (∀ (H : KGNRSpatialHilbert →ₗ.[ℂ] KGNRSpatialHilbert)
      (C : KGScalarFreeComparator H),
      KGFreeAnchoredDispersionAt a C → H = kgNRSpatialKinetic a) ∧
    (∀ (H : KGNRSpatialHilbert →ₗ.[ℂ] KGNRSpatialHilbert)
      (W : KGScalarSSQ1Witness a H (0 : KGSpatialSpace → ℝ)),
      KGFreeInertialDispersion a (kgScalarFreeComparatorOfSSQ1 a W) →
        H = kgNRSpatialKinetic a)
```

## kg_free_calibrated_comparator_eq

Module `KGScalarComparatorFourier`, source line 147, SHA256 `3bdd60469bca14a142d8f088836de60ae586824487dce771d6fe921b784a266c`.

```lean
theorem kg_free_calibrated_comparator_eq
    (a : Parameters) {H : KGNRSpatialHilbert →ₗ.[ℂ] KGNRSpatialHilbert}
    (C : KGScalarFreeComparator H) (calibration : KGFreeAnchoredDispersionAt a C) :
    H = kgNRSpatialKinetic a
```

## kg_nr_free_comparator_inertial_dispersion

Module `KGScalarComparatorFourier`, source line 166, SHA256 `3bdd60469bca14a142d8f088836de60ae586824487dce771d6fe921b784a266c`.

```lean
theorem kg_nr_free_comparator_inertial_dispersion (a : Parameters) :
    KGFreeInertialDispersion a (kgNRFreeComparator a)
```

## kg_original_core_poisson_extensions_descend

Module `KGOriginalCorePoissonAttachment`, source line 180, SHA256 `e1de9966a8a92fb60a2498ebab72a323ded6c483f0287e5e5513e725df87c830`.

```lean
theorem kg_original_core_poisson_extensions_descend (a : Parameters)
    (u : fockCoreDomain a) (hu : ‖u‖=1) (ℓ η : KGAERRepresentableCovector u)
    (F F' : KGAERRepresentableExtension u hu ℓ.functional)
    (G G' : KGAERRepresentableExtension u hu η.functional) :
    KGAERRepresentableAmbientBracket u hu ℓ.functional η.functional F G=
        KGAERRepresentableBracket u ℓ η ∧
      KGAERRepresentableAmbientBracket u hu ℓ.functional η.functional F' G'=
        KGAERRepresentableBracket u ℓ η
```

## original_total_action_implies_scalar_clock_matching

Module `OriginalTotalActionSourceMatching`, source line 114, SHA256 `5baed47bfc61225675de0c7bf61fb7669ff65f62c79b1fb6c5030ee8a9406573`.

```lean
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
    ∀ p ∈ Ω, E p = (κ • scalarFieldStress g χ μ) p
```
