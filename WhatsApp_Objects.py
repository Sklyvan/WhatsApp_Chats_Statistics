import datetime

class WhatsApp_Message_Date:
    def __init__(self, DayString, TimeString):
        self.DayString = DayString
        self.TimeString = TimeString
        self.Day = int(DayString[:2])
        self.Month = int(DayString[3:5])
        self.Year = int(DayString[6:10])
        self.Hour = int(TimeString[:2])
        self.Minutes = int(TimeString[3:5])
        self.DateTime = datetime.datetime(self.Year, self.Month, self.Day) # Saving the date into 'datetime' library format.
        self.WeekDay = self.DateTime.weekday() # Numeric week day.
        self.WeekDay_String = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"][self.WeekDay]
        self.Month_String = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"][self.Month-1]

    def __str__(self):
        return str(self.DayString) + str(" ") + str(self.TimeString)

class WhatsApp_Message_Text:
    def __init__(self, Message):
        """
        :param Message: Text messages with rare chars, emojis...
        """
        self.Message = Message
        self.LowerMessage = Message.lower() # WhatsApp message with ONLY lowercase letters.
        self.Emojis = [] # List of all the emojis on this message.
        for MessageChar in self.LowerMessage:
            if MessageChar.lower() in 'áàéèíìóòúù': # Removing accent mark because spanish sucks.
                i = 'áàéèíìóòúù'.index(MessageChar)
                ReplaceChar = ''
                if i == 0 or i == 1:
                    ReplaceChar = 'a'
                elif i == 2 or i == 3:
                    ReplaceChar = 'e'
                elif i == 4 or i == 5:
                    ReplaceChar = 'i'
                elif i == 6 or i == 7:
                    ReplaceChar = 'o'
                elif i == 8 or i == 9:
                    ReplaceChar = 'u'
                self.LowerMessage = self.LowerMessage.replace(MessageChar, ReplaceChar)
            elif (ord(MessageChar) < 97 or ord(MessageChar) > 122) and MessageChar != ' ': # If the character is not a text char, we delete it.
                self.LowerMessage = self.LowerMessage.replace(MessageChar, '')
                
            if ord(MessageChar) >= 127987 and ord(MessageChar) <= 129535: # If the char is a emoji, we add to the emojis list.
                self.Emojis.append(MessageChar)
        self.Words = self.LowerMessage.split() # Just lowercase words, using it to count the most used words.

    def __str__(self):
        return self.Message

    def __len__(self):
        return len(self.Message)

class WhatsApp_Message:
    def __init__(self, Message_Text, Message_Date):
        Date_Array = Message_Date.split(', ')
        try:
            self.Message = WhatsApp_Message_Text(Message_Text[Message_Text.index(":")+2:]) # Removing the message sender name. (Ex: SenderName: Message)
        except ValueError:
            breakpoint()
        self.Sender = Message_Text[:Message_Text.index(":")]
        self.Date = WhatsApp_Message_Date(Date_Array[0], Date_Array[1]) # Saved as 'DD/MM/YYYY Hours:Minutes'

    def GetWords(self):
        return self.Message.Words

    def GetEmojis(self):
        return self.Message.Emojis

    def __len__(self):
        return len(self.Message)

    def __str__(self):
        return str(self.Message)
