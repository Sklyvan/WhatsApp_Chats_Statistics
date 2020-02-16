from File_Management import Get_File_Data
from WhatsApp_Objects import WhatsApp_Message
from Data_Visualization import GenerateBarsPlot, GeneratePlot, GenerateDotsPlot
from Date_Management import WhatsApp_Messages_Calendar

FILE_DATA = Get_File_Data('./WhatsApp_DB/Lidia_DB.txt')
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