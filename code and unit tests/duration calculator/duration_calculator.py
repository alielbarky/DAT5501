import numpy as np
#define a function that takes a date as a parameter and calculates the duration between that date and today
def duration_calculator(date_str):
    input_date = np.datetime64(date_str, 'D')
    today = np.datetime64('today', 'D')
    return ( today - input_date).astype(int)
#ask the user for a date
date = input ("Enter a date (YYYY-MM-DD): ")
#call the function to calculate duration
days = duration_calculator(date)
print(f"{days} days have passed since {date}.")