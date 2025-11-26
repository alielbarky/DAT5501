import unittest
#import all necessary variables and the fitting function
from data_science_pipeline import true_m, true_b, data_filename, fit_data 

#define maximum acceptable difference between the true and fitted parameters.
tolerance = 3
class TestLinearFit(unittest.TestCase):
    def test_fitted_parameters_match_true(self):
        #test  that the fitted slope (m) and intercept (b) are within the defined tolerance of the true parameters.
        # 1. Execute the fitting function to retrieve the fitted parameters.
        # run the pipeline file first to create the CSV.
        try:
            # The fit_data function is called with: filename, true_m, true_b
            fitted_m, fitted_b = fit_data(data_filename, true_m, true_b)
        except FileNotFoundError:
            self.fail(f"Could not load data. Ensure '{data_filename}' exists and the main pipeline script was run.")
        except Exception as e:
            self.fail(f"An error occurred during fitting: {e}")

        # use assertAlmostEqual for robust floating-point comparison to check if the two values are within 'delta' (tolerance) of each other.
        
        # Test Slope (m)
        self.assertAlmostEqual(fitted_m, true_m, 
                               delta=tolerance,
                               msg=(f"Slope (m) failed test. "
                                    f"True: {true_m:.4f}, Fitted: {fitted_m:.4f}. "
                                    f"Difference is greater than tolerance ({tolerance}).")) # Renamed reference

        # Test Intercept (b)
        self.assertAlmostEqual(fitted_b, true_b, 
                               delta=tolerance, # Renamed reference
                               msg=(f"Intercept (b) failed test. "
                                    f"True: {true_b:.4f}, Fitted: {fitted_b:.4f}. "
                                    f"Difference is greater than tolerance ({tolerance}).")) # Renamed reference
        
        print(f"TEST PASSED! (Both m and b are within the tolerance of {tolerance})") # Renamed reference

if __name__ == '__main__':
    #the original script's fit_data function will run twice
    unittest.main()