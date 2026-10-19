# Reproduction and source identity

The public source union contains 839 distinct baseline modules (786 dynamics
and 64 licensing, with 11 identical shared modules), ten composition production
modules and four composition audit modules. Mathematical source bytes and
retained evidence are preserved. The prior export manifest is retained exactly
at `manifests/export-before-composition.json`.

## Public source checks

With Python 3.11 or later, from the repository root:

```console
python scripts/verify_export.py
python scripts/replay_composition.py --check-only
```

These read-only checks verify repository file identities, the two original
source closures, the composition's exact copied evidence, the 839-module source
union, all direct import names and the 49-field proof assignment inventory.
They do not invoke Lean, fetch dependencies or establish a fresh compilation.

## Composition replay with relocated inputs

`composition/EXPORT_BINDINGS.json` binds repository-relative source paths to
accepted source/object hashes, direct imports and the external object boundary.
The public runner takes explicit paths to an already existing Lean executable,
baseline cache and ordered library roots. It never downloads or installs them.

```console
python scripts/replay_composition.py --lean PATH_TO_LEAN --baseline-cache PATH_TO_839_OBJECT_CACHE --library-root FIRST_LIBRARY_ROOT --library-root NEXT_LIBRARY_ROOT --preflight
python scripts/replay_composition.py --lean PATH_TO_LEAN --baseline-cache PATH_TO_839_OBJECT_CACHE --library-root FIRST_LIBRARY_ROOT --library-root NEXT_LIBRARY_ROOT --output NEW_NONEXISTENT_DIRECTORY
```

Supply all external library roots in their declared namespace resolution order.
The retained order is aesop, batteries, importGraph, LeanSearchClient, mathlib,
NonDegenerateConstructionAndKernelOfAdmissibility, plausible, proofwidgets, Qq,
then the Lean runtime library. The public binding manifest identifies the
original root index for each external import. The runner checks actual
namespace-first resolution and hashes; a similarly named different object is
rejected. The input compiler hash is
`6a66c4a5739fa17146b88ac81bab2bca1924806cac321ddad6b96006dde9c691`.

The default compilation reuses 839 verified baseline objects, freshly rebuilds
the ten production modules and all four audits, checks object byte identity,
audit report counts/axioms, the seven required proof dependencies and final
input/output identities. Outputs and an explicit receipt go only to the new
directory. Choose a location outside the sealed sources.

`--full-local` rebuilds the 839 baseline sources too, in dependency order, while
reusing the same compiler/library binaries. This mode has not been executed
for the public export. Strict object identity is bound to the retained Windows
runtime. Source relocation is distinct from a verified cross-platform build.

## Executed exported-source relocation replay

The public `scripts/replay_composition.py` was executed against the repository-relative source index, the existing pinned compiler/library roots and the 839-object baseline cache, with a new output directory outside the repository. Its exact command arguments, import resolutions, per-module hashes and counts are retained in [the packaging replay receipt](composition/packaging-replay/REPLAY_RECEIPT.json) and companion logs/receipts.

All ten production modules and all four audits were freshly compiled. All fourteen objects were byte-identical to the accepted originals. The audits reproduced 252 compiled declaration checks, 230 public axiom reports, the seven required actual proof dependencies and 66,526 root-reachable constants. There were no errors and sixteen expected unused-proof-binder warnings. All 839 baseline objects and 183 external direct-import objects were hash-verified and reused; no baseline, compiler or external library rebuild was performed. This is a successful relocation of the source package within the existing Windows workspace, not an independent clean-machine or cross-platform build.

## Retained verification evidence

The original four composition stages audited 252 declarations, including
private/generated declarations, with 230 exact public axiom reports. The
retained successor replay in `composition/replay-001/REPLAY_RECEIPT.json`
rebuilt ten new production modules and one connected audit, all eleven objects
byte-identical, with sixteen disclosed unused-proof-binder warnings and no
errors. It reused 839 hash-verified baseline objects and Lean/library binaries.
Its reported 443.431 seconds covers the replay phase, excluding initial input
verification/copying; it is not an end-to-end baseline/bootstrap timing.

The unchanged `composition/replay_connected.py` and original receipts retain
absolute historical paths. They document that workspace execution and expect
its private cache/baseline sources/frozen attempts. They are not silently
relocated executable commands or a self-contained runtime distribution.
`COPY_PROVENANCE.json` lists the retained exact files and the compiled objects
omitted from Git. The original private-status statements are dated evidence;
they do not describe the availability of the newly published sources.

## Original baseline source builds and full archive

The original `dynamics/` and `licensing/` Lake projects retain Lean 4.28.0 and
mathlib revision `8f9d9cff6bd728b17a24e163c9402775d9e6a365`. With an already
configured compatible environment they may be built separately with
`lake build` in each directory. Lake may fetch dependencies. No new Lake
dependency resolution, download, install or compiler/library bootstrap was
performed to prepare this export. Those two packaging entry points predate
the new composition and remain distinct from its public replay runner.

The separate original 2.79 GB archive contains the 786-module dynamics replay
package, copied runtime/libraries and corrected `audit-repair/replay.py`.
From that archive's `audit-repair/`, its retained commands are:

```console
python -B -X utf8 replay.py --check
python -B -X utf8 -u replay.py --run --work-dir C:\short\new-replay --jobs 2
```

The copies under `evidence/full-archive-audit-repair/` require that full private
archive. It does not contain a newly assembled portable runtime bundle of the
composition. The original failed inventory-parser attempt remains preserved;
the correction changed an audit-local identifier, leaving mathematical sources
and imports unchanged. Its 507.588-second receipt describes the resumed phase.
The archive was not unpacked, republished or rebuilt for this update.
