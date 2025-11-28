import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

file_path = r"data\life-expectancy.csv"
data_frame = pd.read_csv(file_path)

df_world = data_frame[data_frame['Entity'] == 'World'].copy()
df_world.rename(columns={'Period life expectancy at birth': 'life_expectancy'}, inplace=True)
data = df_world[['Year', 'life_expectancy']].dropna()

start_year = data['Year'].min()
data['time'] = data['Year'] - start_year

n_total = len(data)
n_test = 10
n_train = n_total - n_test

#training data
train_data = data.iloc[:n_train]
x_train = train_data['time'].values
y_train = train_data['life_expectancy'].values

#full range
x_full = data['time'].values
years_full = data['Year'].values

#function for polynomial fitting
def polynomial_function(x, *params):
    # P(x) = p[0] + p[1]*x + ...
    return np.poly1d(params[::-1])(x)

#analysing the best model

m_poly = 3
k_poly = m_poly + 1 # 4 parameters
p0_poly = np.ones(k_poly) * 0.1

#Fit Order 3 Polynomial
popt_poly, pcov_poly = curve_fit(
    f=polynomial_function,
    xdata=x_train,
    ydata=y_train,
    p0=p0_poly,
    maxfev=10000
)

#calculate Uncertainties
perr_poly = np.sqrt(np.diag(pcov_poly))


#print parameters

print(f"Best Model (Order 3 Polynomial) Parameters")

# Parameter values and uncertainties
params_df = pd.DataFrame({
    'parameter': [f'p{i}' for i in range(k_poly)],
    'value': popt_poly,
    'uncertainty (sigma)': perr_poly,
})
print("\nParameter Values and Uncertainties:")
print(params_df.to_markdown(index=False, floatfmt=".6f"))

# Covariance Matrix
print("\nCovariance Matrix:")
pcov_df = pd.DataFrame(pcov_poly, columns=[f'p{i}' for i in range(k_poly)], index=[f'p{i}' for i in range(k_poly)])
print(pcov_df.to_markdown(floatfmt=".4e"))