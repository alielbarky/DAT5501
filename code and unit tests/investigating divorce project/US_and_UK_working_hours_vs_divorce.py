import pandas as pd
import matplotlib.pyplot as plt

# Load working hours data
working_hours_df = pd.read_csv(r"data\annual-working-hours-per-worker.csv")
# Load divorce rate data
divorce_rate_df = pd.read_csv(r"data\US and UK divorces-per-1000-people.csv")

#Clean and rename columns for clarity
divorce_rate_df = divorce_rate_df.rename(columns={'Crude divorce rate(per 1000 people)': 'Divorce Rate'}
)
working_hours_df = working_hours_df.rename(columns={'Annual Working hours per worker': 'Working Hours'})
countries_to_plot = ['United States', 'United Kingdom']
wh_filtered = working_hours_df[working_hours_df['Entity'].isin(countries_to_plot)]
dr_filtered = divorce_rate_df[divorce_rate_df['Entity'].isin(countries_to_plot)]

#pivot the tables to have Country (Entity) as a column for easier plotting
wh_pivot = wh_filtered.pivot(index='Year', columns='Entity', values='Working Hours')
dr_pivot = dr_filtered.pivot(index='Year', columns='Entity', values='Divorce Rate')

# Merge the two pivoted tables by year
combined_df = wh_pivot.join(dr_pivot, how='inner', lsuffix=' - Working Hours', rsuffix=' - Divorce Rate').reset_index()
# Drop rows with any missing values that might occur from the join
combined_df = combined_df.dropna()
# Ensure Year is integer for clean plotting
combined_df['Year'] = combined_df['Year'].astype(int)


#Create figure and primary axes for Working Hours
fig, ax1 = plt.subplots(figsize=(12, 6))

# Set title and background style
plt.style.use('seaborn-v0_8-whitegrid')
fig.suptitle('Annual Working Hours vs. Crude Divorce Rate (US & UK)', fontsize=16, fontweight='bold')
color_wh = 'tab:blue'
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Annual Working Hours per Worker', color=color_wh, fontsize=12)

# US Working Hours (Solid Line)
line1, = ax1.plot(combined_df['Year'], combined_df['United States - Working Hours'], color=color_wh, linestyle='-', linewidth=2, label='US - Working Hours')
# UK Working Hours (Dashed Line)
line2, = ax1.plot(combined_df['Year'], combined_df['United Kingdom - Working Hours'], color=color_wh, linestyle='--', linewidth=2, label='UK - Working Hours')

ax1.tick_params(axis='y', labelcolor=color_wh)
ax1.grid(True, linestyle=':', alpha=0.6)

#create Secondary axes for divorce rate
ax2 = ax1.twinx()
color_dr = 'tab:red'
ax2.set_ylabel('Crude Divorce Rate (per 1000 people)', color=color_dr, fontsize=12)

# US Divorce Rate(Solid Line)
line3, = ax2.plot(combined_df['Year'], combined_df['United States - Divorce Rate'], color=color_dr, linestyle='-', linewidth=2, label='US - Divorce Rate')
#UK Divorce Rate(Dashed Line)
line4, = ax2.plot(combined_df['Year'], combined_df['United Kingdom - Divorce Rate'], color=color_dr, linestyle='--', linewidth=2, label='UK - Divorce Rate')

ax2.tick_params(axis='y', labelcolor=color_dr)

# legend
lines = [line1, line2, line3, line4]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='lower center', bbox_to_anchor=(0.5, -0.55), ncol=2, frameon=True, shadow=True, fancybox=True, fontsize=10)

# Configure X-axis for better readability (showing every 5th year)
start_year = combined_df['Year'].min()
end_year = combined_df['Year'].max()
year_ticks = range(start_year, end_year + 1, 5)
ax1.set_xticks(year_ticks)
ax1.tick_params(axis='x', rotation=45)
plt.tight_layout(rect=[0, 0.1, 1, 0.95]) 

plt.show()