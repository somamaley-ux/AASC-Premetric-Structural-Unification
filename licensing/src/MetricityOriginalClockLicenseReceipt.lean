import MetricityCanonicalLicensingInterface
import SRNativeClockLicensing

/-! Attach the already constructed occupied coasting clock to the new
canonical receiver. All real source redescriptions and marked times remain.
This is a positive license for the original clock task, not a new physical
first-interface assertion or a derivation of its model metric from licensing. -/
namespace AASCMetricityClockLicenseReceipt
noncomputable section
set_option autoImplicit false
open AASCMetricConstruction
open AASCMetricityOrderAudit
open AASCMetricityLicensingConstruction
variable {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [Nontrivial E]

def originalClockTransition (eta : ℝ) (c : SRNativeClockUse E) (h : ℝ)
    (d : SRNativeClockUse E) : Prop := d = srNativeClockUseRedescription eta h c

def originalClockEdgeWarrant (eta : ℝ) (c : SRNativeClockUse E) (_ : ℝ)
    (d : SRNativeClockUse E) : Prop :=
  (srNativeClockUseValid eta d ↔ srNativeClockUseValid eta c) ∧
  d.start=c.start ∧ d.finish=c.finish ∧ d.claimed=c.claimed ∧
  ∀ sigma : ℝ, srNativeCoastingMarkedRecord eta d.record sigma =
    srNativeCoastingMarkedRecord eta c.record sigma

theorem original_occupied_clock_valid_region_is_sound (eta : ℝ) :
    OriginalSoundRegion (srNativeClockUseValid (E:=E) eta)
      (originalClockTransition eta) (originalClockEdgeWarrant eta)
      {c | srNativeClockUseValid eta c} := by
  intro c valid
  refine ⟨valid,?_⟩
  intro h d edge
  subst d
  have hv := sr_native_clock_original_use_domain_and_answer_preserved eta h c
  exact ⟨⟨hv,rfl,rfl,rfl,
    fun sigma => sr_native_clock_redescription_preserves_every_original_marked_record eta h c.record sigma⟩,
    hv.mpr valid⟩

/-- No sector is removed: duration is a supplied member of the original distance
payload, and the canonical relation remains typed over the full dependent sum. -/
theorem original_occupied_clock_has_canonical_full_family_duration_license
    (original : DescriptorSector → Type) (duration : original .distance)
    (eta : ℝ) (positive : 0 < eta) :
    ∃ c : SRNativeClockUse E,
      canonicalMetricLicense id (fun _ : SRNativeClockUse E =>
        (⟨.distance,duration⟩ : FullDescriptorFamily original))
        (srNativeClockUseValid eta) (originalClockTransition eta)
        (originalClockEdgeWarrant eta) c ⟨.distance,duration⟩ := by
  obtain ⟨c,hc⟩ := sr_native_physical_rest_duration_safe_region_is_nonempty (E:=E) eta positive
  have valid := (sr_native_clock_greatest_original_safe_region_computed eta c).mp hc
  exact ⟨c,c,original_sound_region_is_safe _ _ _ _
    (original_occupied_clock_valid_region_is_sound eta) c valid,rfl,rfl⟩

theorem original_occupied_clock_has_constructed_complete_receiver_point
    (original : DescriptorSector → Type) (duration : original .distance)
    (eta : ℝ) (positive : 0 < eta) :
    Nonempty (CanonicalLicensingReceiver id
      (fun _ : SRNativeClockUse E => (⟨.distance,duration⟩ : FullDescriptorFamily original))
      (fun (c : SRNativeClockUse E) (sigma : ℝ) => srNativeCoastingMarkedRecord eta c.record sigma)
      (srNativeClockUseValid eta) (originalClockTransition eta) (originalClockEdgeWarrant eta)) := by
  obtain ⟨c,license⟩ := original_occupied_clock_has_canonical_full_family_duration_license
    (E:=E) original duration eta positive
  obtain ⟨r,_⟩ := (constructed_receiver_exactly_presents_canonical_license id
    (fun _ : SRNativeClockUse E => (⟨.distance,duration⟩ : FullDescriptorFamily original))
    (fun (c : SRNativeClockUse E) (sigma : ℝ) => srNativeCoastingMarkedRecord eta c.record sigma)
    (srNativeClockUseValid eta) (originalClockTransition eta) (originalClockEdgeWarrant eta)
    c ⟨.distance,duration⟩).mp license
  exact ⟨r⟩

#print axioms originalClockTransition
#print axioms originalClockEdgeWarrant
#print axioms original_occupied_clock_valid_region_is_sound
#print axioms original_occupied_clock_has_canonical_full_family_duration_license
#print axioms original_occupied_clock_has_constructed_complete_receiver_point
end
end AASCMetricityClockLicenseReceipt
