from __future__ import print_function

import sys

if sys.version_info.major == 2:
  input = raw_input

def isPalindrome(word):
  w = word.strip().lower();
  for i in range(0, len(w)//2+1):
    if w[i] != w[-(i+1)]:
      return False
  return True

def main():
  print('Write word to test if it is a palindrome:')
  s = input()
  if isPalindrome(s):
    print('It is a palindrome')
  else:
    print('It is not a palindrome')

if __name__ == '__main__':
  main()
