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

1. Create a new tracking issue for the release in this repository and add the `release` label. See [#59](https://github.com/bazelbuild/java_tools/issues/59) as an example.
2. Trigger a new build of the [`java_tools binaries pipeline`](https://buildkite.com/bazel-trusted/java-tools-binaries-java). Set the message field to "java_tools release [version] [rc]", and leave the commit field as "HEAD" and branch as "master". See [example](https://buildkite.com/bazel-trusted/java-tools-binaries-java/builds/189).
3. Identify and set the following environment variables:

  * `COMMIT_HASH` the commit hash where the pipeline was run (see below)
  * `NEW_VERSION` the new version number you’re trying to release (e.g. `11.09`)
  * `RC` the number of the current release candidate

     For example:
     ```bash
     export COMMIT_HASH=7bd0ab63a8441c3f3d7f495d09ed2bed38762874
     export NEW_VERSION=11.09
     export RC=1
     ```

4. Create a new release candidate by running the command below from the [bazel](https://github.com/bazelbuild/bazel) repo:

    ```bash
    src/create_java_tools_release.sh \
    --commit_hash $COMMIT_HASH \
    --java_tools_version $NEW_VERSION \
    --rc $RC --release false
    ```

    The script will output the sha256sum of the rc artifacts for linux, darwin
    and windows.
    
    Sample output:
    ```bash
    $ src/create_java_tools_release.sh --commit_hash 7bd0ab63a8441c3f3d7f495d09ed2bed38762874 --java_tools_version 11.9 --rc 1 --release false

      release_candidates/java/v11.9/java_tools_linux-v11.9-rc1.zip 512582cac5b7ea7974a77b0da4581b21f546c9478f206eedf54687eeac035989
      release_candidates/java/v11.9/java_tools_windows-v11.9-rc1.zip 677ab910046205020fd715489147c2bcfad8a35d9f5d94fdc998d217545bd87a
      release_candidates/java/v11.9/java_tools_darwin_x86_64-v11.9-rc1.zip b9e962c6a836ba1d7573f2473fab3a897c6370d4c2724bde4017b40932ff4fe4
      release_candidates/java/v11.9/java_tools_darwin_arm64-v11.9-rc1.zip 3a897c6370d4c2724bde4017b40932ff4fe4b9e962c6a836ba1d7573f2473fab
      release_candidates/java/v11.9/java_tools-v11.9-rc1.zip 5cd59ea6bf938a1efc1e11ea562d37b39c82f76781211b7cd941a2346ea8484d
    ```

5. Create a new branch in the [rules_java](https://github.com/bazelbuild/rules_java) repository

  * Name the branch `java_v[version number]`, e.g. `java_v11.09`
  * Edit [java_tools_repos()](https://github.com/bazelbuild/rules_java/blob/master/java/repositories.bzl#L22-L73) by updating the `sha256` and `urls` fields for `remote_java_tools` with the correct version, rc, sha256sum, and url (see output from step 4)

     Example:
     ```starlark
     maybe(
         http_archive,
         name = "remote_java_tools",
         sha256 = "5cd59ea6bf938a1efc1e11ea562d37b39c82f76781211b7cd941a2346ea8484d",
         urls = [
            "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v11.9/java_tools-v11.9-rc1.zip",
         ],
     )     
     ```
     
  * Repeat for `remote_java_tools_linux`, `remote_java_tools_windows`, `remote_java_tools_darwin_x86_64` and `remote_java_tools_darwin_arm64`    

6. Edit [distdir_deps.bzl](https://github.com/bazelbuild/bazel/blob/master/distdir_deps.bzl#L65) in the Bazel repository by updating the `archive`, `sha256`, and `urls` fields with the updates made to the new branch (step 5). Create a new pull request - **example PR coming soon**. The PR triggers the CI presubmit.

7. Trigger a new build on Downstream https://buildkite.com/bazel/bazel-at-head-plus-downstream. Set the message field to "java_tools release [version] [rc]", leave the commit field as "HEAD", and use `pull/[PRNUMBER]/head` for the branch. See [example](https://buildkite.com/bazel/bazel-at-head-plus-downstream/builds/2818). 

    1. Check the results of the build to confirm that there are no new failures (i.e. all failures also appear at HEAD). To do this, compare the results to the latest run [here](https://buildkite.com/bazel/bazel-at-head-plus-downstream/builds?branch=master).
    2. If the CI finishes successfully:
        - Create the release artifacts from the release candidate:
          ```bash
          src/create_java_tools_release.sh \
          --java_tools_version $NEW_VERSION \
          --rc $RC --release true
          ```
          The script will output the sha256sum of the rc artifacts for linux, darwin and windows.

          Sample output:
          ```bash
          $ src/create_java_tools_release.sh --commit_hash 7bd0ab63a8441c3f3d7f495d09ed2bed38762874 --java_tools_version 11.9 --rc 1 --release true

            releases/java/v11.9/java_tools_linux-v11.9.zip 512582cac5b7ea7974a77b0da4581b21f546c9478f206eedf54687eeac035989
            releases/java/v11.9/java_tools_windows-v11.9.zip 677ab910046205020fd715489147c2bcfad8a35d9f5d94fdc998d217545bd87a
            releases/java/v11.9/java_tools_darwin_x86_64-v11.9.zip b9e962c6a836ba1d7573f2473fab3a897c6370d4c2724bde4017b40932ff4fe4
            releases/java/v11.9/java_tools_darwin_arm64-v11.9.zip 3a897c6370d4c2724bde4017b40932ff4fe4b9e962c6a836ba1d7573f2473fab
            releases/java/v11.9/java_tools-v11.9.zip 5cd59ea6bf938a1efc1e11ea562d37b39c82f76781211b7cd941a2346ea8484d
          ```        

        - Update the release in the java_tools [releases page](https://github.com/bazelbuild/java_tools/releases)
            -   Click on "Draft a new release"
                -   Set tag to java_v[version number], e.g. java_v11.09
                -   Set target to master
                -   Add the name, sha256, and urls to the description

                Example:
                ```
                To use this java_tools release, add to your WORKSPACE file the definitions:

                http_archive(
                    name = "remote_java_tools",
                    sha256 = "5cd59ea6bf938a1efc1e11ea562d37b39c82f76781211b7cd941a2346ea8484d",
                    urls = [
                            "https://mirror.bazel.build/bazel_java_tools/releases/java/v11.9/java_tools-v11.9.zip",
                            "https://github.com/bazelbuild/java_tools/releases/download/java_v11.9/java_tools-v11.9.zip",
                    ],
                )

                http_archive(
                    name = "remote_java_tools_linux",
                    sha256 = "512582cac5b7ea7974a77b0da4581b21f546c9478f206eedf54687eeac035989",
                    urls = [
                            "https://mirror.bazel.build/bazel_java_tools/releases/java/v11.9/java_tools_linux-v11.9.zip",
                            "https://github.com/bazelbuild/java_tools/releases/download/java_v11.9/java_tools_linux-v11.9.zip",
                    ],
                )

                http_archive(
                    name = "remote_java_tools_windows",
                    sha256 = "677ab910046205020fd715489147c2bcfad8a35d9f5d94fdc998d217545bd87a",
                    urls = [
                            "https://mirror.bazel.build/bazel_java_tools/releases/java/v11.9/java_tools_windows-v11.9.zip",
                            "https://github.com/bazelbuild/java_tools/releases/download/java_v11.9/java_tools_windows-v11.9.zip",    
                    ],
                )

                http_archive(
                    name = "remote_java_tools_darwin_x86_64",
                    sha256 = "b9e962c6a836ba1d7573f2473fab3a897c6370d4c2724bde4017b40932ff4fe4",
                    urls = [
                            "https://mirror.bazel.build/bazel_java_tools/releases/java/v11.9/java_tools_darwin_x86_64-v11.9.zip",
                            "https://github.com/bazelbuild/java_tools/releases/download/java_v11.9/java_tools_darwin_x86_64-v11.9.zip",
                    ],
                )

                http_archive(
                    name = "remote_java_tools_darwin_arm64",
                    sha256 = "3a897c6370d4c2724bde4017b40932ff4fe4b9e962c6a836ba1d7573f2473fab",
                    urls = [
                            "https://mirror.bazel.build/bazel_java_tools/releases/java/v11.9/java_tools_darwin_arm64-v11.9.zip",
                            "https://github.com/bazelbuild/java_tools/releases/download/java_v11.9/java_tools_darwin_arm64-v11.9.zip",
                    ],
                )
                ```
                
                -   Download the 5 .zip files from the updated https://mirror.bazel.build URLs above and attach them to the release
                -   Set as the latest release
                -   Refer to [this example](https://github.com/bazelbuild/java_tools/releases/tag/java_v11.9)
             
        - Return to the rules_java repository and create a PR to update [java_tools_repos()](https://github.com/bazelbuild/rules_java/blob/master/java/repositories.bzl#L22-L73) with the latest java_tools versions. After making sure presubmits pass, send the PR for review and assign `@hvadehra`.

        - Follow the steps [here](https://github.com/bazelbuild/rules_java/tree/master/distro) to release a new version of rules_java. Reach out to `@hvadhera` to decide/confirm the version number bump.
      
        - Update Bazel with the final rules_java version by editing the following files. After making sure presubmits pass, send the PR for review and assign `@hvadehra`.
            -   https://github.com/bazelbuild/bazel/blob/master/distdir_deps.bzl#L65
            -   https://github.com/bazelbuild/bazel/blob/master/src/MODULE.tools#L4
            -   https://github.com/bazelbuild/bazel/blob/master/MODULE.bazel#L19

    3. If the CI finishes unsuccessfully find the reasons why the CI is failing and file bugs. After the bugs are fixed start all over again from step 2 and create the next release candidate. This case is highly unlikely because Bazel already tests the `java_tools` built at head.
 
