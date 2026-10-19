import KGLicensedScalarReceiver
import Lean

open Lean Elab Command
run_cmd do
  let env ← getEnv
  let selected := #["KGCanonicalScalarLicensing", "KGLicensedScalarReceiver"]
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
      throwError "Rejected scalar licensing declaration {name}"
    if isPrivateName name || name.isInternalDetail then continue
    let axioms ← collectAxioms name
    unless axioms.all (fun n => #["Classical.choice", "Quot.sound", "propext"].contains n.toString) do
      throwError "Nonstandard scalar licensing dependency {name}"
    liftIO <| IO.println ("SCALAR_LICENSE_DECLARATION|" ++ (Json.mkObj [
      ("module", toJson moduleName), ("name", toJson name.toString),
      ("axioms", toJson (axioms.map Name.toString))]).compress)
    audited := audited + 1
  liftIO <| IO.println ("SCALAR_LICENSE_CONSTANT_COUNT|" ++ toString count)
  liftIO <| IO.println ("SCALAR_LICENSE_PUBLIC_AUDIT_COUNT|" ++ toString audited)
