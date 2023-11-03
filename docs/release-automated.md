**This playbook describes the updated java_tools release process. If you see any failures or issues with automation, please follow the manual release process documented [here](https://github.com/bazelbuild/java_tools/blob/master/docs/release.md).**

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

1. Create a new tracking issue for the release in this repository using the "release tracker" [template](https://github.com/bazelbuild/java_tools/issues/new/choose).
2. Trigger a new build of the [`java_tools binaries pipeline`](https://buildkite.com/bazel-trusted/java-tools-binaries-java). Set the message field to "java_tools release [version] [rc]", and leave the commit field as "HEAD" and branch as "master". See [example](https://buildkite.com/bazel-trusted/java-tools-binaries-java/builds/233).
3. Identify and set the following environment variables:

  * `COMMIT_HASH` the commit hash where the pipeline was run (see below)
  * `NEW_VERSION` the new version number you’re trying to release (e.g. `13.1`)
  * `RC` the number of the current release candidate

     For example:
     ```bash
     export COMMIT_HASH=c7d8d1e3f16ac6db37b134358b6cfdb5e3c8f6b0
     export NEW_VERSION=13.1
     export RC=1
     ```

4. Create a new release candidate by running the command below from the [Bazel](https://github.com/bazelbuild/bazel) repo:

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
    $ src/create_java_tools_release.sh --commit_hash c7d8d1e3f16ac6db37b134358b6cfdb5e3c8f6b0 --java_tools_version 13.1 --rc 1 --release false

      {
        "version": "v13.1",
        "release": "false",
        "artifacts": {
          "java_tools_linux": {
            "mirror_url": "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v13.1/java_tools_linux-v13.1-rc1.zip",
            "sha": "d134da9b04c9023fb6e56a5d4bffccee73f7bc9572ddc4e747778dacccd7a5a7"
          },
          "java_tools_windows": {
            "mirror_url": "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v13.1/java_tools_windows-v13.1-rc1.zip",
            "sha": "c5c70c214a350f12cbf52da8270fa43ba629b795f3dd328028a38f8f0d39c2a1"
          },
          "java_tools_darwin_x86_64": {
            "mirror_url": "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v13.1/java_tools_darwin_x86_64-v13.1-rc1.zip",
            "sha": "0db40d8505a2b65ef0ed46e4256757807db8162f7acff16225be57c1d5726dbc"
          },
          "java_tools_darwin_arm64": {
            "mirror_url": "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v13.1/java_tools_darwin_arm64-v13.1-rc1.zip",
            "sha": "dab5bb87ec43e980faea6e1cec14bafb217b8e2f5346f53aa784fd715929a930"
          },
          "java_tools": {
            "mirror_url": "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v13.1/java_tools-v13.1-rc1.zip",
            "sha": "286bdbbd66e616fc4ed3f90101418729a73baa7e8c23a98ffbef558f74c0ad14"
          }
        }
      }
    ```

5. Create a new branch in the [rules_java](https://github.com/bazelbuild/rules_java) repository

  * Name the branch `java_v[version number]`, e.g. `java_v11.09`
  * Edit [java/repositories.bzl](https://github.com/bazelbuild/rules_java/blob/master/java/repositories.bzl) by copying the output from step 4 to `_JAVA_TOOLS_CONFIG`

     Example:
     ```starlark
      _JAVA_TOOLS_CONFIG = {
        "version": "v13.1",
        "release": "false",
        "artifacts": {
          "java_tools_linux": {
            "mirror_url": "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v13.1/java_tools_linux-v13.1-rc1.zip",
            "sha": "d134da9b04c9023fb6e56a5d4bffccee73f7bc9572ddc4e747778dacccd7a5a7"
          },
          "java_tools_windows": {
            "mirror_url": "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v13.1/java_tools_windows-v13.1-rc1.zip",
            "sha": "c5c70c214a350f12cbf52da8270fa43ba629b795f3dd328028a38f8f0d39c2a1"
          },
          "java_tools_darwin_x86_64": {
            "mirror_url": "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v13.1/java_tools_darwin_x86_64-v13.1-rc1.zip",
            "sha": "0db40d8505a2b65ef0ed46e4256757807db8162f7acff16225be57c1d5726dbc"
          },
          "java_tools_darwin_arm64": {
            "mirror_url": "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v13.1/java_tools_darwin_arm64-v13.1-rc1.zip",
            "sha": "dab5bb87ec43e980faea6e1cec14bafb217b8e2f5346f53aa784fd715929a930"
          },
          "java_tools": {
            "mirror_url": "https://mirror.bazel.build/bazel_java_tools/release_candidates/java/v13.1/java_tools-v13.1-rc1.zip",
            "sha": "286bdbbd66e616fc4ed3f90101418729a73baa7e8c23a98ffbef558f74c0ad14"
          }
        }
      } 
     ```
     
  * Refer to [this example](https://github.com/bazelbuild/rules_java/commit/8b3d6fd2728610c71be2f6937783a396de139576)

6. Edit [distdir_deps.bzl](https://github.com/bazelbuild/bazel/blob/master/distdir_deps.bzl) in the Bazel repository and create a new pull request. This PR will trigger the CI presubmit.

  * Get the commit hash for the changes made in step 5 (e.g. `8b3d6fd2728610c71be2f6937783a396de139576` for [this commit](https://github.com/bazelbuild/rules_java/commit/8b3d6fd2728610c71be2f6937783a396de139576))
     * Download the tar.gz file at `https://github.com/bazelbuild/rules_java/archive/<commit hash>.tar.gz`
     * Run `shasum -a 256 <file>`
     * Update the following fields (note: add `strip_prefix`)
       
        Example:
        ```starlark
        "archive": "8b3d6fd2728610c71be2f6937783a396de139576.tar.gz",
        "sha256": "e8a6427d7882215b009c048f996499e89c9e43c13c56234da16a49b154c46546",
        "strip_prefix": "rules_java-8b3d6fd2728610c71be2f6937783a396de139576",
        "urls": ["https://github.com/bazelbuild/rules_java/archive/8b3d6fd2728610c71be2f6937783a396de139576.tar.gz"],`
        ```
        
     * Refer to [this PR](https://github.com/bazelbuild/bazel/pull/20045) (specifically [this commit](https://github.com/bazelbuild/bazel/pull/20045/commits/b0ec360581ee665faf2298641ef4bb6feee12f9d))
  * Add archive_override to MODULE.bazel
     * To calculate the `integrity` value of the source archive, trigger the [BCR integrity pipeline](https://buildkite.com/bazel-trusted/bcr-integrity). Set the message field to "java_tools release [version] [rc]", and leave the commit field as "HEAD" and branch as "main". Click on "get archive" and enter the `<commit>.tar.gz` (e.g. `8b3d6fd2728610c71be2f6937783a396de139576.tar.gz`). The integrity value will be printed at the end of the "calculate integrity value" step. See [example](https://buildkite.com/bazel-trusted/bcr-integrity/builds/13).

     * Add archive_override with the `integrity` and commit hash from above
       
        Example:
        ```starlark
        archive_override(
            module_name = "rules_java",
            urls = ["https://github.com/bazelbuild/rules_java/archive/8b3d6fd2728610c71be2f6937783a396de139576.tar.gz"],
            integrity = "sha256-6KZCfXiCIVsAnASPmWSZ6JyeQ8E8ViNNoWpJsVTEZUY=",
            strip_prefix = "rules_java-8b3d6fd2728610c71be2f6937783a396de139576",
        )
        ```
        
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
          $ src/create_java_tools_release.sh --commit_hash c7d8d1e3f16ac6db37b134358b6cfdb5e3c8f6b0 --java_tools_version 13.1 --rc 1 --release true
      
            {
              "version": "v13.1",
              "release": "true",
              "artifacts": {
                "java_tools_linux": {
                  "mirror_url": "https://mirror.bazel.build/bazel_java_tools/releases/java/v13.1/java_tools_linux-v13.1.zip",
                  "github_url": "https://github.com/bazelbuild/java_tools/releases/download/java_v13.1/java_tools_linux-v13.1.zip",
                  "sha": "d134da9b04c9023fb6e56a5d4bffccee73f7bc9572ddc4e747778dacccd7a5a7"
                },
                "java_tools_windows": {
                  "mirror_url": "https://mirror.bazel.build/bazel_java_tools/releases/java/v13.1/java_tools_windows-v13.1.zip",
                  "github_url": "https://github.com/bazelbuild/java_tools/releases/download/java_v13.1/java_tools_windows-v13.1.zip",
                  "sha": "c5c70c214a350f12cbf52da8270fa43ba629b795f3dd328028a38f8f0d39c2a1"
                },
                "java_tools_darwin_x86_64": {
                  "mirror_url": "https://mirror.bazel.build/bazel_java_tools/releases/java/v13.1/java_tools_darwin_x86_64-v13.1.zip",
                  "github_url": "https://github.com/bazelbuild/java_tools/releases/download/java_v13.1/java_tools_darwin_x86_64-v13.1.zip",
                  "sha": "0db40d8505a2b65ef0ed46e4256757807db8162f7acff16225be57c1d5726dbc"
                },
                "java_tools_darwin_arm64": {
                  "mirror_url": "https://mirror.bazel.build/bazel_java_tools/releases/java/v13.1/java_tools_darwin_arm64-v13.1.zip",
                  "github_url": "https://github.com/bazelbuild/java_tools/releases/download/java_v13.1/java_tools_darwin_arm64-v13.1.zip",
                  "sha": "dab5bb87ec43e980faea6e1cec14bafb217b8e2f5346f53aa784fd715929a930"
                },
                "java_tools": {
                  "mirror_url": "https://mirror.bazel.build/bazel_java_tools/releases/java/v13.1/java_tools-v13.1.zip",
                  "github_url": "https://github.com/bazelbuild/java_tools/releases/download/java_v13.1/java_tools-v13.1.zip",
                  "sha": "286bdbbd66e616fc4ed3f90101418729a73baa7e8c23a98ffbef558f74c0ad14"
                }
              }
            }
          ```        

        - Create a [java_tools release](https://github.com/bazelbuild/java_tools/releases) by triggering the [java-tools-release pipeline](https://buildkite.com/bazel-trusted/java-tools-release). Set the message field to "java_tools release [version] [rc]", and leave the commit field as "HEAD" and branch as "master". Click on "artifacts information" and paste the output from the step above. See [example](https://buildkite.com/bazel-trusted/java-tools-release/builds/2).
                         
        - Return to the rules_java repository and create a PR to update [java/repositories.bzl](https://github.com/bazelbuild/rules_java/blob/master/java/repositories.bzl) with the latest java_tools versions. After making sure presubmits pass, send the PR for review and assign `@hvadehra`. Refer to [this example](https://github.com/bazelbuild/rules_java/pull/119) (it also includes the 2 updates needed for the next step).

        - Follow the steps [here](https://github.com/bazelbuild/rules_java/tree/master/distro) to release a new version of rules_java.
      
        - Update Bazel with the final rules_java version by editing the following files. After making sure presubmits pass, send the PR for review and assign `@hvadehra`. Refer to [this PR](https://github.com/bazelbuild/bazel/pull/18902).
            -   https://github.com/bazelbuild/bazel/blob/master/distdir_deps.bzl#L65 ([example](https://github.com/bazelbuild/bazel/pull/18902/commits/30aa092cfe50435ae370c4a4bc9938eff52ce3fb))
            -   https://github.com/bazelbuild/bazel/blob/master/src/MODULE.tools#L4 ([example](https://github.com/bazelbuild/bazel/pull/18902/commits/73c8858d5195f072bbb316a3bf1289de1646d91a))
            -   https://github.com/bazelbuild/bazel/blob/master/MODULE.bazel#L19 ([example](https://github.com/bazelbuild/bazel/pull/18902/commits/5b30bc4f23037f5651063e24c1881328720d6bcb)). Remove the archive_override() method as well.

    3. If the CI finishes unsuccessfully find the reasons why the CI is failing and file bugs. After the bugs are fixed start all over again from step 2 and create the next release candidate. This case is highly unlikely because Bazel already tests the `java_tools` built at head.
 
