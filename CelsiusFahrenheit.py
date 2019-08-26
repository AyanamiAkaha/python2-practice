import sys

def celsius2fahrenheit(celsius):
  return celsius*9.0/5 + 32;

def fahrenheit2celsius(fahrenheit):
  return (fahrenheit-32)*5.0/9

def main():
  if len(sys.argv) != 3:
    print >> sys.stderr, 'Usage: {0} <temperature> <F|C>'.format(sys.argv[0])
    return
  try:
    temperature = float(sys.argv[1])
  except ValueError:
    print >> sys.stderr, '{0} is not a number'.format(sys.argv[1])
    return
  if(sys.argv[2].lower() == 'f'):
    print fahrenheit2celsius(temperature)
  elif(sys.argv[2].lower() == 'c'):
    print celsius2fahrenheit(temperature)
  else:
    print >> sys.stderr, 'Unknown scale {0}'.format(sys.argv[2])

if(__name__ == '__main__'):
  main()
