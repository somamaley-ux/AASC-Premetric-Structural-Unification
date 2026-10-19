"""Write a new explicit proposition from exact, already compiled receipt types.

This helper only writes its new named output. It does not execute corpus scripts
or alter sources, receipts, prior objects, or public artifacts.
"""
from pathlib import Path
import json, re, textwrap

HERE = Path(__file__).resolve().parent
target = HERE / 'src/KernelFaithfulLicensedEndpoints.lean'
assert not (HERE / 'build' / target.with_suffix('.olean').name).exists()
groups = [
 ('KGCanonicalMetricLicensing', '', [
   'current_metric_use_constructs_kernel_and_canonical_license']),
 ('KGLicensedEHReceiver', '', [
   'receiver_has_actual_canonical_license', 'present_licensed_history_surjective',
   'licensed_readout_square', 'licensed_response_coverage', 'licensed_source_profile_coverage',
   'licensed_response_continuation_square', 'licensed_readout_continuation_square',
   'licensed_metric_square', 'licensed_action_square', 'licensed_directional_action_square',
   'licensed_original_answer_square', 'licensed_original_first_failure_square',
   'licensed_eh_source_is_original_directional_action', 'licensed_eh_same_metric_representation']),
 ('KGLicensedEHFailure', '', [
   'licensed_original_failure_square', 'licensed_rejected_metric_request_stays_failed']),
 ('KGCanonicalScalarLicensing', '(A : KGNRObject a)', [
   'scalar_use_constructs_kernel_and_canonical_license', 'every_original_scalar_has_canonical_license']),
 ('KGLicensedScalarReceiver', '(A : KGNRObject a)', [
   'present_licensed_scalar_surjective', 'licensed_scalar_meaning_exact',
   'licensed_scalar_state_coverage', 'licensed_scalar_old_reference_square',
   'licensed_scalar_old_complete_record', 'licensed_scalar_continuation_reference',
   'licensed_scalar_continuation_first_failure', 'licensed_scalar_full_continuation_square',
   'licensed_scalar_comparison_reference', 'licensed_scalar_region_reference',
   'licensed_scalar_tensor_original_square', 'licensed_scalar_domain_graph_receipt',
   'licensed_scalar_full_flow_receipt', 'licensed_scalar_exact_generator',
   'licensed_scalar_complete_weak_graph', 'licensed_scalar_calibrated_comparator']),
 ('KGLicensedScalarEndpoint', '(A : KGNRObject a)', [
   'licensed_scalar_free_ssq1', 'licensed_scalar_reference_dispersion',
   'licensed_scalar_zero_potential_full_domain', 'licensed_scalar_ssq1_comparator']),
 ('KGCommonLicensedPreparation', '', [
   'common_original_preparation_square', 'common_original_metric_operand_square',
   'common_original_metric_source_record_square', 'common_original_registered_reference_square']),
 ('KGCommonLicensedEvolution', '', [
   'licensed_scalar_evolved_original_preparation', 'common_evolved_original_preparation_square',
   'common_preparation_covers_declared_core']),
]
out = '''import KGCommonLicensedEvolution
import KGLicensedScalarEndpoint

/-! Constraint-first composed receipts for the declared original source and
its two current licensed receiving endpoints. Every field below is the exact
type of a proved semantic map, coverage, licensing or analytic receipt.

The shared preparation is the declared invariant one-particle core with an
independently admitted metric operand. EH history append and scalar NR time
flow remain distinct. This does not select a metric, assert matter matching,
exhaust the entire original role architecture, or remove the explicitly
quantified comparator calibration. -/
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace AASCKleinGordon.CanonicalLicensing
open AASCSemanticExhaustion KGQuantum W9 TopologicalSpace MeasureTheory CategoryTheory
open AASC.KernelReference AASCMetricityOriginalAssembly AASCMetricityLicensingConstruction
open scoped SchwartzMap
attribute [local instance] Classical.propDecidable KGInnerCarrier.normed KGInnerCarrier.innerSpace

structure KernelFaithfulLicensedEndpoints (a : Parameters) (s : ℝ)
    (Ω : Opens CoordinatePoint) : Prop where
  constraint_first_source : KGSpecificStandingSource a s Ω
  current_free_receiving : KGNRReceivingQS a s Ω
  geometric_einstein_receiving : ∀ (κ Λ : ℝ) (coupling : κ ≠ 0),
    (∃! ac : ℝ × ℝ, ac.1 ≠ 0 ∧
      CoordinateEinsteinResponseForm (originalEHGeometricResponse κ Λ) ac.1 ac.2)
'''
bindings = []
for module, extra, names in groups:
    source = (HERE / 'src' / (module + '.lean')).read_text(encoding='utf-8')
    for name in names:
        begin = source.index('theorem ' + name) + len('theorem ' + name)
        depth = 0
        end = None
        for i in range(begin, len(source)):
            c = source[i]
            if c in '({[': depth += 1
            elif c in ')}]': depth -= 1
            elif source[i:i+2] == ':=' and depth == 0 and not \
                source[source.rfind('\n', begin, i)+1:i].strip().startswith('let '):
                end = i
                break
        assert end is not None, name
        head = source[begin:end].strip()
        # Find the declaration's top-level colon; binder annotations do not count.
        depth = 0
        colon = None
        for i, c in enumerate(head):
            if c in '({[': depth += 1
            elif c in ')}]': depth -= 1
            elif c == ':' and depth == 0:
                colon = i
                break
        assert colon is not None, name
        params = ' '.join(x for x in [extra, head[:colon].strip()] if x)
        typ = textwrap.dedent(head[colon+1:]).strip()
        field = 'receipt_' + name
        out += '\n  ' + field + ' : ' + ('∀ ' + params + ',\n    ' if params else '\n    ')
        out += typ.replace('\n', '\n    ') + '\n'
        bindings.append({'field': field, 'module': module, 'theorem': name, 'extra': extra})
out += '''
theorem kernel_faithful_canonical_licensing_to_eh_and_free_schrodinger
    (a : Parameters) (s : ℝ) (Ω : Opens CoordinatePoint) :
    KernelFaithfulLicensedEndpoints a s Ω where
  constraint_first_source := kg_constraint_first_standing_source a s Ω
  current_free_receiving := kg_nr_receiving_qs_constructed a s Ω
  geometric_einstein_receiving κ Λ coupling :=
    (restricted_original_eh_kernel_einstein_receiving a s Ω κ Λ coupling).2
'''
for row in bindings:
    out += '  ' + row['field'] + ' := ' + row['theorem'] + ' a s Ω\n'
out += '\nend AASCKleinGordon.CanonicalLicensing\n'
target.write_text(out, encoding='utf-8')
(HERE/'ROOT_FIELD_BINDINGS.json').write_text(json.dumps(bindings, indent=2)+'\n', encoding='utf-8')
print('Wrote',len(bindings)+3,'explicit receipt fields to',target)
