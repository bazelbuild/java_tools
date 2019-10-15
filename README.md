# Bazel Tools for Java

This is a repository for the tools used by [Bazel](https://bazel.build/) to compile Java.

The source code of the Bazel Tools for Java is currently checked in the [bazel
repository](https://github.com/bazelbuild/bazel). The source code will be moved 
incrementally to this repository.

# Upgrade a Bazel project to use custom java_tools version

To use a specific java_tools release in your Bazel project please add the `http_archive`
definitions in your WORKSPACE file and set the options `--java_toolchain` and/or
`--host_java_toolchain` accordingly. All java_tools releases can be found under
https://github.com/bazelbuild/java_tools/releases.

For example to use java_tools_javac11-v6.0 you can add the following to the WORKSPACE
file:

```
http_archive(
    name = "remote_java_tools_linux",
    sha256 = "37acb8380b1dd6c31fd27a19bf3da821c9b02ee93c6163fce36f070a806516b5",
    urls = [
        "https://mirror.bazel.build/bazel_java_tools/releases/javac11/v6.0/java_tools_javac11_linux-v6.0.zip",
        "https://github.com/bazelbuild/java_tools/releases/download/javac11-v6.0/java_tools_javac11_linux-v6.0.zip",
    ],
)
http_archive(
    name = "remote_java_tools_windows",
    sha256 = "384e138ca58842ea563fb7efbe0cb9c5c381bd4de1f6a31f0256823325f81ccc",
    urls = [
        "https://mirror.bazel.build/bazel_java_tools/releases/javac11/v6.0/java_tools_javac11_windows-v6.0.zip",
        "https://github.com/bazelbuild/java_tools/releases/download/javac11-v6.0/java_tools_javac11_windows-v6.0.zip",
    ],
)
http_archive(
    name = "remote_java_tools_darwin",
    sha256 = "5a9f320c33424262e505151dd5c6903e36678a0f0bbdaae67bcf07f41d8c7cf3",
    urls = [
        "https://mirror.bazel.build/bazel_java_tools/releases/javac11/v6.0/java_tools_javac11_darwin-v6.0.zip",
        "https://github.com/bazelbuild/java_tools/releases/download/javac11-v6.0/java_tools_javac11_darwin-v6.0.zip",
    ],
)
```

and set the command line options according to the OS:

```
  --java_toolchain=@remote_java_tools_linux//:toolchain \
  --host_java_toolchain=@remote_java_tools_linux//:toolchain
```

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
