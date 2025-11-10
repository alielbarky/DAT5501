#take inputs from a user
days_in_month = int(input("how many days in this month : "))
start_day=input("what day do you want the month to start on e.g. Monday, Tuesday etc. : ").lower
days=["sunday","monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
if start_day in days:
    position=int(days.index(start_day))
else:
    print("error, you did not enter a valid day, re-run the code")
print("S M T W T F S ")
print("_ _ _ _ _ _ _")
print(7 * "-")
print(int(days.index(start_day)))