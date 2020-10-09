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
`release` label. See [#7](https://github.com/bazelbuild/java_tools/issues/7) as
an example.
2. Trigger a new build of the [`java_tools binaries pipeline`](https://buildkite.com/bazel-trusted/java-tools-binaries-java).
3. Identify and set the following environment variables:

  * `COMMIT_HASH` the commit hash where the pipeline was run (see below)
  * `JDK_VERSION` the JDK version for which you want to release `java_tools`
  * `NEW_VERSION` the new version number you’re trying to release (e.g. `3.1`)
  * `RC` the number of the current release candidate

4. Create a new release candidate by running the command below from the bazel repo:

    ```
    src/create_java_tools_release.sh \
    --commit_hash $COMMIT_HASH \
    --java_tools_version $NEW_VERSION \
    --java_version $JDK_VERSION \
    --rc $RC --release false
    ```

    The script will output the sha256sum of the rc artifacts for linux, darwin
    and windows.

5. Create a new bazel Pull Request that updates the `java_tools` `html_archive`s
with the new release candidates. See
[#8302](https://github.com/bazelbuild/bazel/pull/8302) as an example.
The PR triggers the CI presubmit.


6. Trigger a new build on Downstream https://buildkite.com/bazel/bazel-at-head-plus-downstream.
   Using `pulls/PRNUMBER/head` for the branch.

    1. If the CI finishes successfully:
        - create the release artifacts from the
        release candidate:
        ```
        src/create_java_tools_release.sh \
        --java_tools_version $NEW_VERSION \
        --java_version $JDK_VERSION \
        --rc $RC --release true
        ```
        - update the urls of the `http_archive`s in the upgrade PR and send it for
        review.
    2. If the CI finishes unsuccessfully find the reasons why the CI is failing
    and file bugs. After the bugs are fixed start all over again creating the
    next release candidate. This case is highly unlikely because bazel already
    tests the `java_tools` built at head.
