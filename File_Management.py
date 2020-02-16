def Get_File_Data(FILE_PATH):
    FILE = open(FILE_PATH, "r", encoding="utf8") # Using 'utf8' encoding to avoid exceptions caused by the rare chars on the chat.
    # For every line on the file, if its not a line containing '<Media omitted>', I save the line without the \n char.
    FILE_CONTENT = [fileLine.replace("\n", "") for fileLine in FILE.readlines() if '<Media omitted>' not in fileLine and 'Messages to this chat and calls are now secured with end-to-end encryption. Tap for more info.' not in fileLine and
                    'security code changed. Tap for more info.' not in fileLine]
    FILE_DATA = []
    Position = 0
    for i in range (len(FILE_CONTENT)):
        fileLine = FILE_CONTENT[i]
        if len(fileLine) >= 17:
            if fileLine[2] == '/' and fileLine[5] == '/' and fileLine[14] == ":":
                FILE_DATA.append(fileLine)
                Position += 1
            else:
                FILE_DATA[Position-1] += fileLine
    return FILE_DATA
