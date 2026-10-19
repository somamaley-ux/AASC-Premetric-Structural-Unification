# AASC Premetric Structural Unification

**Amos Jay Maley · source export dated 19 October 2026**

Pre-metric structural unification and downstream Einstein and Schrödinger dynamics emergence.

This repository contains the Lean sources and selected verification evidence for
the cross-corpus formalization described in *Premetric Structural Unification:
From the AASC Kernel to Einstein-Form and Free-Scalar Dynamics*. It preserves two
separately audited proof closures:

| Project | Local source modules | Checked result |
| --- | ---: | --- |
| `dynamics/` | 786 | Bounded EH metric-source receiving with Einstein-form response classification, and separate calibrated free-scalar receiving. |
| `licensing/` | 64 | Canonical Kernel/AMetric/Lmetric safe-use licensing and its original-clock application. |

The closures share 11 byte-identical source modules, including the ten
`AASC.Core` modules. They are kept as separate projects. The dynamics closure
does not import the canonical licensing assembly; no composed theorem between
that assembly and both dynamics endpoints is asserted.

## Mathematical endpoint

The bounded geometric consumer
`original_curvature_general_response_has_unique_einstein_form` has six premises,
all discharged for the actual action-derived EH response. The root
`restricted_original_eh_kernel_einstein_receiving` connects admitted H+tK action
derivatives, retained response equivalence and canonical Kernel source profiles
to same-current-metric source representation and Einstein-form coefficient
classification. It fixes real kappa and Lambda with kappa nonzero. The response
represents the geometric action's own source, not an independently supplied
matter tensor.

The roots `kg_nr_free_receiving_ssq1`, `kg_nr_free_receiving_exact_graph` and
`kg_source_free_s36_comparator_endpoint` provide the constructed free scalar
receiver, exact generator, complete weak graph/domain and calibrated comparison.
An arbitrary comparator still requires the complete finite scalar differential
class and dispersion calibration. The actual reference dispersion is proved.
Both branches connect to the same constructed KG standing source.

Structural emergence denotes downstream derivation within the stated Kernel-governed constructions; no temporal genesis or unproved coarse-graining limit is asserted.

Common Kernel governance and standing-source origin do not identify branch
quotients or complete interiors. No unrestricted candidate exhaustion, general
paper-level SSQ1 equivalence, all-potentials theorem, preferred projection,
unique spacetime solution or interacting Einstein-scalar solution is claimed.
Optional matter matching requires correct normalization and total stationarity.
Lmetric licensing is neutral among faithful projections.

## Inspect and verify

`manifests/` records every accepted local source's exact SHA256, module name and
direct imports. The accepted source bytes are unchanged. Run the read-only check:

```console
python scripts/verify_export.py
```

The exact 44-entry endpoint ledger and selected statements are in
`evidence/endpoints/`. Only 42 entries are in the fresh dynamics root audit;
the two optional declarations in `historical-source-only/` are historical
source evidence and are outside both project entry points.

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the source-build and retained
replay distinctions, and [TRUST.md](TRUST.md) for the verification boundary.
This source export adds import-only Lake entry points. They are packaging
conveniences, not new audited mathematical roots. The retained audit precedes
these Lake wrappers; a fresh Lake build of this export is not claimed here.

## Electronic formal artifact and citation

The full Windows replay bundle is a separate artifact:
`kernel-downstream-bounded-replay-private-20261018.zip` (2,794,959,803 bytes).
Its archive SHA256 is
`608d4913908dd1911c7778be989d6c36c0069def8508d462edecb4812552f76e`.
The exact bindings are in [ARTIFACTS.json](ARTIFACTS.json). The archive includes
runtime/library binaries, build/import records and the corrected replay driver;
those large binary dependencies are not stored in this Git repository.

This repository is the public source export, not a byte-identical replacement
for the full replay archive. A Zenodo release and DOI are separate subsequent
release steps. No DOI is asserted here. Use `CITATION.cff` and the exact commit
when referring to this source snapshot. The capstone manuscript is maintained
separately; it is not published by this source push.

## License

The repository uses the MIT license selected at creation. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md). External dependencies retain their own licenses.
