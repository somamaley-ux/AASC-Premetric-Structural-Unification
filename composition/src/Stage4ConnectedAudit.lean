import KernelFaithfulLicensedEndpoints
import Lean

open Lean Elab Command
run_cmd do
  let env ← getEnv
  let selected := #["KGLicensedScalarEndpoint", "KGCommonLicensedPreparation",
    "KGCommonLicensedEvolution", "KernelFaithfulLicensedEndpoints"]
  let mut count := 0
  let mut audited := 0
  for (name, info) in env.constants.toList do
    let some index := env.getModuleIdxFor? name | continue
    let moduleName := env.header.moduleNames[index.toNat]!.toString
    unless selected.contains moduleName do continue
    count := count + 1
    let forbidden := match info with
      | .axiomInfo _ => true
      | .opaqueInfo _ => true
      | _ => false
    if forbidden || info.isUnsafe || info.type.hasSorry || (info.value? true).any Expr.hasSorry then
      throwError "Rejected connected declaration {name}"
    if isPrivateName name || name.isInternalDetail then continue
    let axioms ← collectAxioms name
    unless axioms.all (fun n => #["Classical.choice", "Quot.sound", "propext"].contains n.toString) do
      throwError "Nonstandard connected dependency {name}"
    liftIO <| IO.println ("CONNECTED_DECLARATION|" ++ (Json.mkObj [
      ("module", toJson moduleName), ("name", toJson name.toString),
      ("axioms", toJson (axioms.map Name.toString))]).compress)
    audited := audited + 1
  liftIO <| IO.println ("CONNECTED_CONSTANT_COUNT|" ++ toString count)
  liftIO <| IO.println ("CONNECTED_PUBLIC_AUDIT_COUNT|" ++ toString audited)
  -- Follow actual compiled proof values, including transitive helper proofs.
  let root := ``AASCKleinGordon.CanonicalLicensing.kernel_faithful_canonical_licensing_to_eh_and_free_schrodinger
  let required := #[
    ``AASCKleinGordon.kg_constraint_first_standing_source,
    ``AASCMetricityOriginalAssembly.kernel_ametric_canonical_metric_licensing,
    ``AASCKleinGordon.restricted_original_eh_kernel_einstein_receiving,
    ``AASCKleinGordon.kg_nr_spatial_exact_generator,
    ``AASCKleinGordon.kg_free_calibrated_comparator_eq,
    ``AASCKleinGordon.CanonicalLicensing.common_original_registered_reference_square,
    ``AASCKleinGordon.CanonicalLicensing.common_evolved_original_preparation_square]
  let mut seen : Std.HashSet Name := {}
  let mut todo : List Name := [root]
  while !todo.isEmpty do
    let name := todo.head!
    todo := todo.tail!
    if seen.contains name then continue
    seen := seen.insert name
    let some info := env.find? name | continue
    if let some value := info.value? true then
      for dep in value.getUsedConstants do
        unless seen.contains dep do todo := dep :: todo
  for name in required do
    unless seen.contains name do throwError "Missing actual proof dependency {name}"
    liftIO <| IO.println ("CONNECTED_REQUIRED_PROOF_DEPENDENCY|" ++ name.toString)
  liftIO <| IO.println ("CONNECTED_PROOF_REACHABLE_CONSTANT_COUNT|" ++ toString seen.size)

#print axioms AASCKleinGordon.CanonicalLicensing.kernel_faithful_canonical_licensing_to_eh_and_free_schrodinger
