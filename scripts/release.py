# Copyright 2022 The Bazel Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script to get release notes + zip files to release java_tools."""

import argparse
import wget

def get_artifact_breakdown(input):
  artifacts = {}
  input = input.split("\n")
  for artifact in input:
    dict = {}
    info = artifact.split()
    dict["path"] = path = info[0]
    dict["sha"] = info[1]
    name = path[path.find("/java_"):path.find("-v")][1:]
    artifacts[name] = dict
  return artifacts

def get_version(artifacts):
  path = artifacts["java_tools"]["path"]
  version = path[path.find("/v"):path.find("/java_")][1:]
  return version

def generate_release_info(item, version, path, sha):
  mirror_url = "https://mirror.bazel.build/bazel_java_tools/" + path
  relnote = ("\n" + 
            "http_archive(\n"
            "    name = \"remote_" + item + "\",\n" +
            "    sha = \"" + sha + "\",\n" +
            "    urls = [\n" +
            "            \"" + mirror_url + "\",\n" + 
            "            \"https://github.com/bazelbuild/java_tools/releases/download/java_" + version + "/" + item + "-" + version + ".zip\",\n"
            "    ],\n" +
            ")")    
  return relnote, mirror_url

def download_file(mirror_url):
  wget.download(mirror_url , '.')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--artifacts',
      required=True,
      dest='artifacts',
      help='Output from create_java_tools_release.sh')
  opts = parser.parse_args()

  artifacts = get_artifact_breakdown(opts.artifacts)
  version = get_version(artifacts)

  relnotes = "To use this java_tools release, add to your WORKSPACE file the definitions: \n```py"
  for item in artifacts:
    relnote, mirror_url = generate_release_info(item, version, artifacts[item]["path"], artifacts[item]["sha"])
    relnotes += relnote
    download_file(mirror_url)

  relnotes += "```"
  with open('relnotes.txt', 'w') as f:
    f.write(relnotes)


if __name__ == '__main__':
  main()
