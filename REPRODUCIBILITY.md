# Reproduction and source identity

The accepted dynamics source closure consists of 786 modules, and the separate
canonical licensing closure consists of 64 modules. The source manifests bind
each exported file to its retained audited bytes. The verification script checks
those identities and the 11 shared modules without installing anything or
invoking Lean. It also verifies the repository export manifest.

## Ordinary source build

Both independent Lake projects declare Lean 4.28.0 and mathlib revision
`8f9d9cff6bd728b17a24e163c9402775d9e6a365`. Their local source closures include
the Kernel modules actually used, rather than substituting a newer public
Kernel checkout. With an already configured Lean/Lake environment and compatible
mathlib dependencies, build the two projects separately:

```console
cd dynamics
lake build
```

```console
cd licensing
lake build
```

Lake may obtain dependencies if they are not already available. Such an ordinary
build is distinct from the retained offline replay and its imported-object audit.
No new Lake build, dependency fetch or installation was performed to prepare
this source export. The added Lake configurations and import-only entry points
are not themselves part of the historical audit.

## Exact retained Windows replay

The separately retained complete archive supplies its sealed package, copied
Lean/library binaries and `audit-repair/` alongside `package/`. From that full
archive's `audit-repair/` folder, using an existing Python 3.11 or later:

```console
python -B -X utf8 replay.py --check
python -B -X utf8 -u replay.py --run --work-dir C:\short\new-replay --jobs 2
```

Choose a new, nonexistent work directory outside the sealed package. The
corrected driver supersedes the original package README's command. The copies
in `evidence/full-archive-audit-repair/` document that exact procedure but cannot
run without the full archive's sealed package and dependencies. The archive was
not unpacked or rebuilt while preparing this repository.

The retained execution rebuilt all 786 local project modules, then corrected an
inventory parser error and revalidated all source/object/import/log records.
The original failed source and log remain preserved in the full artifact.
The correction renamed an audit-local identifier; mathematical sources and
imports were unchanged. The original audit driver did not pass. The receipt's
507.588-second duration describes the resumed phase, not an end-to-end build.

Original absolute paths in the unchanged provenance and audit records are
historical locations. The relative source manifests are the repository's
operational source index. Raw receipt hashes remain tied to the original
artifact, and are not represented as hashes of a newly executed GitHub build.
