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

def generate_release_info(platform, artifacts):  
  return '''
  http_archive(
      name = "remote_{platform}",
      sha256 = "{sha}",
      urls = [
        "{mirror_url}",
        "{github_url}"
      ]
  )'''.format(
    platform = platform,
    sha = artifacts["sha"],
    mirror_url = artifacts["mirror_url"],
    github_url = artifacts["github_url"]
  )  

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

  artifacts = json.loads(opts.artifacts)["artifacts"]

  relnotes = "To use this java_tools release, add to your WORKSPACE file the definitions: \n```py"
  for platform in artifacts:
    relnotes += generate_release_info(platform, artifacts[platform])
    download_file(artifacts[platform]["mirror_url"])

  relnotes += "\n```"
  with open('relnotes.txt', 'w') as f:
    f.write(relnotes)


if __name__ == '__main__':
  main()
