from File_Management import getFileData, emojiToUnicode, emojiToPNG
from WhatsApp_Objects import WhatsApp_Message
from Data_Visualization import GenerateBarsPlot, GeneratePlot, GenerateDotsPlot
from Date_Management import WhatsApp_Messages_Calendar

def GenerateCalendar(DataPath):
    FILE_DATA = getFileData(DataPath)
    MyCalendar = WhatsApp_Messages_Calendar()
    MESSAGES_DB = {}
    for FileMessage in FILE_DATA:
        MessageDate = (FileMessage.split(" - "))[0]
        MessageText = (FileMessage.split(" - "))[1]
        CurrentMessage = WhatsApp_Message(MessageText, MessageDate)
        if CurrentMessage.Sender in MESSAGES_DB:
            MESSAGES_DB[CurrentMessage.Sender].append(CurrentMessage)
        else:
            MESSAGES_DB[CurrentMessage.Sender] = [CurrentMessage]

        MyCalendar.AddMessage(CurrentMessage)

    return MyCalendar

def getDailyMessages(MyCalendar): # Returning a dictionary containing the day with the number of messages on this day. dailyMessages[DayObject] = int
    dailyMessages = {} # Keys are Day objects and values are the number of messages on this day.
    for currentYear in MyCalendar.Years:
        for currentMonth in currentYear.Months:
            for currentWeek in currentMonth.Weeks:
                for currentDay in currentWeek.Days:
                    if currentDay:
                        dailyMessages[currentDay] = len(currentDay)
    return dailyMessages

def getEmojisCounter(MyCalendar):
    emojisCounter = {}
    for currentMessage in MyCalendar.Messages:
        if len(currentMessage.GetEmojis()) != 0:
            for currentEmoji in currentMessage.GetEmojis():
                if currentEmoji in emojisCounter:
                    emojisCounter[currentEmoji] = emojisCounter[currentEmoji] + 1
                else:
                    emojisCounter[currentEmoji] = 1
    return emojisCounter

def getMessagesPerUser(MyCalendar):
    messagesPerUser = {}
    for currentMessage in MyCalendar.Messages:
        if currentMessage.Sender in messagesPerUser:
            messagesPerUser[currentMessage.Sender] = messagesPerUser[currentMessage.Sender] + 1
        else:
            messagesPerUser[currentMessage.Sender] = 1
    return messagesPerUser

def getMostActiveDays(dailyMessages, nDays=None):
    mostActiveDays = {}
    dictKeys = list(dailyMessages.keys()) # Day Objects.
    dictValues = list(dailyMessages.values()) # Integrers.
    if not nDays: nDays = len(dictKeys)
    for _ in range(nDays):
        maxDay = dictKeys[dictValues.index(max(dictValues))]
        mostActiveDays[maxDay] = max(dictValues)
        dictKeys.pop(dictValues.index(max(dictValues)))
        dictValues.remove(max(dictValues))
    return mostActiveDays

def getMostCommonWords(MyCalendar, nCommonWords=None):
    mostCommonWords = {}
    dictKeys = list(MyCalendar.WordsCounter.keys())  # Words Objects.
    dictValues = list(MyCalendar.WordsCounter.values())  # Integrers.
    if not nCommonWords: nCommonWords = len(dictKeys)
    for _ in range(nCommonWords):
        maxWord = dictKeys[dictValues.index(max(dictValues))]
        mostCommonWords[maxWord] = max(dictValues)
        dictKeys.pop(dictValues.index(max(dictValues)))
        dictValues.remove(max(dictValues))
    return mostCommonWords

def getMostCommonEmojis(emojisCounter, nEmojis=None):
    mostCommonEmojis = {}
    dictKeys = list(emojisCounter.keys())
    dictValues = list(emojisCounter.values())
    if not nEmojis: nEmojis = len(dictKeys)
    for _ in range(nEmojis):
        maxEmoji = dictKeys[dictValues.index(max(dictValues))]
        mostCommonEmojis[maxEmoji] = max(dictValues)
        dictKeys.pop(dictValues.index(max(dictValues)))
        dictValues.remove(max(dictValues))
    return mostCommonEmojis

def getMostMessagesPerUser(messagesPerUser, nUsers=None):
    mostMessagesPerUser = {}
    dictKeys = list(messagesPerUser.keys())
    dictValues = list(messagesPerUser.values())
    if not nUsers: nUsers = len(dictKeys)
    for _ in range(nUsers):
        maxUser = dictKeys[dictValues.index(max(dictValues))]
        mostMessagesPerUser[maxUser] = max(dictValues)
        dictKeys.pop(dictValues.index(max(dictValues)))
        dictValues.remove(max(dictValues))
    return mostMessagesPerUser

def getMostActiveDaysOfWeek(MyCalendar, nDays=None):
    mostActiveDaysOfWeek = {'MONDAY': 0, 'TUESDAY': 0, 'WEDNESDAY': 0, 'THURSDAY': 0, 'FRIDAY': 0, 'SATURDAY': 0, 'SUNDAY': 0}
    for currentMessage in MyCalendar.Messages:
        dayOfWeek = currentMessage.Date.WeekDay_String
        mostActiveDaysOfWeek[dayOfWeek] = mostActiveDaysOfWeek[dayOfWeek] + 1
    return mostActiveDaysOfWeek

MyCalendar = GenerateCalendar('./WhatsApp_DB/Group_DB.txt')
# emojisCounter = getMostCommonEmojis(getEmojisCounter(MyCalendar), 10)
# mostActiveDays = getMostActiveDays(getDailyMessages(MyCalendar), 10)
# mostCommonWords = getMostCommonWords(MyCalendar, 50)
# messagesPerUser = getMostMessagesPerUser(getMessagesPerUser(MyCalendar))
# GenerateBarsPlot(list(emojisCounter.values()), list(emojisCounter.keys()), 'blue')
# GeneratePlot()
mostActiveDaysOfWeek = getMostActiveDaysOfWeek(MyCalendar)
for dictKey in mostActiveDaysOfWeek:
    print(dictKey.capitalize(), mostActiveDaysOfWeek[dictKey])