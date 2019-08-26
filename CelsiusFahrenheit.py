from __future__ import print_function

import sys

def celsius2fahrenheit(celsius):
  return celsius*9.0/5 + 32;

def fahrenheit2celsius(fahrenheit):
  return (fahrenheit-32)*5.0/9

def main():
  if len(sys.argv) != 3:
    print('Usage: {0} <temperature> <F|C>'.format(sys.argv[0]), file=sys.stderr)
    return
  try:
    temperature = float(sys.argv[1])
  except ValueError:
    print('{0} is not a number'.format(sys.argv[1]), file=sys.stderr)
    return
  if(sys.argv[2].lower() == 'f'):
    print(fahrenheit2celsius(temperature))
  elif(sys.argv[2].lower() == 'c'):
    print(celsius2fahrenheit(temperature))
  else:
    print('Unknown scale {0}'.format(sys.argv[2]), file=sys.stderr)

if(__name__ == '__main__'):
  main()
