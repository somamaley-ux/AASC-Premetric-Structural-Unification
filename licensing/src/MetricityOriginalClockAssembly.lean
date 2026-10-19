import MetricityOriginalUseAssembly
import MetricityOriginalClockLicenseReceipt

/-! The existing occupied clock, now received by all five licensing properties.
The supplied descriptor must denote the actual complete original clock meaning;
a distance-sector tag alone is not accepted as its interpretation. The clock's
original flat-metric/action/finite-dimensional hypotheses remain unchanged. -/
namespace AASCMetricityClockAssembly
noncomputable section
set_option autoImplicit false
open AASCMetricConstruction
open AASCMetricityOrderAudit
open AASCMetricityLicensingConstruction
open AASCMetricityOriginalAssembly
open AASCMetricityClockLicenseReceipt
open AASC.KernelReference
variable {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [Nontrivial E]

structure ClockOriginalGround (E : Type) where
  start : ℝ
  finish : ℝ
  claimed : ℝ
  marked : ℝ → Fin 2 × SRNativeClockState E

structure CompleteClockMeaning (E : Type) where
  intervalAnswer : SRNativeClockUse E → ℝ
  originalDomain : SRNativeClockUse E → Prop
  everyMarkedRecord : SRNativeClockUse E → ℝ → Fin 2 × SRNativeClockState E
  everyDeclaredRedescription : SRNativeClockUse E → ℝ → SRNativeClockUse E

def sourceClockMeaning (eta : ℝ) : CompleteClockMeaning E :=
  ⟨srNativeClockActualInterval eta,srNativeClockUseValid eta,
    fun c sigma => srNativeCoastingMarkedRecord eta c.record sigma,
    fun c h => srNativeClockUseRedescription eta h c⟩

def sourceClockGround (eta : ℝ) (c : SRNativeClockUse E) : ClockOriginalGround E :=
  ⟨c.start,c.finish,c.claimed,fun sigma => srNativeCoastingMarkedRecord eta c.record sigma⟩

theorem clock_redescription_retains_complete_original_ground (eta h : ℝ) (c : SRNativeClockUse E) :
    sourceClockGround eta (srNativeClockUseRedescription eta h c)=sourceClockGround eta c := by
  apply congrArg (fun marked => (⟨c.start,c.finish,c.claimed,marked⟩ : ClockOriginalGround E))
  funext sigma
  exact sr_native_clock_redescription_preserves_every_original_marked_record eta h c.record sigma

def sourceClockAnswerIncidence (eta : ℝ) (ground : ClockOriginalGround E) :
    (q : Unit ⊕ ℝ) → ProfileValue (fun _ : ℝ => Fin 2 × SRNativeClockState E) (CompleteClockMeaning E) q → Prop
  | .inl _ => fun meaning => meaning=sourceClockMeaning eta
  | .inr sigma => fun answer => answer=ground.marked sigma

def originalClockTask (original : DescriptorSector → Type)
    (duration : original .distance)
    (denotes : FullDescriptorFamily original → CompleteClockMeaning E) (eta : ℝ) :
    OriginalMetricTask (SRNativeClockUse E) (SRNativeClockUse E) (ClockOriginalGround E)
      (FullDescriptorFamily original) ℝ Empty ℝ (fun _ => Fin 2 × SRNativeClockState E)
      (SRNativeClockUse E) (CompleteClockMeaning E) Unit (ClockOriginalGround E) where
  act := id
  ground := sourceClockGround eta
  descriptor := fun _ => ⟨.distance,duration⟩
  descriptorMeaning := denotes
  answers := fun c sigma => srNativeCoastingMarkedRecord eta c.record sigma
  qualification := fun ground witness => sourceClockGround eta witness=ground ∧ srNativeClockUseValid eta witness
  originalAnswer := sourceClockAnswerIncidence eta
  originalLocal := srNativeClockUseValid eta
  redescription := fun c d => ∃ h,d=srNativeClockUseRedescription eta h c
  redEdge := originalClockTransition eta
  contEdge := fun _ t _ => nomatch t
  redOriginalWarrant := originalClockEdgeWarrant eta
  contOriginalWarrant := fun _ t _ => nomatch t
  context := fun _ => ()
  boundaryWork := id

omit [FiniteDimensional ℝ E] [Nontrivial E] in
theorem original_clock_answer_relation_is_determinate
    (original : DescriptorSector → Type) (duration : original .distance)
    (denotes : FullDescriptorFamily original → CompleteClockMeaning E) (eta : ℝ) :
    DependentConservation.Determinate (originalClockTask original duration denotes eta).originalAnswer := by
  intro ground q x y hx hy
  cases q with
  | inl u => exact hx.trans hy.symm
  | inr sigma => exact hx.trans hy.symm

omit [FiniteDimensional ℝ E] [Nontrivial E] in
theorem original_clock_valid_record_passes_local_tests
    (original : DescriptorSector → Type) (duration : original .distance)
    (denotes : FullDescriptorFamily original → CompleteClockMeaning E) (eta : ℝ)
    (interpretation : denotes ⟨.distance,duration⟩=sourceClockMeaning eta)
    (c : SRNativeClockUse E) (valid : srNativeClockUseValid eta c) :
    originalLocalTest (originalClockTask original duration denotes eta) c := by
  refine ⟨⟨c,rfl,valid⟩,?_,valid,?_⟩
  · intro q
    cases q with
    | inl u => exact interpretation
    | inr sigma => rfl
  · rintro d ⟨h,rfl⟩
    exact ⟨h,srNativeClockUseRedescription eta h c,rfl,rfl⟩

theorem occupied_clock_original_valid_region_is_postfixed
    (original : DescriptorSector → Type) (duration : original .distance)
    (denotes : FullDescriptorFamily original → CompleteClockMeaning E) (eta : ℝ)
    (interpretation : denotes ⟨.distance,duration⟩=sourceClockMeaning eta) :
    {c | srNativeClockUseValid eta c} ⊆ originalSafetyOperator
      (originalClockTask original duration denotes eta) {c | srNativeClockUseValid eta c} := by
  intro c valid
  refine ⟨original_clock_valid_record_passes_local_tests original duration denotes eta interpretation c valid,?_⟩
  intro t d edge
  cases t with
  | inl h =>
    have old := original_occupied_clock_valid_region_is_sound (E:=E) eta c valid
    obtain ⟨warrant,dvalid⟩ := old.2 h d edge
    have same : sourceClockGround eta d=sourceClockGround eta c := by
      change d=srNativeClockUseRedescription eta h c at edge
      rw [edge]
      exact clock_redescription_retains_complete_original_ground eta h c
    exact ⟨⟨warrant,same⟩,dvalid⟩
  | inr impossible => exact nomatch impossible

omit [FiniteDimensional ℝ E] [Nontrivial E] in
theorem occupied_clock_receives_all_five_licensing_properties
    (original : DescriptorSector → Type) (duration : original .distance)
    (denotes : FullDescriptorFamily original → CompleteClockMeaning E) (eta : ℝ) :
    FiveLicensingConclusions (originalClockTask original duration denotes eta) :=
  canonical_original_use_construction_proves_L1_through_L5 _
    (original_clock_answer_relation_is_determinate original duration denotes eta)

theorem occupied_interpreted_duration_has_actual_canonical_license
    (original : DescriptorSector → Type) (duration : original .distance)
    (denotes : FullDescriptorFamily original → CompleteClockMeaning E) (eta : ℝ)
    (interpretation : denotes ⟨.distance,duration⟩=sourceClockMeaning eta) (positive : 0<eta) :
    ∃ c,constructedLicensing (originalClockTask original duration denotes eta) c ⟨.distance,duration⟩ := by
  obtain ⟨c,hc⟩ := sr_native_physical_rest_duration_safe_region_is_nonempty (E:=E) eta positive
  have valid := (sr_native_clock_greatest_original_safe_region_computed eta c).mp hc
  exact ⟨c,canonical_licensing_contains_every_original_sound_region _ _
    (occupied_clock_original_valid_region_is_postfixed original duration denotes eta interpretation) c valid⟩

omit [FiniteDimensional ℝ E] [Nontrivial E] in
theorem clock_license_forces_actual_complete_descriptor_meaning
    (original : DescriptorSector → Type) (duration : original .distance)
    (denotes : FullDescriptorFamily original → CompleteClockMeaning E) (eta : ℝ)
    (c : SRNativeClockUse E) (m : FullDescriptorFamily original)
    (licensed : constructedLicensing (originalClockTask original duration denotes eta) c m) :
    denotes m=sourceClockMeaning eta := by
  obtain ⟨record,safe,_,hm⟩ := licensed
  have answer := (safe record Relation.ReflTransGen.refl).1.2.1 (.inl ())
  change denotes ((originalClockTask original duration denotes eta).descriptor record)=sourceClockMeaning eta at answer
  rw [hm] at answer
  exact answer

theorem occupied_clock_constructs_actual_public_kernel_and_licensed_interior
    (original : DescriptorSector → Type) (duration : original .distance)
    (denotes : FullDescriptorFamily original → CompleteClockMeaning E) (eta : ℝ)
    (interpretation : denotes ⟨.distance,duration⟩=sourceClockMeaning eta) (positive : 0<eta) :
    let D := originalClockTask original duration denotes eta
    AASC.Instances.KernelPaper.Manuscript.DerivedKernelRoles
      (ObjecthoodNecessity.canonicalRegime (originalIncidence D)) ∧
    FiveLicensingConclusions D ∧ ∃ c,constructedLicensing D c ⟨.distance,duration⟩ := by
  let D := originalClockTask original duration denotes eta
  obtain ⟨c,licensed⟩ := occupied_interpreted_duration_has_actual_canonical_license
    original duration denotes eta interpretation positive
  obtain ⟨witness,hw⟩ := licensed_original_incidence_witness D c ⟨.distance,duration⟩ licensed
  have assembly := kernel_ametric_canonical_metric_licensing D
    (original_clock_answer_relation_is_determinate original duration denotes eta) ⟨D.ground c,witness,hw⟩
  exact ⟨assembly.1,occupied_clock_receives_all_five_licensing_properties original duration denotes eta,c,licensed⟩

#print axioms ClockOriginalGround
#print axioms CompleteClockMeaning
#print axioms sourceClockMeaning
#print axioms sourceClockGround
#print axioms clock_redescription_retains_complete_original_ground
#print axioms sourceClockAnswerIncidence
#print axioms originalClockTask
#print axioms original_clock_answer_relation_is_determinate
#print axioms original_clock_valid_record_passes_local_tests
#print axioms occupied_clock_original_valid_region_is_postfixed
#print axioms occupied_clock_receives_all_five_licensing_properties
#print axioms occupied_interpreted_duration_has_actual_canonical_license
#print axioms clock_license_forces_actual_complete_descriptor_meaning
#print axioms occupied_clock_constructs_actual_public_kernel_and_licensed_interior
end
end AASCMetricityClockAssembly
