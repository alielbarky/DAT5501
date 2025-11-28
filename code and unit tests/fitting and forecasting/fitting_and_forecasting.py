import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Load data
file_path = r"data\life-expectancy.csv"
data_frame = pd.read_csv(file_path)
df_world = data_frame[data_frame['Entity'] == 'World'].copy()
df_world.rename(columns={'Period life expectancy at birth': 'life_expectancy'}, inplace=True)
data = df_world[['Year', 'life_expectancy']].dropna()
start_year = data['Year'].min()
data['time'] = data['Year'] - start_year

#Sub-sample data
n_total = len(data)
n_test = 10
n_train = n_total - n_test

#training data
train_data = data.iloc[:n_train]
x_train = train_data['time'].values
y_train = train_data['life_expectancy'].values

#test data
test_data = data.iloc[n_train:]
x_test = test_data['time'].values
y_test = test_data['life_expectancy'].values

#full range for comparison
x_full = data['time'].values
years_full = data['Year'].values


#define polynomial function and function to calculate metrics
def polynomial_function(x, *params):
    # P(x) = p[0] + p[1]*x + ...
    return np.poly1d(params[::-1])(x)

def calculate_metrics(y_train, y_fit, k):
    # Calculates SSR, Chi^2/dof, and BIC
    n_train = len(y_train)
    ssr = np.sum((y_train - y_fit)**2)
    nu = n_train - k # Degrees of freedom
    chi2_per_dof = ssr / nu
    
    # BIC = N*ln(SSR/N) + K*ln(N)
    if ssr > 1e-10:
         bic = n_train * np.log(ssr / n_train) + k * np.log(n_train)
    else:
         bic = np.inf
         
    return ssr, chi2_per_dof, bic

#store results
results = []
max_order = 9

for m in range(1, max_order + 1):
    k = m + 1 # Number of parameters
    p0 = np.ones(k) * 0.1 

    try:
        #fit the training data
        popt, pcov = curve_fit(
            f=polynomial_function,
            xdata=x_train,
            ydata=y_train,
            p0=p0,
            maxfev=10000
        )

        #generate the model fit over the training data
        y_fit_train = polynomial_function(x_train, *popt)

        ssr, chi2_per_dof, bic = calculate_metrics(y_train, y_fit_train, k)
        
        y_forecast_full = polynomial_function(x_full, *popt)

        # Store results
        results.append({
            'order': m,
            'k_params': k,
            'params': popt,
            'covariance': pcov,
            'ssr': ssr,
            'chi2_per_dof': chi2_per_dof,
            'bic': bic,
            'y_forecast_full': y_forecast_full,
        })
        
    except RuntimeError:
        #failed fits
        results.append({
            'order': m, 'k_params': k, 'params': None, 'covariance': None, 
            'ssr': np.nan, 'chi2_per_dof': np.nan, 'bic': np.nan, 
            'y_forecast_full': np.full_like(x_full, np.nan)
        })

#convert the results list to a dataframe
results_df = pd.DataFrame(results).dropna(subset=['bic'])

plt.figure(figsize=(10, 6))
plt.scatter(years_full, data['life_expectancy'], label='all data', color='grey', alpha=0.6)
plt.scatter(test_data['Year'], y_test, label='reality (test data)', color='red', s=40, marker='X')

#plot selected models for clarity
for index, row in results_df.iterrows():
    m = row['order']
    if m in [1, 3, 5, 9]:
        plt.plot(years_full, row['y_forecast_full'], label=f'order {m} forecast', linestyle='--')

plt.axvline(x=test_data['Year'].min(), color='black', linestyle=':', label='forecast start')
plt.title('Polynomial Fitting and 10-Year Forecast (World Life Expectancy)')
plt.xlabel('Year')
plt.ylabel('Life Expectancy (Years)')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.5)
plt.savefig('part2_forecast_comparison.png')
plt.close()

fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Polynomial Order ($M$)')
ax1.set_ylabel('Chi^2 per Degree of Freedom', color=color)
ax1.plot(results_df['order'], results_df['chi2_per_dof'], 'o-', color=color, label='$\chi^2$/dof')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(results_df['order'].values)

#second axis for BIC
ax2 = ax1.twinx()  
color = 'tab:red'
ax2.set_ylabel('Bayesian Information Criterion (BIC)', color=color)  
ax2.plot(results_df['order'], results_df['bic'], 's--', color=color, label='BIC')
ax2.tick_params(axis='y', labelcolor=color)

#legends and set title
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')
fig.suptitle('Model Selection Metrics vs. Polynomial Order', fontsize=14)
fig.tight_layout()  
plt.grid(True, axis='x', alpha=0.5)
plt.savefig('part3_model_metrics.png')
plt.close()

#print results table
metrics_df = results_df[['order', 'k_params', 'ssr', 'chi2_per_dof', 'bic']].copy()
metrics_df.rename(columns={'k_params': 'parameters (k)'}, inplace=True)
print(metrics_df.to_markdown(index=False, floatfmt=".4f"))