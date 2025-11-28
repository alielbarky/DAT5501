import numpy as np
from scipy.stats import triang
import pandas as pd
import matplotlib.pyplot as plt

#random seed for reproducibility
np.random.seed(42)

#1. set up the parameters
num_iterations = 20000  #Number of simulation runs
time_horizon = 20    # time horizon for each simulation
years = np.arange(1, time_horizon + 1)
mpc = 0.11           # marginal propensity to consume (MPC) assumed to be constant and taken to be 0.11 in New York which is the current estimate according to federal reserve bank of New York
multiplier = 1 / (1 - mpc) # well accepted equation by economists for multiplier effect based on MPC 
boost_factor = multiplier - 1   #the amount of the multiplier in excess of the original money spent

#multiplier time lag distribution (Spread over 4 years)
#the multiplier effect has a time delay until it kicks in
#many eonomists agree that the time lag is distributed like the model below
lag_distribution = {
    1: 0.20,  # t+1: 20% of boost hits
    2: 0.30,  # t+2: 30% of boost hits
    3: 0.30,  # t+3: 30% of boost hits
    4: 0.20   # t+4: 20% of boost hits
}

#2. parameter distributions (in $ Billions)
# Tax Revenue (Normal distribution: μ, σ)
tax_rev_mean = 9.5
tax_rev_std = 1.0 # to account for uncertainty

#childcare Cost (Normal distribution: μ, σ)
childcare_mean = 6.0
childcare_std = 0.5 #to account for uncertainty

#free Bus Cost (Normal distribution: μ, σ)
free_bus_mean = 0.7115
free_bus_std = 0.15 #to account for uncertainty

# Subsidised Grocery Cost (triangular: min, mode, max). Triangular since there is no real world cost data for such a program so higher uncertainty.
#start up costs were ignored here as it is a one time payment so i only focused on operational costs
grocery_min = 0.010
grocery_mode = 0.030
grocery_max = 0.050

#rent freeze Subsidy Cost (Normal distribution: μ, σ)
rent_subsidy_mean = 1.5
rent_subsidy_std = 0.5
rent_subsidy_prob = 0.05   #this models the probability that costs for landlords rise so much that the city has to cover the difference to keep rents frozen

# Other Spending Fraction (OSF) (Triangular: min, mode, max)
#this is to accouunt for other spend commitments not modelled here
osf_min = 0.10
osf_mode = 0.15
osf_max = 0.25

# pre-calculate constants for scipy.stats.triang
osf_c = (osf_mode - osf_min) / (osf_max - osf_min)
grocery_c = (grocery_mode - grocery_min) / (grocery_max - grocery_min)
grocery_scale = grocery_max - grocery_min
osf_scale = osf_max - osf_min

#3. storing outcomes for simulation
accumulated_fiscal_position = np.zeros(num_iterations)
rent_crisis_triggered = np.zeros(num_iterations, dtype=bool)
annual_failure_count = np.zeros(num_iterations)

#4. main Monte Carlo Loop
for i in range(num_iterations):
    #arrays to store annual results for this run
    total_cost_t = np.zeros(time_horizon)
    
    #tracking subsidy status 
    subsidy_active = False
    net_position_run = 0.0
    
    #annual time loop
    for t in years:
        year_index = t - 1
        
        #Sample revenue and costs
        tax_rev_t = np.random.normal(tax_rev_mean, tax_rev_std)
        childcare_cost = np.random.normal(childcare_mean, childcare_std)
        free_bus_cost = np.random.normal(free_bus_mean, free_bus_std)
        grocery_cost = triang.rvs(loc=grocery_min, scale=grocery_scale, c=grocery_c)
        
        #determine the probabilistic rent freeze cost
        rent_freeze_cost = 0.0
        
        if subsidy_active or np.random.rand() < rent_subsidy_prob:
            rent_freeze_cost = np.random.normal(rent_subsidy_mean, rent_subsidy_std)
            rent_freeze_cost = max(0, rent_freeze_cost) # ensure cost is non-negative
            
            rent_crisis_triggered[i] = True
            subsidy_active = True
        else:
            subsidy_active = False
            
        #calculate total annual cost
        total_cost_run = childcare_cost + free_bus_cost + grocery_cost + rent_freeze_cost
        total_cost_t[year_index] = total_cost_run
        
        #Check annual budget constraint (OSF)
        osf_t = triang.rvs(loc=osf_min, scale=osf_scale, c=osf_c)
        
        required_other_spending = tax_rev_t * osf_t
        total_required_spending = total_cost_run + required_other_spending
        
        #Calculate net spending (surplus or deficit)
        net_spending_t = tax_rev_t - total_required_spending
        
        if tax_rev_t < total_required_spending:
            annual_failure_count[i] += 1
            
        #Apply multiplier
        economic_boost = 0.0
        
        for lag in lag_distribution:
            lag_index = year_index - lag
            if lag_index >= 0:
                boost_from_lag = total_cost_t[lag_index] * boost_factor * lag_distribution[lag]
                economic_boost += boost_from_lag
                
        #update net position
        net_position_run += net_spending_t + economic_boost

    #store final accumulated position for this run
    accumulated_fiscal_position[i] = net_position_run

#summary statistics

#mean net accumulated fiscal position
mean_net_position = np.mean(accumulated_fiscal_position)

# % of runs net fiscal position was negative
prob_failure = np.mean(accumulated_fiscal_position < 0) * 100

# C. 5th Percentile Net Accumulated Position (Maximum Plausible Risk)
fifth_percentile = np.percentile(accumulated_fiscal_position, 5)

#policy risk metrics i.e. a rent crisis
prob_rent_crisis = np.mean(rent_crisis_triggered) * 100
mean_annual_failure_rate = np.mean(annual_failure_count > 0) * 100

#visualisation (Probability distribution function and histogram)


#I was not familiar with making probability distribution functions so this section of the code is largely AI generated
plt.figure(figsize=(10, 6))
# Using a KDE plot to estimate the PDF
pd.Series(accumulated_fiscal_position).plot(kind='kde', linewidth=3, color='#4682B4', label='Distribution of Final Outcomes (PDF)')

# Add the mean and 5th percentile lines
plt.axvline(mean_net_position, color='green', linestyle='--', linewidth=1.5, label=f'Mean: ${mean_net_position:.2f}B')
plt.axvline(fifth_percentile, color='red', linestyle=':', linewidth=1.5, label=f'5th Percentile: ${fifth_percentile:.2f}B')
plt.axvline(0, color='black', linestyle='-', linewidth=1.0, label='Break-Even Point ($0B)')

plt.title('1. Probability Density Function (PDF) of Accumulated Fiscal Position (20 Years)', fontsize=14)
plt.xlabel('Net Accumulated Fiscal Position ($ Billions)', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.legend(loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
plt.savefig('accumulated_fiscal_position_pdf.png')


#Histogram
plt.figure(figsize=(10, 6))
plt.hist(accumulated_fiscal_position, bins=50, color='#4682B4', edgecolor='black', alpha=0.7, density=True, label='Frequency of Final Outcomes (Histogram)')

# Add the mean and 5th percentile lines
plt.axvline(mean_net_position, color='green', linestyle='--', linewidth=1.5, label=f'Mean: ${mean_net_position:.2f}B')
plt.axvline(fifth_percentile, color='red', linestyle=':', linewidth=1.5, label=f'5th Percentile: ${fifth_percentile:.2f}B')
plt.axvline(0, color='black', linestyle='-', linewidth=1.0, label='Break-Even Point ($0B)')

plt.title('2. Histogram of Accumulated Fiscal Position (20 Years)', fontsize=14)
plt.xlabel('Net Accumulated Fiscal Position ($ Billions)', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.legend(loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
plt.savefig('accumulated_fiscal_position_histogram.png')

print("Monte Carlo Simulation Results (20-Year Horizon)")
print("")
print(f"Total Iterations: {num_iterations}")
print(f"Economic Multiplier (k): {multiplier:.3f}")

print("\n Mean Net Accumulated Fiscal Position (20 Years)")
print(f"Expected Outcome: ${mean_net_position:.2f} Billion (Average Surplus/Deficit)")

print("\n Probability of Fiscal Failure")
print(f"% of Runs with Accumulated Deficit: {prob_failure:.2f}%")

print("\n Maximum Plausible Risk Exposure (5th Percentile)")
print(f"Worst 5% Outcome: ${fifth_percentile:.2f} Billion (Accumulated Deficit)")

print("\n Policy Risk Metrics")
print(f"Rent Subsidy Triggered (at least once): {prob_rent_crisis:.2f}% of runs")
print(f"Annual Budget Constraint Failure (at least once): {mean_annual_failure_rate:.2f}% of runs (Budget too small for all required spending)")

print("\n plots generated and saved")