#This is similar to the initial data sciencepipeline with additions like dealing with outliers, non-linear fit and so on
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TRUE_A = 0.05 
TRUE_B = -1.0 
TRUE_C = 20.0 
NUM_POINTS = 100
NOISE_MEAN_STD_DEV = 3.0
OUTLIER_X = 75
OUTLIER_Y_OFFSET = 50 
DATA_FILENAME = 'extended_synthetic_data.csv'

#threshold which will be used in the unit test 
MIN_R_SQUARED_THRESHOLD = 0.85 

#data generation function remains very similar
def generate_complex_data(a, b, c, n, noise_std, outlier_x, outlier_offset):
    X = np.arange(n, dtype=float)
    Y_perfect = a * X**2 + b * X + c
    Y_err = NOISE_MEAN_STD_DEV + (X / n) * NOISE_MEAN_STD_DEV * 2
    Y_noisy = Y_perfect + np.random.normal(0, Y_err)
    
    #introducnig the outlier
    outlier_idx = np.where(X == outlier_x)[0]
    if outlier_idx.size > 0:
        Y_noisy[outlier_idx] += outlier_offset
        print(f"Introduced outlier at X={outlier_x}, offset by {outlier_offset}")

    data = pd.DataFrame({'X': X, 'Y': Y_noisy, 'Y_Err': Y_err})
    data.to_csv(DATA_FILENAME, index=False)
    
    print(f"Data saved to {DATA_FILENAME}")
    return X, Y_noisy, Y_err

#function for fitting, R^2 calculation, plotting etc.
def fit_and_plot_data(filename, true_a, true_b, true_c):
    data = pd.read_csv(filename)
    X_loaded = data['X'].values
    Y_loaded = data['Y'].values
    Y_err_loaded = data['Y_Err'].values

    #Fit Quadratic Model (degree=2)
    coefficients = np.polyfit(X_loaded, Y_loaded, deg=2)
    fitted_a, fitted_b, fitted_c = coefficients
    p = np.poly1d(coefficients)
    Y_fit = p(X_loaded)
    print(f"Fitted Params: a={fitted_a:.4f}, b={fitted_b:.4f}, c={fitted_c:.4f}")

    #R-squared Calculation
    y_mean = np.mean(Y_loaded)
    ss_tot = np.sum((Y_loaded - y_mean)**2) # Total sum of squares
    ss_res = np.sum((Y_loaded - Y_fit)**2) # Residual sum of squares
    r_squared = 1 - (ss_res / ss_tot)
    
    print(f"Calculated R-Squared (R²): {r_squared:.4f}")
    #plotting
    Y_true = true_a * X_loaded**2 + true_b * X_loaded + true_c
    
    plt.figure(figsize=(12, 7))
    plt.errorbar(X_loaded, Y_loaded, yerr=Y_err_loaded, fmt='o', 
                 label='Noisy Data with Variable Error Bars', 
                 capsize=3, markersize=4, color='darkgray', alpha=0.6)
    
    outlier_idx = np.where(X_loaded == OUTLIER_X)[0]
    if outlier_idx.size > 0:
        plt.scatter(X_loaded[outlier_idx], Y_loaded[outlier_idx], 
                    color='purple', s=100, marker='x', label='Outlier')
        
    plt.plot(X_loaded, Y_true, label=f'Original Quadratic Curve', 
             color='green', linestyle='--', linewidth=3, alpha=0.7)
             
    plt.plot(X_loaded, Y_fit, label=f'Best Fit Quadratic (R²={r_squared:.2f})', 
             color='red', linestyle='-', linewidth=2)
    
    plt.title('Quadratic Fit with Variable Error Bars and Outlier')
    plt.xlabel('X (Independent Variable)')
    plt.ylabel('Y (Dependent Variable)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plot_filename = 'extended_fit_plot.png'
    plt.savefig(plot_filename)
    print(f"\nPlot saved to {plot_filename}")
    plt.show()
    
    return r_squared

#running the main code    

#Generate the data
X_gen, Y_gen, Y_err_gen = generate_complex_data(
    TRUE_A, TRUE_B, TRUE_C, NUM_POINTS, NOISE_MEAN_STD_DEV, 
    OUTLIER_X, OUTLIER_Y_OFFSET
    )
    
#fit and plot the data
r_squared_result = fit_and_plot_data(DATA_FILENAME, TRUE_A, TRUE_B, TRUE_C)
