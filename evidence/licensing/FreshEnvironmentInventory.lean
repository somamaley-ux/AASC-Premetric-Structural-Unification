import Lean
import AMetricMetricUseRestrictions
import MetricityOriginalUseAssembly
import MetricityOriginalClockAssembly
import MetricityLicensingSemanticChecks
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let selected : Array String := #["AASC.Core.Incidence","AASC.Core.Kernel","AASC.Core.Reference","AASC.Core.Standing","AASC.Core.Continuation","AASC.Core.KernelNecessity","AASC.Core.EndpointUse","AASC.Core.SameScope","AASC.Core.Irreversibility","AASC.Core.DeterminateObjecthood","AASC.Core.TargetAdequacy","AASC.Core.BoundaryClosure","AASC.Core.SameDomainRoutes","AASC.Core.ExhaustionStrength","AASC.Core.AmetricIdentityBoundary","AASC.Core.Exhaustion","AASC.Instances.KernelPaper.Model","AASC.Instances.KernelPaper.Interaction","AASC.Instances.KernelPaper.Endpoint","AASC.Instances.KernelPaper.CurrentLocus","AASC.Instances.KernelPaper.Witness","AASC.Core.ConstraintResidue","AASC.Core.ConstraintClosure","AASC.Core.RoleOccupancy","AASC.Core.RoleOccupancyAction","AASC.Core.RoleOccupancyGeneration","AASC.Instances.KernelPaper.FixedRole","AASC.Instances.KernelPaper.FixedRoleWitness","AASC.Instances.KernelPaper.RoleOccupancyClosure","AASC.Instances.KernelPaper.Manuscript","KernelReference.Foundation","KernelReference.IncidenceNecessity","KernelReference.NecessityRealization","KernelReference.Authorization","KernelReference.ObjecthoodNecessity","KernelReference.DependentConservation","KernelReference.EqualityPatterns","AMetricMetricUseRestrictions","MetricityOriginalOrderScope","KernelReference.ContextualQuotient","MetricityCanonicalLicensingInterface","MetricityOriginalUseAssembly","SRNativeCoastingClockSource","CompletedConeClock","FiniteRestClockSeparation","SourceReachConstruction","SROccupiedRayReach","SRConeClockBody","SRBodyCovariancePositive","SRBodyCovarianceInvariant","SRIsotropicBodyRadial","SRSpatialQuadraticConstruction","SRSpatialCoordinateIndependence","SRLorentzConeReconstruction","SRLorentzNondegeneracy","SRSourceConeLineage","SROccupiedIsotropicRaySource","SRRaySourceConstructedForm","SRNativeFiniteReflectionProtocol","SRConstructedIntervalCalibration","SRNativeClockLicensing","MetricityOriginalClockLicenseReceipt","MetricityOriginalClockAssembly","MetricityLicensingSemanticChecks"]
  let mut constants := 0
  let mut theorems := 0
  for (name, info) in env.constants.toList do
    let some idx := env.getModuleIdxFor? name | continue
    let moduleName := env.header.moduleNames[idx.toNat]!
    unless selected.contains moduleName.toString do continue
    constants := constants + 1
    let forbidden := match info with
      | .axiomInfo _ => true
      | .opaqueInfo _ => true
      | _ => false
    if forbidden || info.isUnsafe || info.type.hasSorry || (info.value? true).any Expr.hasSorry then
      throwError "Rejected project declaration {name} in {moduleName}"
    match info with
    | .thmInfo _ =>
      unless isPrivateName name || name.isInternalDetail do
        liftIO <| IO.println ("THEOREM_JSON|" ++ (Json.mkObj [
          ("name", toJson name.toString), ("module", toJson moduleName.toString)]).compress)
        theorems := theorems + 1
    | _ => pure ()
  liftIO <| IO.println ("INVENTORY_JSON|" ++ (Json.mkObj [
    ("constants", toJson constants), ("theorems", toJson theorems)]).compress)
