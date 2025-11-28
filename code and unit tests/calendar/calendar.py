
#define function to check inputs are valid
def check_input(prompt, min_val):
    # While loop to keep asking until we get a valid number
    while True:
        try:
            # convert input into a whole number if it's not already
            value = int(input(prompt))
            # check if number is in the right range e.g.atleast 28 for dayss in a month 
            if value >= min_val:
                return value
            else:
                print(f"The value has to be at least {min_val}. Try again.")
        except ValueError:
            # If they typed letters or a decimal, this catches it!
            print("Looks like that wasn't a valid number. Try again.")

def calendar():
    # get inputs from user and validate them
    days_in_month = check_input("Enter the number of days in the month (e.g., 30 or 31): ", 28)
    start_day_index = check_input("What day does the month start on? (Enter 1 for Sunday, 2 for Monday, ..., 7 for Saturday): ", 1)
    
    # check the start day index is not bigger than 7
    if start_day_index > 7:
        print("invalid weekday entered, sunday is assumed to be the start day")
        start_day_index = 1

    print("\n" + "=" * 25)
    print(" S  M  T  W  T  F  S") 
    
    #fill the empty spots before the start day
    output_line = ""
    for _ in range(start_day_index - 1):
        output_line += " - " 

    # print the actual dates
    for day_num in range(1, days_in_month + 1):
        day_str = f"{day_num:2d} " 
        output_line += day_str

        # if the day's total position is divisibke by 7 we start a new line
        if (day_num + start_day_index - 1) % 7 == 0:
            print(output_line.rstrip())
            output_line = "" # Clear the line to start the next one

    #print out leftover days
    if output_line:
        print(output_line.rstrip())
    
    print("=" * 25)
calendar()