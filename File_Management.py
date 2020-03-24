from bs4 import BeautifulSoup as BS
import requests, urllib.request

URL = "https://unicode.org/emoji/charts/emoji-list.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
HTML_Page = requests.get(URL, headers=HEADERS)
MySoup = BS(HTML_Page.content, "html.parser")

def getFileData(FILE_PATH):
    FILE = open(FILE_PATH, "r", encoding="utf8") # Using 'utf8' encoding to avoid exceptions caused by the rare chars on the chat.
    # For every line on the file, if its not a line containing '<Media omitted>', I save the line without the \n char.
    FILE_CONTENT = [fileLine.replace("\n", "") for fileLine in FILE.readlines() if '<Media omitted>' not in fileLine and 'Messages to this chat and calls are now secured with end-to-end encryption. Tap for more info.' not in fileLine and
                    'security code changed. Tap for more info.' not in fileLine and 'Messages to this group are now secured with end-to-end encryption. Tap for more info.' not in fileLine and 'created group' not in fileLine and 'added ' not in fileLine and
                    'changed the subject' not in fileLine and 'changed this group' not in fileLine and 'changed the group description' not in fileLine and 'invite link' not in fileLine and 'left' not in fileLine and 'group description' not in fileLine and
                    'removed' not in fileLine and 'admin' not in fileLine]
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

def emojiToUnicode(Char, toScrap=False):
    if toScrap:
        return str((Char.encode('unicode_escape'))[5:]).replace('b', '').replace("'", "")
    else:
        return str('U+') + str((Char.encode('unicode_escape'))[5:]).replace('b', '').replace("'", "").upper()

def emojiToPNG(emojiUnicode):
    searchName = 'full-emoji-list.html#' + str(emojiUnicode)
    emojiURL = MySoup.findAll('a', href=searchName)[0].findAll('img')[0]['src']
    urllib.request.urlretrieve(emojiURL, emojiUnicode.upper()+str('.png'))
    return emojiUnicode.upper()+str('.png')