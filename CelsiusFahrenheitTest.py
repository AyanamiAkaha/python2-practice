import unittest as t
from CelsiusFahrenheit import *

testData = [
  { 'Celsius': 0, 'Fahrenheit': 32 },
  { 'Celsius': 10, 'Fahrenheit': 50 },
  { 'Celsius': -10, 'Fahrenheit': 14 },
  { 'Celsius': 100, 'Fahrenheit': 212 },
  { 'Celsius': -100, 'Fahrenheit': -148 },
  { 'Celsius': 50, 'Fahrenheit': 122 },
  { 'Celsius': -50, 'Fahrenheit': -58 },
  { 'Celsius': 4, 'Fahrenheit': 39.2 },
]

class CelsiusFahrenheitTest(t.TestCase):
  def testConvertsCelsiusToFahrenheit(self):
    for sample in testData:
      result = celsius2fahrenheit(sample['Celsius'])
      self.assertAlmostEqual(1.0*sample['Fahrenheit'], result,
                       msg='Want {0}, got {1}'.format(sample['Fahrenheit'], result))

  def testConvertsFahrenheitToCelsius(self):
    for sample in testData:
      result = fahrenheit2celsius(sample['Fahrenheit'])
      self.assertAlmostEqual(1.0*sample['Celsius'], result,
                       msg='Want {0}, got {1}'.format(1.0*sample['Celsius'], result))

if(__name__ == '__main__'):
  t.main()
