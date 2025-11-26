#main pipeline should be run run first
import unittest
#import constants and the key function
from data_science_pipeline_extended import (TRUE_A, TRUE_B, TRUE_C, DATA_FILENAME, MIN_R_SQUARED_THRESHOLD, fit_and_plot_data)

class TestQuadraticFit(unittest.TestCase):
    #validating the R-squared value 

    def test_goodness_of_fit(self):
        #R-squared must be above minimum required threshold
        print("\nRunning Unit Test for Goodness of Fit (R²)")
        
        #call the function that calculates R^2
        try:
            r_squared = fit_and_plot_data(DATA_FILENAME, TRUE_A, TRUE_B, TRUE_C)
        except FileNotFoundError:
            self.fail(f"Could not load data. Ensure '{DATA_FILENAME}' exists and the pipeline was run.")

        print(f"Calculated R²: {r_squared:.4f}")
        print(f"Required R² Threshold: {MIN_R_SQUARED_THRESHOLD:.2f}")

        #unittest assertion for threshold checking
        # Check calculated R^2 is greater than or equal to the threshold
        self.assertGreaterEqual(
            r_squared, 
            MIN_R_SQUARED_THRESHOLD, 
            msg=f"R² score ({r_squared:.4f}) is below the required threshold of {MIN_R_SQUARED_THRESHOLD:.2f}"
        )
        
        print("\nTEST PASSED! The quadratic model fit is of sufficient quality.")

if __name__ == '__main__':
    unittest.main()
