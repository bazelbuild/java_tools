# Bazel Tools for Java

This is a repository for the tools used by [Bazel](https://bazel.build/) to compile Java.

The source code of the Bazel Tools for Java is currently checked in the [bazel
repository](https://github.com/bazelbuild/bazel). The source code will be moved 
incrementally to this repository.

# Releases

The releases can be found under [java_tools/releases](https://github.com/bazelbuild/java_tools/releases)
starting with java_tools javac11 v4.0.
For previous releases see the issues marked with
[the release label](https://github.com/bazelbuild/java_tools/issues/15).

If you're interested in the release process please see [docs/release.md](docs/release.md)

# Release Schedule

A new `java_tools` for the javac version used by bazel is released monthly.
The first RC should be cut at least 7 days before the bazel release, around the
25th day of the month.

See [upcoming scheduled releases](https://github.com/bazelbuild/java_tools/issues?q=is%3Aopen+is%3Aissue+label%3Arelease).
