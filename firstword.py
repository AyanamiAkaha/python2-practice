from __future__ import print_function

import sys
import re

if(sys.version_info.major == 2):
  input = raw_input

def main():
  print('Enter any sentence: ')
  s = input()
  firstWord = re.sub('\\s+.*', '', s.lstrip());
  print('First character is \'{0}\', last is \'{1}\''.format(s[0], s[-1]))
  print('First word is "{0}"'.format(firstWord))

if __name__ == '__main__':
  main()
