# Behind the Release Process

## What is a `java_tools` zip?

A `java_tools` zip is an archive that contains the tools required by Bazel for
building Java targets (e.g. `JavaBuilder`, `Turbine`, `TestRunner`, `ijar`,
`singlejar`, `javac`). Each tool, except `ijar`, `singlejar` and `javac`, are
built from bazel @ HEAD and their deploy jars are archived in `java_tools.zip`.
These deploy jars are platform independent.

`ijar` and `singlejar` are C++ binaries which are also built from bazel @ HEAD.
The built binaries accompanied by their sources are archived into the
`java_tools` zip. The C++ binaries are platform dependent.

`java_tools` archive two javac jars: `java_compiler.jar` and `jdk_compiler.jar`.

## How is a java_tools zip versioned and named?

### javac version

The javac version archived into a `java_tools` zip is reflected in the zip’s
name. For example if a `java_tools` zip contains `java_compiler.jar` and
`jdk_compiler.jar` compiled for javac 9, the `java_tools` name contains `javac9`.

### platform name

The `java_tools` zip is built individually for every supported platform (Ubuntu,
Windows, MacOS) because the ijar and singlejar C++ binaries are platform
dependent. The platform name is reflected into a `java_tools` version.
For example a `java_tools` zip with binaries built on Windows contains `windows`
in its name.

### version

A `java_tools` zip has multiple versions for a certain javac version and platform.
A new `java_tools` version is released when a new feature/bug fix is added. The
version is reflected in the release name.
For example the first version contains `v1.0` and a patch release version can be
`v3.2`.

## Supported javac versions

Currently there are `java_tools` releases with embedded `javac` 9, 10, 11, 12.

## Testing java_tools before the release process

Each `java_tools` zip contains a `java_toolchain` (`//:toolchain`) in its `BUILD`
file. There are java integration tests that run bazel with `--java_toolchain`
and `--host_java_toolchain` pointing to a `java_tools` zip built at HEAD for
each supported javac version.
The tests are defined in [src/test/shell/bazel/BUILD](https://github.com/bazelbuild/bazel/blob/master/src/test/shell/bazel/BUILD)
(`bazel_java_test_jdk` + `$java_version` + `toolchain_head`). The tests run on
Bazel’s CI presubmit and postbumit.

## Manually trying out java_tools before the release process

Build a `java_tools` zip with version *X* by running

```
bazel build //src:java_tools_javaX.zip
```

Define a repository named `local_java_tools` that points to the built zip. For
example:

```
http_archive(
    name = "local_java_tools",
    urls = ["file///path/to/the/java_tools/zip"]
)
```

Build any java target pointing `--java_toolchain/--host_java_toolchain` to
`@local_java_tools//:toolchain`.

## java_tools binaries pipeline

The [java_tools binaries pipeline](https://buildkite.com/bazel-trusted/java-tools-binaries-java)
is a Bazel’s Buildkite trusted pipeline. One needs special permission to access
it. If you want to release the Java tools but don’t have these permissions
please contact the Bazel EngProd team (`bazel-engprod@google.com`).

The configuration file is
[`java_tools-binaries.yml`](https://github.com/bazelbuild/continuous-integration/blob/master/pipelines/java_tools-binaries.yml)
and is maintained by Bazel’s EngProd team.

Once triggered the pipeline starts independent builds on 3 platforms: Centos7,
Windows 10 and MacOS. Each platform build invokes
[`src/upload_all_java_tools.sh`](https://github.com/bazelbuild/bazel/blob/master/src/upload_all_java_tools.sh),
which does the following:

1. Builds `java_tools` zips for each supported java version (9, 10, 11, 12).
2. Runs the java integration tests using the `java_toolchain` in each generated `java_tools`.
3. If all tests are successful uploads each `java_tools` zip to GCP (via
[src/upload_java_tools.sh](https://github.com/bazelbuild/bazel/blob/master/src/upload_java_tools.sh)).
The zips are uploaded under
[bazel-mirror/bazel_java_tools/tmp/build](https://console.cloud.google.com/storage/browser/bazel-mirror/bazel_java_tools/tmp/build)
to a file defined by: the commit hash where the tools were built, the javac version, the platform and the timestamp when they were uploaded:

```
bazel-mirror/bazel_java_tools/tmp/build/${commit_hash}/java${java_version}/java_tools_javac${java_version}_${platform}-${timestamp}.zip
```

## Releasing

Both creating a release candidate and creating a release use the same script
[`src/create_java_tools_release.sh`](https://github.com/bazelbuild/bazel/blob/master/src/create_java_tools_release.sh).
In both cases the script needs to know:

- the javac version archived in the wanted RC/release
- the version number of the java_tools to be released
- the release candidate number (either to be created or to be released)
- the commit hash where the zip was built
- a boolean telling whether it’s creating a release candidate or a release

### Creating a release candidate

To create a release candidate invoke the [`src/create_java_tools_release.sh`](https://github.com/bazelbuild/bazel/blob/master/src/create_java_tools_release.sh) 
script with the parameters set accordingly to the way described above in the
*Releasing* section.

When creating release candidates the script assumes that the `java_tools` pipeline
was already run at the same commit hash passed to the script.

The script identifies where the `java_tools` zip was uploaded on GCP by the
`java_tools` pipeline and copy it under a [GCP `release_candidates` directory](https://console.cloud.google.com/storage/browser/bazel-mirror/bazel_java_tools/release_candidates/):

```
release_candidates/javac${java_version}/v${java_tools_version}/java_tools_javac${java_version}_${platform}-v${java_tools_version}-rc${rc}.zip
```

The uploaded file is the new release candidate. Bazel can be tested by updating
the `java_tools` urls and checksums to the new RC url and its checksum.


### Creating a release

To create a release invoke the [`src/create_java_tools_release.sh`](https://github.com/bazelbuild/bazel/blob/master/src/create_java_tools_release.sh)
script with the parameters set accordingly to the way described above in the
*Releasing*  section. When creating releases the script assumes that a release
candidate with the given number was previously created by the script.

The script identifies where the release candidate with the given number was
uploaded on GCP and copy it under a [GCP `releases` directory](https://console.cloud.google.com/storage/browser/bazel-mirror/bazel_java_tools/releases/):

```
releases/javac${java_version}/v${java_tools_version}/java_tools_javac${java_version}_${platform}-v${java_tools_version}-rc${rc}.zip
```

The uploaded file is the new release. Bazel can be updated to use new release by
updating the `java_tools` urls and checksums to the new release.

