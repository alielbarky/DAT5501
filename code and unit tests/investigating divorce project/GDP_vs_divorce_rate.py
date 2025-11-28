import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

gdp_file = r"data\gdp-per-capita-maddison-project-database.csv"
divorce_file = r"data\US and UK divorces-per-1000-people.csv"

# Load the GDP data
gdp_df = pd.read_csv(gdp_file)
# Load the Divorce Rate data
divorce_df = pd.read_csv(divorce_file)

#Rename columns for easier access and clarity
gdp_df = gdp_df.rename(columns={'Entity': 'Country', 'GDP per capita': 'GDP'})
divorce_df = divorce_df.rename(columns={'Entity': 'Country', 'Crude divorce rate(per 1000 people)': 'DivorceRate'})

#Filter datasets to include only United Kingdom values
uk_gdp = gdp_df[gdp_df['Country'] == 'United Kingdom'].copy()
uk_divorce = divorce_df[divorce_df['Country'] == 'United Kingdom'].copy()
uk_gdp['GDP'] = pd.to_numeric(uk_gdp['GDP'], errors='coerce')
uk_divorce['DivorceRate'] = pd.to_numeric(uk_divorce['DivorceRate'], errors='coerce')

# Drop rows with missing values that resulted from 'coerce' or initial loading issues
uk_gdp.dropna(subset=['GDP'], inplace=True)
uk_divorce.dropna(subset=['DivorceRate'], inplace=True)

#inner merge by year
merged_df = pd.merge(uk_gdp[['Year', 'GDP']], uk_divorce[['Year', 'DivorceRate']], on='Year', how='inner')

# Define x and y
X = merged_df['GDP'].values
Y = merged_df['DivorceRate'].values

# Calculate the coefficients of the quadratic: y = ax^2 + bx + c
coeffs = np.polyfit(X, Y, 2)
# Create the polynomial function
poly_model = np.poly1d(coeffs)

#plot
x_fit = np.linspace(X.min(), X.max(), 100)
y_fit = poly_model(x_fit)
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    merged_df['GDP'],
    merged_df['DivorceRate'],
    c=merged_df['Year'], # Color the points by year
    cmap='viridis', # Use a color map to show progression over time
    label='UK Data Points (Colored by Year)',
    edgecolor='k',
    s=70 # Point size
)

# Plot the quadratic fitted curve
plt.plot(x_fit, y_fit, color='red', linestyle='--', label=f'Quadratic Fit')

# Add labels and title
plt.title('UK Divorce Rate vs. GDP per Capita with Quadratic Fit', fontsize=14)
plt.xlabel('GDP per Capita', fontsize=12)
plt.ylabel('Crude Divorce Rate (per 1000 people)', fontsize=12)

# Add a colour bar
cbar = plt.colorbar(scatter, label='Year')

#add the equation
equation = f'Fit: y = {coeffs[0]:.2e}x² + {coeffs[1]:.2f}x + {coeffs[2]:.2f}'
plt.figtext(0.15, 0.85, equation, bbox=dict(facecolor='white', alpha=0.8), fontsize=10)

plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.show()