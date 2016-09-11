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
