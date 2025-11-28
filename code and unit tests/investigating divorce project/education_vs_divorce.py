import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

divorce_file = r"data\US and UK divorces-per-1000-people.csv"
schooling_file = r"data\years-of-schooling.csv"
df_divorce = pd.read_csv(divorce_file)
df_schooling = pd.read_csv(schooling_file)

#Filter for United Kingdom data only
uk_divorce = df_divorce[df_divorce['Entity'] == 'United Kingdom'].copy()
uk_schooling = df_schooling[df_schooling['Entity'] == 'United Kingdom'].copy()

#Merge the datasets by year
#Inner join to get only years where both data points exist
merged_data = pd.merge(uk_divorce, uk_schooling, on='Year')

#Prepare data for plotting
x = merged_data['Average years of schooling']
y = merged_data['Crude divorce rate(per 1000 people)']

#calculate quadratic fit
coefficients = np.polyfit(x, y, 2)
poly_eqn = np.poly1d(coefficients)
x_line = np.linspace(x.min(), x.max(), 100)
y_line = poly_eqn(x_line)

# Calculate R-squared for the fit
y_pred = poly_eqn(x)
ss_res = np.sum((y - y_pred) ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

#plot
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='black', alpha=0.7, label='Actual Data')
plt.plot(x_line, y_line, color='red', linewidth=2, label=f'Quadratic Fit ($R^2={r_squared:.2f}$)')

#formatting
plt.title('United Kingdom: Divorce Rate vs. Years of Schooling')
plt.xlabel('Average Years of Schooling')
plt.ylabel('Crude Divorce Rate (per 1000 people)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

print(f"Graph generated successfully")
plt.show()