# Copyright (C) 2016 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys

from mir.qualia import qualifier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('qualities', nargs='*')
    args = parser.parse_args()
    qual = qualifier.Qualifier(args.qualities)
    for line in qual(sys.stdin):
        sys.stdout.write(line)


if __name__ == '__main__':
    main()
