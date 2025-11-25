import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#load the data from the file
path = r"C:\Users\aelbarky001\Desktop\divorces-per-1000-people.csv"

df = pd.read_csv(path)
uk = df[df['Entity'] == 'United Kingdom'].copy()


uk['Year'] = pd.to_numeric(uk['Year'], errors='coerce')
uk['divorce rate'] = pd.to_numeric(uk['divorce rate'], errors='coerce')
uk = uk.dropna(subset=['Year', 'divorce rate']).sort_values('Year')

x = uk['Year'].values.astype(float)
y = uk['divorce rate'].values.astype(float)

#tried modelling it as linear did not look too good, quadratic fit works better
def quadratic_model(x, a, b, c):
    return a * x**2 + b * x + c

#fit the model and plot the curve
popt, pcov = curve_fit(quadratic_model, x, y)
a, b, c = popt
x_curve = np.linspace(x.min(), x.max(), 400)
y_curve = quadratic_model(x_curve, a, b, c)
plt.figure(figsize=(10, 7))
plt.scatter(x, y, color='teal', alpha=0.8, s=45, label='Data')
plt.plot(x_curve, y_curve, color='blue', linewidth=2, label='Quadratic Fit')
eq = f"y = {a:.5e}x² {'+' if b>=0 else '-'} {abs(b):.3f}x {'+' if c>=0 else '-'} {abs(c):.2f}"
x_text = x.min() + 0.02 * (x.max() - x.min())
y_text = y.max() - 0.05 * (y.max() - y.min())

#add colour, legend, title and label axes
plt.text(x_text, y_text, eq, fontsize=12, color='blue', ha='left', va='top')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Divorce Rate (per 1000 people)', fontsize=12)
plt.title('Divorce Rate Over Time - United Kingdom (Quadratic Fit)', fontsize=16)
plt.grid(True, alpha=0.3)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()