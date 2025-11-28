#i had no previous experience with statsmodel so i used some AI assistance here
import pandas as pd
import statsmodels.api as sm

df_divorce = pd.read_csv(r"data\US and UK divorces-per-1000-people.csv")
df_gdp = pd.read_csv(r"data\gdp-per-capita-maddison-project-database.csv")
df_schooling = pd.read_csv(r"data\years-of-schooling.csv")
df_working_hours = pd.read_csv(r"data\annual-working-hours-per-worker.csv")


# Target Variable (Divorce Rate)
df_divorce_uk = df_divorce[df_divorce['Entity'] == 'United Kingdom'].copy()
df_divorce_uk = df_divorce_uk[['Year', 'Crude divorce rate(per 1000 people)']]
df_divorce_uk.rename(columns={'Crude divorce rate(per 1000 people)': 'Divorce_Rate'}, inplace=True)

# metric 1: GDP per capita
df_gdp_uk = df_gdp[df_gdp['Entity'] == 'United Kingdom'].copy()
df_gdp_uk = df_gdp_uk[['Year', 'GDP per capita']]
df_gdp_uk.rename(columns={'GDP per capita': 'GDP_Per_Capita'}, inplace=True)

# metric 2: Years of Schooling
df_schooling_uk = df_schooling[df_schooling['Entity'] == 'United Kingdom'].copy()
df_schooling_uk = df_schooling_uk[['Year', 'Average years of schooling']]
df_schooling_uk.rename(columns={'Average years of schooling': 'Years_of_Schooling'}, inplace=True)

# metric 3: Annual Working Hours
df_working_hours_uk = df_working_hours[df_working_hours['Entity'] == 'United Kingdom'].copy()
df_working_hours_uk = df_working_hours_uk[['Year', 'Annual Working hours per worker']]
df_working_hours_uk.rename(columns={'Annual Working hours per worker': 'Annual_Working_Hours'}, inplace=True)

# Merge all UK dataframes based on 'Year'
df_merged = df_divorce_uk.merge(df_gdp_uk, on='Year', how='inner')
df_merged = df_merged.merge(df_schooling_uk, on='Year', how='inner')
df_merged = df_merged.merge(df_working_hours_uk, on='Year', how='inner')

# Drop any rows with missing data (NaNs) after merging, as regression requires complete data points
df_merged.dropna(inplace=True)

if df_merged.empty:
    print("Error: The datasets do not have overlapping years for the UK to perform the analysis.")
    print("Please check the 'Year' column in all four files for 'United Kingdom' data.")
    exit()

print(f"Successfully merged {len(df_merged)} data points for the UK (Years {df_merged['Year'].min()} to {df_merged['Year'].max()}).")
print("-" * 50)

# Define the dependent (Y) and independent (X) variables
Y = df_merged['Divorce_Rate']
X = df_merged[['GDP_Per_Capita', 'Years_of_Schooling', 'Annual_Working_Hours']]

# Add a constant to the independent variables for the intercept term in the regression model
X = sm.add_constant(X)

# Create and fit the OLS (Ordinary Least Squares) model
model = sm.OLS(Y, X).fit()


# Print a summary of the regression
print("Multi-Variable Regression Analysis: UK Divorce Rate vs. Socioeconomic Factors")
print("Dependent Variable: Crude divorce rate (per 1000 people)")
print("-" * 70)
print(model.summary().as_text())
print("-" * 70)

# Interpret the results to clearly identify the best predictor
print("\n--- Interpretation of Results ---")

# Extract the p-values and coefficients for comparison
results_df = model.summary2().tables[1].reset_index()
results_df.columns = ['Variable', 'Coefficient', 'StdErr', 't', 'P>|t|', 'CI_L', 'CI_U']

# Filter out the constant term
predictor_results = results_df[results_df['Variable'] != 'const']

# Check for statistically significant variables (p-value < 0.05)
significant_predictors = predictor_results[predictor_results['P>|t|'] < 0.05]

if significant_predictors.empty:
    print("\nConclusion: None of the independent variables (GDP, Schooling, Working Hours) are statistically significant predictors of the UK Divorce Rate in this model (at the 5% significance level).")
    print("The model's R-squared value is {:.3f}, suggesting these variables collectively explain {:.1f}% of the variance in divorce rates.".format(model.rsquared, model.rsquared * 100))
else:
    # Identify the best predictor: the one with the lowest P-value (most statistically significant)
    best_predictor = significant_predictors.loc[significant_predictors['P>|t|'].idxmin()]
    
    print("Statistically Significant Predictors (p < 0.05):")
    for index, row in significant_predictors.iterrows():
        sign = "Positive" if row['Coefficient'] > 0 else "Negative"
        print(f"- {row['Variable']} (P-value: {row['P>|t|']:.4f}): A {sign} relationship with Divorce Rate.")

    print(f"\nConclusion: The best predictor of UK Divorce Rate in this model is **{best_predictor['Variable']}**.")
    print(f"It has the lowest P-value ({best_predictor['P>|t|']:.4f}), indicating the strongest statistical significance.")
    
    # Calculate the explained variance
    print(f"\n(The model's overall R-squared is {model.rsquared:.3f}, meaning these variables explain {model.rsquared * 100:.1f}% of the variance in divorce rates.)")
    print("\n the sign of the coefficient indicates the direction of the relationship.")