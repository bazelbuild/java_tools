# Release Process

*Note: This document describes how to release java_tools for a JDK version that
is already tested by Bazel. This document is addressed to trusted members of
the Bazel team who have access to the Buildkite Bazel trusted pipelines and GCP.
If you want to release the Java tools but don’t have these permissions please
contact someone from the Bazel EngProd team (bazel-engprod@google.com).*

The steps below are only meant to be followed as presented in order to release
a new java_tools version. To understand the mechanism behind these steps and for
more details about how the process works, see
[Behind the java_tools release process](behind-the-release.md).

1. Create a new tracking issue for the release in this repository and add the
`release` label. See [#59](https://github.com/bazelbuild/java_tools/issues/59) as
an example.
2. Trigger a new build of the [`java_tools binaries pipeline`](https://buildkite.com/bazel-trusted/java-tools-binaries-java). Set the message field to "java_tools release [version] [rc]". See [example](https://buildkite.com/bazel-trusted/java-tools-binaries-java/builds/189).
3. Identify and set the following environment variables:

  * `COMMIT_HASH` the commit hash where the pipeline was run (see below)
  * `NEW_VERSION` the new version number you’re trying to release (e.g. `11.09`)
  * `RC` the number of the current release candidate

     For example:
     ```
     EXPORT COMMIT_HASH=7bd0ab63a8441c3f3d7f495d09ed2bed38762874
     EXPORT NEW_VERSION=11.09
     EXPORT RC=1
     ```

4. Create a new release candidate by running the command below from the [bazel](https://github.com/bazelbuild/bazel) repo:

    ```
    src/create_java_tools_release.sh \
    --commit_hash $COMMIT_HASH \
    --java_tools_version $NEW_VERSION \
    --rc $RC --release false
    ```

    The script will output the sha256sum of the rc artifacts for linux, darwin
    and windows.
    
    Sample output:
    ```
    $ src/create_java_tools_release.sh --commit_hash 7bd0ab63a8441c3f3d7f495d09ed2bed38762874 --java_tools_version 11.9 --rc 1 --release false

      release_candidates/java/v11.9/java_tools_linux-v11.9-rc1.zip 512582cac5b7ea7974a77b0da4581b21f546c9478f206eedf54687eeac035989
      release_candidates/java/v11.9/java_tools_windows-v11.9-rc1.zip 677ab910046205020fd715489147c2bcfad8a35d9f5d94fdc998d217545bd87a
      release_candidates/java/v11.9/java_tools_darwin-v11.9-rc1.zip b9e962c6a836ba1d7573f2473fab3a897c6370d4c2724bde4017b40932ff4fe4
      release_candidates/java/v11.9/java_tools-v11.9-rc1.zip 5cd59ea6bf938a1efc1e11ea562d37b39c82f76781211b7cd941a2346ea8484d
    ```

5. Create a new bazel Pull Request that updates the `java_tools` archives (file [distdir_deps.bzl](https://github.com/bazelbuild/bazel/blob/master/distdir_deps.bzl)) with the new release candidates. The PR triggers the CI presubmit.  

  * Edit [distdir_deps.bzl](https://github.com/bazelbuild/bazel/blob/master/distdir_deps.bzl) by updating the `archive`, `sha256`, and `urls` fields for `remote_java_tools` with the correct version, rc, sha256sum, and url (see output from step 4)
  
     Example:
     ```
     "archive": "java_tools-v11.9-rc1.zip",
     "sha256": "5cd59ea6bf938a1efc1e11ea562d37b39c82f76781211b7cd941a2346ea8484d",
     "urls": [
         "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v11.9/java_tools-v11.9-rc1.zip",
     ],
     ```
     
  * Repeat for `remote_java_tools_linux`, `remote_java_tools_windows`, and `remote_java_tools_darwin`
  * See [#16865](https://github.com/bazelbuild/bazel/pull/16865) for reference

6. Trigger a new build on Downstream https://buildkite.com/bazel/bazel-at-head-plus-downstream.
   Using `pull/PRNUMBER/head` for the branch.

    1. If the CI finishes successfully:
        - create the release artifacts from the
        release candidate:
        ```
        src/create_java_tools_release.sh \
        --java_tools_version $NEW_VERSION \
        --rc $RC --release true
        ```
        - update the urls of the `http_archive`s in the upgrade PR and send it for
        review.
    2. If the CI finishes unsuccessfully find the reasons why the CI is failing
    and file bugs. After the bugs are fixed start all over again creating the
    next release candidate. This case is highly unlikely because bazel already
    tests the `java_tools` built at head.
