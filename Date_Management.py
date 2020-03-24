import datetime, calendar
from WhatsApp_Exceptions import DateTimeError, SearchingMessageError, AddMessageError
from WhatsApp_Objects import WhatsApp_Message

class WhatsApp_Messages_Calendar:
    def __init__(self):
        self.Years = [] # Years as objects.
        self.YearsList = [] # Years as strings.
        self.Messages = [] # WhatsApp Message objects.
        self.WordsCounter = {} # DICT[Word] = Number of times used.

    def AddMessage(self, Message):
        if Message.Date.Year not in self.YearsList:
            CurrentYear = Year(Message.Date.Year)
            self.Years.append(CurrentYear)
            self.YearsList.append(Message.Date.Year)
        else:
            CurrentYear = self.Years[(self.YearsList.index(Message.Date.Year))]

        if type(Message) is WhatsApp_Message:
            MessageDay = Message.Date # Message date as 'DD/MM/YYYY'.
            CurrentMonth =  CurrentYear[MessageDay.Month-1] # Getting the month object.
            # Now, since the month object contains week objects, we are going to get the week number of the date that we have, and getting the week.
            CurrentDay = CurrentMonth[CurrentMonth.Get_WeekNumber(MessageDay.Day)-1][MessageDay.WeekDay]
            CurrentDay.AddMessage(Message)
            self.Messages.append(Message)
            for MessageWord in Message.GetWords():
                if MessageWord in self.WordsCounter:
                    self.WordsCounter[MessageWord] = self.WordsCounter[MessageWord] + 1
                else:
                    self.WordsCounter[MessageWord] = 1
        else:
            raise AddMessageError(f"The object which you're trying to add isn't a WhatsApp_Message, is {type(Message)}.")

    def __getitem__(self, itemKey):
        try:
            return self.Messages[itemKey]
        except IndexError:
            raise SearchingMessageError(f"Wrong message number, number can't be bigger than {len(self.Messages)-1}, your message number is {itemKey}")

    def __str__(self):
        return (f"Calendar with years {str(self.YearsList).replace('[', '').replace(']', '')}.")

    def __len__(self):
        n = 0
        for CurrentYear in self.Years:
            n += len(CurrentYear)
        return n

class Year:
    def __init__(self, Year):
        self.Year = Year
        self.Months = []
        for i in range (12):
            NewMonth = Month(i+1, Year)
            self.Months.append(NewMonth)

        if Year % 4 == 0 and Year % 100 != 0 or Year % 400 == 0:
            self.isLeap = True
        else:
            self.isLeap = False

    def __getitem__(self, itemKey):
        try:
            return self.Months[itemKey]
        except IndexError:
            raise SearchingMessageError(f"Wrong month number, number can't be bigger than {len(self.Months)-1}, your month number is {itemKey}")

    def __len__(self):
        n = 0
        for YearMonth in self.Months:
            n += len(YearMonth)
        return n

    def __str__(self):
        if self.isLeap:
            return str(f'Year {self.Year}, the year is leap.')
        else:
            return str(f'Year {self.Year}.')

class Month:
    def __init__(self, Month, Year):
        self.Month = Month
        self.Year = Year
        self.MonthMatrix = calendar.monthcalendar(Year, Month)
        self.Weeks = []
        for CurrentWeek in self.MonthMatrix:
            """NonZeros = [i for i in CurrentWeek if i != 0] # Creating the array without zeros, we don't need the zeros since our days have a name and a WeekPosition value.
            WeekRange = tuple(i for i in range(min(NonZeros), max(NonZeros)+1))"""
            WeekRange = tuple(CurrentWeek)
            NewWeek = Week(WeekRange, Month, Year)
            self.Weeks.append(NewWeek)
        try:
            self.MonthName = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"][Month-1]
        except IndexError:
            raise DateTimeError(f'{Month} is an invalid month identificator, it should be between 1 and 12.')
        else:
            if Month in (1, 3, 5, 7, 8, 10, 12): # If the month has 31 days.
                self.Days = 31
            elif Month in (4, 6, 9, 11): # If the month has 30 days.
                self.Days = 30
            elif Month == 2: # Since February can have 28 or 29 days depending on the year.
                if Year % 4 == 0 and Year % 100 != 0 or Year % 400 == 0: # If we are on a Leap year, 28 days February.
                    self.Days = 29
                else:
                    self.Days = 28
            else:
                raise DateTimeError(f'Month number should be between 1 and 12, your value is {Month}.')

    def Get_WeekNumber(self, SearchDay):
        WeekNumber = 0
        for Week in self.MonthMatrix:
            WeekNumber += 1
            if SearchDay in Week:
                return WeekNumber
        return False

    def __getitem__(self, itemKey):
        try:
            return self.Weeks[itemKey]
        except IndexError:
            raise SearchingMessageError(f"Wrong week number, the number can't be bigger than {len(self.Weeks)-1}, your week number is {itemKey}.")

    def __len__(self):
        n = 0
        for MonthWeek in self.Weeks:
            n += len(MonthWeek)
        return n

    def __str__(self):
        return str(f'{self.MonthName.capitalize()} of year {self.Year}.')

class Week:
    def __init__(self, WeekRange, Month, Year):
        if len(WeekRange) > 7:
            raise DateTimeError(f"WeekRange tuple size can't be bigger than 7, your size is {len(WeekRange)}.")
        elif type(WeekRange) is not tuple:
            raise DateTimeError(f'WeekRange should be Tuple, yours is {type(WeekRange)}.')
        else:
            self.Days = [] # List containing the 7 days of this week.
            self.WeekRange = WeekRange
            self.Month = Month
            self.Year = Year
            for WeekDay in WeekRange:
                if WeekDay == 0:
                    self.Days.append(None)
                else:
                    try:
                        DayName = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"][datetime.datetime(Year, Month, WeekDay).weekday()]
                    except IndexError:
                        raise DateTimeError(f"Day number should be between 0-6, yours is {datetime.datetime(Year, Month, WeekDay).weekday()}")
                    else:
                        self.Days.append(Day(DayName, WeekDay, Month, Year))
            self.NonEmpy = [CurrentDay for CurrentDay in self.Days if CurrentDay != None]

    def __getitem__(self, itemKey):
        try:
            return self.Days[itemKey]
        except IndexError:
            raise SearchingMessageError(f'Wrong day number, size of the week is {len(self.Days)}, your day number is {itemKey}')

    def __len__(self):
        n = 0
        for WeekDay in self.NonEmpy:
            n += len(WeekDay)
        return n

    def __str__(self):
        return str("Week from ") + str(self.NonEmpy[0]) + str(" to ") + str(self.NonEmpy[-1]) + str(f' of the {self.Month} month, year {self.Year}.')

class Day:
    def __init__(self, DayName, Day, Month, Year, Messages=None):
        self.DayName = DayName
        self.Day = Day
        self.Month = Month
        self.Year = Year
        self.DateTime = datetime.datetime(Year, Month, Day)  # Saving the date into 'datetime' library format.
        self.WeekDay = self.DateTime.weekday()  # Numeric week day.
        if Messages:
            if type(Messages) is list:
                self.Messages = Messages
            else:
                self.Messages = [Messages]
        else:
            self.Messages = []

    def AddMessage(self, Message):
        self.Messages.append(Message)
        return Message

    def RemoveMessage(self, Message):
        self.Messages.remove(Message)
        return Message

    def RemoveMessageByPosition(self, Position):
        return self.Messages.pop(Position)

    def __add__(self, newMessage):
        if type(newMessage) is WhatsApp_Message:
            return self.AddMessage(newMessage)
        elif type(newMessage) is list:
            for currentMessage in newMessage:
                if type(currentMessage) is WhatsApp_Message:
                    self.AddMessage(currentMessage)
                else:
                    raise AddMessageError(f'The values inside the messages list, should be WhatsApp_Message, not {type(currentMessage)}, error found with {currentMessage} message.')
            return newMessage
        else:
            raise AddMessageError(f'The value added should be a list of WhatsApp_Message or a single WhatsApp_Message, not {type(newMessage)}.')

    def __getitem__(self, itemKey):
        try:
            return self.Messages[itemKey]
        except IndexError:
            raise SearchingMessageError(f'Message not found, this day has {len(self.Messages)} messages, your searched for {itemKey}.')

    def __str__(self):
        return str(self.DayName.capitalize()) + str(" ") + str(self.Day) + str("/") + str(self.Month) + str("/") + str(self.Year)

    def __len__(self):
        return len(self.Messages)