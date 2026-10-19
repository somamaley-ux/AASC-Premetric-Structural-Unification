# Composed canonical licensing to both dynamics endpoints

The ten production sources in `src/` implement the actual canonical-licensing,
EH/scalar receiver, common-preparation and composed-endpoint proof. Four
additional `Stage*Audit.lean` sources contain the compiled declaration/axiom
audits. Every copied source, receipt, review and log retains its accepted bytes.

The repository [README](../README.md) gives the mathematical result and its
declared scope. `ROOT_CONCLUSIONS.json` records all 49 conclusion fields and
their proof assignments. `README_CLAIM_AUDIT.json` records which exact fields
support each mathematical summary.

`EXPORT_BINDINGS.json` is the operational, repository-relative index: 839
baseline modules are resolved to `../dynamics/src/` and `../licensing/src/`,
including 11 byte-identical shared modules, followed by the ten production
and four audit modules. It pins source hashes, accepted object hashes, direct
imports, 183 external direct-import object identities and expected audit counts.
External objects, the baseline binary cache and the compiler are not in Git.

Use the public runner from the repository root:

```console
python scripts/replay_composition.py --check-only
python scripts/replay_composition.py --lean PATH_TO_LEAN --baseline-cache PATH_TO_CACHE --library-root FIRST_LIBRARY_ROOT --library-root NEXT_LIBRARY_ROOT --output NEW_DIRECTORY
```

Repeat `--library-root` in the required Lean import-search order. All roots
must already exist. The runner verifies the pinned compiler, all 839 accepted
cache objects and all 183 direct external imports before compiling the ten
production modules and four audits into a new directory. It checks each direct
import's resolved path and hash, all new object identities, audit counts and
proof dependencies, then rechecks the pinned inputs and outputs. It does not
download dependencies or mutate accepted sources.

`--preflight` checks the supplied binaries without compiling or writing.
`--full-local` replaces baseline-cache reuse by rebuilding all 839 baseline
sources as well; it still requires the pinned compiler and external binaries.
That full-local mode has not been executed for this export. The strict object
comparison is tied to the retained Windows runtime and libraries; a different
platform/runtime requires its own checked build procedure and receipt.

The original `DEPENDENCIES.json`, `replay_connected.py`, build receipts and
`replay-001/` records are historical, workspace-bound evidence. Their absolute
paths and private-status notes have not been rewritten into fictitious portable
receipts. The original driver expects the private workspace's `baseline-src/`,
cache, binaries and frozen attempts; use the public runner above for relocated
inputs. `COPY_PROVENANCE.json` lists every exact retained text file and every
accepted compiled object deliberately not distributed. The parent acceptance
seal therefore retains hash references to binary files absent from this source
repository; the public verifier checks the published subset, not their presence.

See [REPRODUCIBILITY.md](../REPRODUCIBILITY.md) for executed-check evidence and
the distinction between this source package and a self-contained runtime archive.
