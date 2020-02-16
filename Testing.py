import random
from Main import MESSAGES_DB
from Date_Management import WhatsApp_Messages_Calendar

JOAN_DB = MESSAGES_DB["Sklyvan"]
RANDOM_MESSAGE = random.choice(JOAN_DB)
MyCalendar = WhatsApp_Messages_Calendar()
MyCalendar.AddMessage(RANDOM_MESSAGE)

print(RANDOM_MESSAGE.Date)
MyYear = MyCalendar.Years[0]
print("Year: ", len(MyYear))
for MyMonth in MyYear.Months:
    print("     Month: ", len(MyMonth))
    for MyWeek in MyMonth.Weeks:
        print("         Week: ", len(MyWeek))
        
breakpoint()