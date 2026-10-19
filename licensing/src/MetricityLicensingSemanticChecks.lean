import MetricityOriginalClockAssembly

/-! Semantic checks of load-bearing distinctions, not physical countermodels:
positive qualification is insufficient for changed boundary work; unavailable
required redescription is not vacuous safety; unsafe promised futures fail;
original partial-answer definedness can be retained. -/
namespace AASCMetricityLicensingSemanticChecks
noncomputable section
set_option autoImplicit false
open AASC.KernelReference
open AASCMetricityOrderAudit
open AASCMetricityOriginalAssembly

def boundaryMutationTask : OriginalMetricTask Bool Bool Bool Unit Unit Empty Unit
    (fun _ => Bool) Unit Unit Bool Bool where
  act := id
  ground := id
  descriptor := fun _ => ()
  descriptorMeaning := id
  answers := fun c _ => c
  qualification := fun _ _ => True
  originalAnswer := fun origin q => match q with
    | .inl _ => fun _ => True
    | .inr _ => fun answer => answer=origin
  originalLocal := fun _ => True
  redescription := fun _ _ => True
  redEdge := fun _ _ _ => True
  contEdge := fun _ t _ => nomatch t
  redOriginalWarrant := fun _ _ _ => True
  contOriginalWarrant := fun _ t _ => nomatch t
  context := id
  boundaryWork := id

theorem positive_local_record_does_not_license_boundary_mutation :
    IncidenceNecessity.assess (originalIncidence boundaryMutationTask) false ()=true ∧
    originalLocalTest boundaryMutationTask false ∧
    ¬ constructedLicensing boundaryMutationTask false () := by
  refine ⟨IncidenceNecessity.actual_incidence_gives_positive _ (value:=()) trivial,?_,?_⟩
  · refine ⟨⟨(),trivial⟩,?_,trivial,?_⟩
    · intro q
      cases q <;> trivial
    · intro a' _
      exact ⟨(),a',trivial,rfl⟩
  · rintro ⟨c,safe,rfl,_⟩
    have step := safe_redescription_has_same_original_ground boundaryMutationTask false true () safe trivial
    have impossible : true=false := step.1
    cases impossible

def missingReadinessTask := {boundaryMutationTask with redEdge:=fun _ _ _ => False}

theorem missing_required_redescription_cannot_pass_vacuously (c : Bool) :
    ¬ originalLocalTest missingReadinessTask c := by
  intro hlocal
  obtain ⟨_,_,edge,_⟩ := hlocal.2.2.2 c trivial
  exact edge

theorem no_license_can_hide_missing_required_redescription (c : Bool) :
    ¬ constructedLicensing missingReadinessTask c () := by
  rintro ⟨record,safe,_,_⟩
  exact missing_required_redescription_cannot_pass_vacuously record
    (safe record Relation.ReflTransGen.refl).1

def unsafeFutureTask : OriginalMetricTask Bool Bool Bool Unit Unit Unit Unit
    (fun _ => Bool) Unit Unit Unit Bool where
  act := id
  ground := id
  descriptor := fun _ => ()
  descriptorMeaning := id
  answers := fun c _ => c
  qualification := fun origin _ => origin=true
  originalAnswer := fun origin q => match q with
    | .inl _ => fun _ => True
    | .inr _ => fun answer => answer=origin
  originalLocal := fun _ => True
  redescription := fun _ _ => False
  redEdge := fun _ _ _ => False
  contEdge := fun c _ d => c=true ∧ d=false
  redOriginalWarrant := fun _ _ _ => True
  contOriginalWarrant := fun _ _ _ => True
  context := fun _ => ()
  boundaryWork := id

theorem positive_present_record_does_not_license_unsafe_promised_future :
    originalLocalTest unsafeFutureTask true ∧ ¬ constructedLicensing unsafeFutureTask true () := by
  constructor
  · refine ⟨⟨(),rfl⟩,?_,trivial,?_⟩
    · intro q
      cases q <;> trivial
    · intro _ impossible
      exact False.elim impossible
  · rintro ⟨record,safe,actEq,_⟩
    have recordEq : record=true := actEq
    subst record
    have path : Relation.ReflTransGen (DeclaredStep (declaredOriginalEdge unsafeFutureTask)) true false :=
      .single ⟨.inr (),rfl,rfl⟩
    obtain ⟨_,impossible⟩ := (safe false path).1.1
    cases impossible

def absentOriginalResult (_ : Unit) (_ : Unit) (_ : Bool) : Prop := False

theorem original_absence_is_retained_as_an_answer_not_failed_search :
    DependentConservation.CompleteOutcome absentOriginalResult () () none ∧
    ¬ DependentConservation.CompleteOutcome absentOriginalResult () () (some false) ∧
    DependentConservation.Determinate (DependentConservation.CompleteOutcome absentOriginalResult) := by
  refine ⟨fun _ impossible => impossible,fun impossible => impossible,?_⟩
  exact DependentConservation.completeOutcome_determinate absentOriginalResult
    (fun _ _ _ _ impossible _ => False.elim impossible)

#print axioms boundaryMutationTask
#print axioms positive_local_record_does_not_license_boundary_mutation
#print axioms missingReadinessTask
#print axioms missing_required_redescription_cannot_pass_vacuously
#print axioms no_license_can_hide_missing_required_redescription
#print axioms unsafeFutureTask
#print axioms positive_present_record_does_not_license_unsafe_promised_future
#print axioms absentOriginalResult
#print axioms original_absence_is_retained_as_an_answer_not_failed_search
end
end AASCMetricityLicensingSemanticChecks
