import unittest as t
from palindrome import *

palindromes = [
    'x',
    'ada',
    'asdffdsa',
    'xxxxxxxxxx1xxxxxxxxxx',
    ' asdfdsa',
    'x  '
]

nonPalindromes = [
  'asdf',
  ' xy ',
  'fds '
]

class PalindromeTest(t.TestCase):
  def testPalindromes(self):
    for w in palindromes:
      self.assertTrue(isPalindrome(w), msg='{0} is palindrome'.format(w))

  def testNotPalindromes(self):
    for w in nonPalindromes:
      self.assertFalse(isPalindrome(w), msg='{0} is not palindrome'.format(w))

if __name__ == '__main__':
  t.main()
