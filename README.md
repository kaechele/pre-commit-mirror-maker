# pre-commit-mirror-maker

Scripts for creating mirror repositories that do not have
.pre-commit-hooks.yaml
## IMPORTANT

This is a fork of `pre-commit-mirror-maker`.

First of all some rules:

- Do **not** report bugs in this version or in repositories created by
  this version against the original upstream project.
- Do **not** attempt to open a pull request with code from this repository
  against the upstream project. Please respect the maintainer's wish to not
  have to deal with nasty hacks and fragile workarounds.
- This is a hack, mainly to make my own life easier. It may make yours
  easier as well. Or infinitely harder. Don't blame me. But do let me know
  if something breaks so I can fix it.

Please report issues directly in this repository.

## This fork

It allows to skip pre-release versions or versions matching a given
regex when creating a mirror.

For registries that have semantic annotations for pre-release versions (i.e.
PyPI, Rubygems) this information is used and is generally reliable.
Crates.io does not provide this information but enforces Semantic Versioning.
As a result we can parse the SemVer string to determine if it has a
pre-release component. This should be robust as well.

Which leaves us with NPM. Most packages there usee SemVer but it is not
enforced.
This can lead to two situations:

  1. SemVer parsing fails and the tool bails out. Use `--skip-release-pattern`
     to define your own regex pattern to skip versions. This has the risk of
     missing a pre-release versions which ends up being incorrectly mirrored.
  2. SemVer parses correctly but the package uses the dash notation for
     something else but pre-release versions. In this case these versions will
     incorrectly be detected as pre-release versions.

You might now understand why the author refuses to mitigate this situation
in the upstream project. The approach is brittle at best.

Having said that, I expect this tool to fail in some situations. Do let me
know if this is the case for you.
