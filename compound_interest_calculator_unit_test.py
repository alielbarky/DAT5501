import unittest
from compound_interest_calculator import interest_calculator

class TestInterestCalculator(unittest.TestCase):
    def test_interest_calculator(self):
        years_to_double, balances = interest_calculator(1000, 10, 3)
        
        # Rule of 72: 72 / 10 = 7.2 → ceil to 8
        self.assertEqual(years_to_double, 8)
        
        # Yearly balances: 1000*(1+0.1) = 1100, 1210, 1331
        expected_balances = [1100.0, 1210.0, 1331.0]
        self.assertEqual(balances, expected_balances)

if __name__ == "__main__":
    unittest.main()