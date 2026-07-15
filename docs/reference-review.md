# Reference review

Reviewed on 2026-07-15.

## `newren/git-filter-repo`

Adopted: destructive repository transformations should have strong safety checks, predictable failure behavior, and explicit operator intent rather than silently rewriting a working tree.

Not adopted: history rewriting or `git-filter-repo` as a runtime dependency.

## `copier-org/copier`

Adopted: template/import operations should avoid overwriting existing files by default and should retain machine-readable source state so later updates are reviewable.

Not adopted: templating, questionnaires, Jinja rendering, or a Python package dependency.

## `git/git`

Adopted: clone/fetch an exact immutable commit into a separate directory, check it out detached, and avoid unsafe copy semantics. The importer initializes an isolated repository and fetches only the reviewed commit without tags.

Not adopted: shared object stores, local hard-link clones, or tracking a moving upstream branch.

## Result

The previous floating `git clone` plus `rsync --delete` workflow was replaced with a dependency-free review-only stage. The stage verifies the commit and AGPL license, rejects symlinks, records file digests, and reports conflicts without applying them.
