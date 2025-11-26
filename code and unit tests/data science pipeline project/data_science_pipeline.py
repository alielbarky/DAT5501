import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

true_m = 2.5
true_b = 10.0
num_points = 100
noise_std_dev = 15
# define filename
data_filename = 'synthetic_data.csv' 

#define function to generate the data
def generate_data(m, b, n, noise_std):
    #Generate synthetic X and Y data points and noise    
    x = np.arange(n, dtype=float)
    y_perfect = m * x + b
    noise = np.random.normal(0, noise_std, n)
    y_noisy = y_perfect + noise
    
    data = pd.DataFrame({'X': x, 'Y': y_noisy})
    data.to_csv(data_filename, index=False)
    
    print(f"Data saved to {data_filename}")
    return x, y_noisy

#define a funciotn for fitting and plottingn
def fit_data(filename, true_m, true_b):
    #load the synthetic data previously generated
    data = pd.read_csv(filename)
    x_loaded = data['X'].values
    y_loaded = data['Y'].values
    
    # perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(x_loaded, y_loaded)
    
    print(f"True Parameters: m={true_m:.4f}, b={true_b:.4f}")
    print(f"Fitted Parameters: m={slope:.4f}, b={intercept:.4f}")
    
    #plotting
    y_fit = slope * x_loaded + intercept
    y_true = true_m * x_loaded + true_b 
    plt.figure(figsize=(10, 6))
    plt.scatter(x_loaded, y_loaded, label='Synthetic Noisy Data', s=10, color='gray')
    plt.plot(x_loaded, y_true, label=f'Original Line (m={true_m:.2f}, b={true_b:.2f})', 
             color='green', linestyle='--', linewidth=2)
    plt.plot(x_loaded, y_fit, label=f'Best Fit Line (m={slope:.2f}, b={intercept:.2f})', 
             color='red', linestyle='-', linewidth=2)
    
    #add title labels and legend
    plt.title('Synthetic Data, Original Line, and Best Fit Line')
    plt.xlabel('X (Independent Variable)')
    plt.ylabel('Y (Dependent Variable)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plot_filename = 'fit_plot.png'
    plt.savefig(plot_filename)
    print(f"\nPlot saved to {plot_filename}")
    plt.show()
    
    return slope, intercept #return the fitted values

#running the main code
x_gen, y_gen = generate_data(true_m, true_b, num_points, noise_std_dev)    
# Fit and plot (results are returned but ignored here, they are used by the test file)
fitted_m, fitted_b = fit_data(data_filename,true_m , true_b)