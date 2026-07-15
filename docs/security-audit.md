# Changed-area security audit

## Fixed

- Removed automatic `rsync --delete` against the repository root.
- Removed fixed shared `/tmp/openmontage-upstream` and backup paths.
- Replaced floating upstream HEAD with an exact reviewed commit lock.
- Added license blob verification and explicit AGPL-3.0 content validation.
- Added clean tracked-tree requirement and a dedicated ignored staging root.
- Rejected upstream symbolic links instead of dereferencing them during copying.
- Added conflict inventory, fork HEAD, provenance, and per-file SHA-256 verification.
- Required explicit `--replace-stage` before deleting an old ignored stage.
- Added regression tests, repository checks, shell validation, and least-privilege CI.

## Residual risks

- The pin proves which source was staged; it does not prove that upstream code is safe. A complete dependency, application, media, network, and secret review is still required before import or execution.
- GitHub Actions are referenced by maintained major tags rather than immutable action SHAs.
- The repository still contains many historical helper scripts and notes. CI compiles/smoke-tests a core set, but importing the upstream application will require its own full test matrix.
- AGPL obligations apply when upstream source is copied, modified, distributed, or offered as a network service. This document is operational guidance, not legal advice.
