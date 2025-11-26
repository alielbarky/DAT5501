import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_name = r"data\ADVANCED MICRO DEVICES INC (12-04-2024 _ 11-26-2025).csv"
df = pd.read_csv(file_name)

#clean and prepare the data
# Convert 'Date' to datetime objects and set as index
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')

# Sort the data by date in ascending order
df = df.sort_index()

#calculate daily percentage change
df['Daily Change (%)'] = df['Close'].pct_change() * 100

#plot closing price vs. date
plt.figure(figsize=(12, 6))
plt.plot(df['Close'], label='Closing Price', color='blue')
plt.title('AMD Closing Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.savefig('amd_closing_price_plot.png')
plt.close()

#plot daily percentage change vs. date
plt.figure(figsize=(12, 6))
plt.plot(df['Daily Change (%)'], label='Daily Percentage Change', color='green')
plt.title('AMD Daily Percentage Change Over Time')
plt.xlabel('Date')
plt.ylabel('Daily Change (%)')
plt.legend()
plt.grid(True)
plt.savefig('amd_daily_change_plot.png')
plt.close()
print("plots generated and saved")