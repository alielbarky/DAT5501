import numpy as np
#define a function that takes a date as a parameter and calculates the duration between that date and today
def duration_calculator(date_str):
    input_date = np.datetime64(date_str, 'D')
    today = np.datetime64('today', 'D')
    return ( today - input_date).astype(int)

#ask the user for a date
date_input = input ("Enter a date (YYYY-MM-DD): ").strip()

#add error handling and how to handle future dates

try:
    #Call the function to calculate duration
    days = duration_calculator(date_input)
        
    #Check if date is for past or future
    if days > 0:
        #Past Date
        print(f"{days} days have passed since {date_input}.")
    elif days < 0:
        #Future Date (result is negative)
        days_until = abs(days)
        print(f"{days_until} days until {date_input}.")
    else:
        print(" That's today, 0 days passed.")
            
except ValueError:
    #Handle invalid input format
    print(f"Error: Could not understand '{date_input}'. Please re-run the program and use the **YYYY-MM-DD** format. ")

#call the function to calculate duration
days = duration_calculator(date_input)