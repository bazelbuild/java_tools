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
import json

def generate_release_info(platform, version, path, sha):
  mirror_url = "https://mirror.bazel.build/bazel_java_tools/" + path
  github_url = "https://github.com/bazelbuild/java_tools/releases/download/java_" + version + "/" + platform + "-" + version + ".zip"
  relnote = ("\n" + 
            "http_archive(\n"
            "    name = \"remote_" + platform + "\",\n" +
            "    sha = \"" + sha + "\",\n" +
            "    urls = [\n" +
            "            \"" + mirror_url + "\",\n" +
            "            \"" + github_url + "\",\n" +
            "    ],\n" +
            ")")    
  return relnote, mirror_url

def download_file(mirror_url):
  wget.download(mirror_url , '.')

def get_version(artifacts):
  path = artifacts["java_tools"]["path"]
  version = path[path.find("/v"):path.find("/java_")][1:]
  return version

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--artifacts',
      required=True,
      dest='artifacts',
      help='Output from create_java_tools_release.sh')
  opts = parser.parse_args()

  artifacts = json.loads(opts.artifacts)
  version = get_version(artifacts)

  relnotes = "To use this java_tools release, add to your WORKSPACE file the definitions: \n```py"
  for platform in artifacts:
    path = artifacts[platform]["path"]
    sha = artifacts[platform]["sha"]
    relnote, mirror_url = generate_release_info(platform, version, path, sha)
    relnotes += relnote
    download_file(mirror_url)

  relnotes += "```"
  with open('relnotes.txt', 'w') as f:
    f.write(relnotes)


if __name__ == '__main__':
  main()
