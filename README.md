# Bazel Tools for Java

This is a repository for the tools used by [Bazel](https://bazel.build/) to compile Java.

The source code of the Bazel Tools for Java is currently checked in the [bazel
repository](https://github.com/bazelbuild/bazel). The source code will be moved 
incrementally to this repository.

# Upgrade a Bazel project to use custom java_tools version

To use a specific java_tools release in your Bazel project please add the `http_archive`
definitions in your WORKSPACE file.

For Bazel versions above 4.0.0, use java_tools releases >= v11. No additional options are needed.

For Bazel versions <= 4.0.0 use java_tools releases <= v10 and set the options `--java_toolchain` and/or
`--host_java_toolchain` accordingly. 

All java_tools releases can be found under https://github.com/bazelbuild/java_tools/releases.


# Releases

The releases can be found under [java_tools/releases](https://github.com/bazelbuild/java_tools/releases).
For previous releases see the issues marked with
[the release label](https://github.com/bazelbuild/java_tools/issues?q=label%3Arelease/15).

If you're interested in the release process please see [docs/release.md](docs/release.md)
