from __future__ import print_function

import sys

from collections import Counter

def usage():
  print('Usage: {0} <filename>'.format(sys.argv[0]), file=sys.stderr);

def main():
  if len(sys.argv) != 2:
    usage()
    return -1
  file=open(sys.argv[1])
  print(Counter(file.read().split()))

if __name__ == '__main__':
  main()
