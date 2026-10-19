# Premetric Structural Unification: Einstein-Form and Free-Scalar Schrödinger Dynamics

**Amos Jay Maley — machine-checked Lean 4 composition**

This repository contains a machine-checked Lean 4 composition deriving **Einstein-form first-response dynamics and calibrated free-scalar Schrödinger dynamics within the AASC Kernel and downstream Kernel-faithful machinery**, through canonical licensing with proved receiver maps, coverage, and shared original preparations.

The unification is structural and premetric: constraint-first Kernel architecture and downstream source-preserving constructions support both receiving branches, and canonical licensing governs their faithful original-use descriptions. The physical structures and analytic hypotheses are supplied by those concrete downstream constructions; licensing does not manufacture them. The result connects the actual canonical licensing assembly to both dynamics endpoints by proved maps and common-source squares.

## The composed proof

The public root is in [KernelFaithfulLicensedEndpoints.lean](composition/src/KernelFaithfulLicensedEndpoints.lean):

```lean
AASCKleinGordon.CanonicalLicensing.
  kernel_faithful_canonical_licensing_to_eh_and_free_schrodinger
    (a : Parameters) (s : ℝ) (Ω : Opens CoordinatePoint) :
    KernelFaithfulLicensedEndpoints a s Ω
```

Its **49 fields are proved conclusions**. Its outer arguments are the declared positive physical parameters, real source parameter, and open coordinate region. No desired endpoint certificate, license, or unverified semantic bridge is passed into the root.

The proof uses the actual canonical Kernel/AMetric/licensing assembly on two constructed original-use tasks. It proves canonical receiver presentations and their stated coverage, then maps those receivers into the retained EH response/source profiles and scalar receiving description. The common map takes a preparation in the invariant original one-particle core together with an independently admitted metric operand. It preserves the quantum preparation, metric operand, complete original records, registered Option-reference answers, and the stated evolved preparation squares.

This is a composed proof with connecting maps, rather than an inference from shared imports. The compiled proof-value audit reaches 66,526 constants and checks seven actual dependencies spanning the constraint-first source, canonical licensing, EH receiving, scalar generator and calibrated comparator, and common reference/evolution maps. [The 49 conclusions](composition/ROOT_CONCLUSIONS.json) and [README claim audit](composition/README_CLAIM_AUDIT.json) link the description to the exact source fields.

| Proved component | Content retained through the maps |
| --- | --- |
| Canonical licensing | Actual Kernel roles, AMetric discipline, five licensing conclusions, nonempty safe regions, and licensed presentations of the stated tasks. |
| EH receiving | Coverage of retained restricted histories, responses and source profiles; same receiver metric, finite action, directional action, original answers, failures and continuation. |
| Einstein-form endpoint | The action-derived geometric source has its same-current-metric representation and unique active Einstein-form coefficients under the proved analytic hypotheses. |
| Free-scalar Schrödinger endpoint | The constructed free Hamiltonian, exact generator, full weak graph/domain, free SSQ1 witness, and actual reference dispersion; calibrated equality for comparators in the declared class. |
| Common original source | Every declared core preparation and admitted metric operand has a licensed presentation with the stated preparation, record, reference and evolution squares. |

## Declared assumptions and extent

`Parameters` supplies positive mass, speed and ℏ. The construction fixes four spacetime and three spatial coordinates, continuum carriers, the declared KG/free branch, and the original Einstein–Hilbert relative action. These choices are explicit downstream data; their values, dimensionality, carriers and action are not selected from bare objecthood alone.

The EH branch uses compact smooth metric-source operands in the original neighborhood with each bounded matrix entry's norm less than 1/16. Its regular Lorentz metric is constructed from the fixed flat Lorentz metric. The receipts retain real κ and Λ with **κ ≠ 0**. The represented source is the geometric action's own first derivative. Coefficient uniqueness applies to that constructed response; it does not select a preferred metric or unique global spacetime. Independently supplied matter matching and an interacting Einstein–scalar solution are additional questions.

The scalar branch is **free**. The exact operator graph/domain is a full spatial Hilbert-space statement, while licensed state coverage and the shared original preparation map concern the declared invariant core. Equality for an arbitrary comparator retains the complete finite scalar differential comparator class and explicit dispersion calibration; the actual reference dispersion is proved. No all-potentials theorem, unrestricted operator exhaustion, general paper-level SSQ1 equivalence, or coverage of every Fock preparation is claimed.

The common source map starts with empty EH histories and preserves its declared core preparations, including the stated evolved original preparations. It does not cover every EH history. EH observe/vary/frame history append and scalar NR time evolution retain distinct meanings; they are not identified as joint metric evolution. The proof establishes structural unification through these receivers and connecting maps, not identification of two complete physical interiors or an interior quantum-gravity theory. It adds no preferred projection or universal metric-interface minimum.

The receiving descriptions are constructed directly on declared continuum carriers, so this construction needs no unproved discretization-to-continuum reconstruction. The separately proved **KG nonrelativistic rest-subtracted limit remains in the analytic chain**. These are distinct statements; no universal continuum-limit solution follows.

## Sources, audits and replay

| Source component | Modules | Audit scope |
| --- | ---: | --- |
| `dynamics/` | 786 | Retained dynamics closure, with its original 42-root fresh audit. |
| `licensing/` | 64 | Retained canonical licensing closure. |
| Shared baseline | 11 identical modules | The union of the two baseline closures has 839 distinct modules. |
| `composition/src/` | 10 production modules + 4 audit modules | The new connecting proof and stage audits. |

The four stage audits inspect **252 compiled declarations**, including generated/private declarations, with **230 exact public axiom reports**. They reject new axioms, opaque/unsafe declarations and sorry terms in their selected declarations. The root's transitive axiom set is `propext`, `Classical.choice`, and `Quot.sound`.

The [retained successor replay](composition/replay-001/REPLAY_RECEIPT.json) freshly rebuilt the ten new production modules and the connected audit. All eleven objects matched the reviewed originals byte for byte, with no errors and sixteen disclosed unused-proof-binder warnings. That run **reused 839 hash-verified baseline dependency objects** and pinned Lean/library binaries; it did not freshly rebuild those 839 modules or bootstrap the compiler/libraries. The exact original [handoff](composition/FINAL_HANDOFF.md), reviews, receipts, logs and workspace replay driver remain unchanged as dated evidence of the private verification phase. Their original private/public-status wording describes that earlier phase; this repository now distributes the composed sources.

The [exported-source relocation replay](composition/packaging-replay/REPLAY_RECEIPT.json) additionally rebuilt the ten production modules and all four audits from the public repository sources. All fourteen objects matched the accepted objects byte for byte; the fresh audits reproduced 252 declaration checks, 230 public axiom reports and the seven required proof dependencies, with no errors and sixteen expected lint warnings. It reused the same 839 verified baseline objects, 183 verified external direct-import objects and pinned compiler. This checks the relocated source package in the existing Windows workspace; it is not an independent clean-machine or full-baseline rebuild.

Run the public source and import checks without Lean or downloads:

```console
python scripts/verify_export.py
python scripts/replay_composition.py --check-only
```

[Reproduction instructions](REPRODUCIBILITY.md) describe the repository-relative replay path, the required separately supplied binaries/cache, and the precise executed checks. [Verification boundaries](TRUST.md) distinguish retained audits, packaging replay, source identity and a clean independent build. The original 44-entry dynamics endpoint ledger remains in `evidence/endpoints/`; its two optional historical declarations remain outside the original fresh 42-root audit and the new composition root.

## Citation and separate artifacts

Use [CITATION.cff](CITATION.cff) and the exact repository commit. The 2,794,959,803-byte private replay archive remains separate, with its original bindings in [ARTIFACTS.json](ARTIFACTS.json); it is neither uploaded here nor a portable runtime release of this composition. The manuscript is maintained separately. No new DOI or Zenodo release is asserted.

The repository retains its MIT [LICENSE](LICENSE) under Amos Jay Maley. [NOTICE.md](NOTICE.md) preserves the source/dependency notices; external dependencies retain their own licenses.
