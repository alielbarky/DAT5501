#take inputs from a user
days_in_month = int(input("how many days in this month : "))
start_day=input("what day do you want the month to start on e.g. Monday, Tuesday etc. : ").lower()
days=["sunday","monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

position=int(days.index(start_day))
print(" S M T W T F S ")
print(position * " -")
counter = position
for count in range(days_in_month):
    print(days)