import unittest
from calculator import total

class CalculatorTests(unittest.TestCase):
    def test_quantity(self): self.assertEqual(total(10, 2), 20)
    def test_another_order(self): self.assertEqual(total(5, 4), 20)
    def test_free_item(self): self.assertEqual(total(0, 4), 0)
    def test_decimal_price(self): self.assertEqual(total(12.5, 2), 25)

if __name__ == '__main__': unittest.main()
