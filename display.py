from libs.functions import indent
from libs.waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont 
from time import sleep
from gpiozero import Button              
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
from os import path
from glob import glob
from math import ceil
from textwrap import wrap

btn1 = Button(5)
btn2 = Button(6)
btn3 = Button(13)
btn4 = Button(19) 
fonts_dir='fonts/'
BOOKFONT = fonts_dir + 'DejaVuSansMono.ttf'
LARGEFONT = fonts_dir + 'Lobster-Regular.ttf'
fontBook = ImageFont.truetype(BOOKFONT,10)
fontLg = ImageFont.truetype(LARGEFONT,44)
fontMenu = ImageFont.truetype(BOOKFONT,10)
fontBookTitle = ImageFont.truetype(BOOKFONT,20)
refreshCount = 0
pageNum = 0
bookNum = 0
bookLen = 0
#screenWidthChar = 0
#screenHeightChar = 0
books_dir='books/'
cache_dir='cache/'
bookNameList = []
fullBook = []
bookListFull = sorted(glob(books_dir + "*.epub"))
for i in bookListFull:
    x = i.split('/')
    bookNameList.append(x[-1])
epd = epd2in7.EPD() #264 by 174
h = epd.height
w = epd.width
epd.init()              # initialize the display
epd.Clear()             # clear the display


def getCharScrSz(font,font2):
    global screenWidthChar
    global screenWidthCharBT
    global screenHeightChar
    global screenHeightCharBT
    global lineHeight
    global lineHeightBT
    charStr=''
    while font.getsize(charStr)[0] < (w-6):
        charStr += 'a'
    screenWidthChar = len(charStr)
    screenHeightChar = round((h-30) / font.getsize(charStr)[1])
    lineHeight = font.getsize(charStr)[1]
    charStr=''
    while font2.getsize(charStr)[0] < (w-6):
        charStr += 'a'
    screenWidthCharBT = len(charStr)
    screenHeightCharBT = round((h-30) / font2.getsize(charStr)[1])
    lineHeightBT = font2.getsize(charStr)[1]

def checkLastRead():
    global book
    global bookNum
    if path.exists(cache_dir + 'last-read.cache'):
        f = open(cache_dir + 'last-read.cache')
        book = f.read()
        bookNum = bookNameList.index(book)
        f.close()
    else:
        book = bookNameList[bookNum]

def checkLastPage():
    global pageNum
    global bookLen
    if path.exists(cache_dir + book.split('.')[0] + '.cache'):
        f = open(cache_dir + book.split('.')[0] + '.cache')
        pageNumStr = f.read()
        pageNum = int(pageNumStr)
        bookLen = ceil(len(fullBook) / screenHeightChar)
        f.close()
    else:
        pageNum = 0
        bookLen = ceil(len(fullBook) / screenHeightChar)
 
def pageNumCache():
    bookLen = ceil(len(fullBook) / screenHeightChar)
    bookFileName=book.split('.')
    f = open(cache_dir + bookFileName[0]+'.cache','w')
    f.write(str(pageNum))
    f.close()

def lastReadCache():
    f = open(cache_dir + 'last-read.cache','w')
    f.write(book)
    f.close

def printToDisplay(string):
    HBlackImage = Image.new('1', (w, h), 255)  # 264x174
    draw = ImageDraw.Draw(HBlackImage)
    draw.text((indent(string,fontLg,w), 2), string, font = fontLg, fill = 0)
    bookVar = epub.read_epub(books_dir + book)
    bookTitle = bookVar.get_metadata('DC','title')[0][0]
    bookTitleWrap = wrap(bookTitle,width=screenWidthCharBT)
    x = 1
    for i in bookTitleWrap:
        draw.text((indent(i,fontBookTitle,w),70+x*lineHeightBT),i,font=fontBookTitle,fill=0)
        x+=1
    printMenuInterface(draw)
    screenCleanup()
    epd.display(epd.getbuffer(HBlackImage))

def printToSplash(string):
    HBlackImage = Image.new('1', (w, h), 255)  # 264x174
    draw = ImageDraw.Draw(HBlackImage)
    draw.text((indent(string,fontLg,w), 90), string, font = fontLg, fill = 0)
    screenCleanup()
    epd.display(epd.getbuffer(HBlackImage))

def printInterface(draw):
    draw.line((0,250,174,250),fill=0,width=1)
    draw.line((43,250,43,264),fill=0,width=1)
    draw.line((87,250,87,264),fill=0,width=1)
    draw.line((130,250,130,264),fill=0,width=1)
    draw.text((indent('Menu',fontMenu,w/4),250),'Menu',font=fontMenu,fill=0)
    draw.text((indent('Prev',fontMenu,w/4)+43,250),'Prev',font=fontMenu,fill=0)
    draw.text((indent('Next',fontMenu,w/4)+87,250),'Next',font=fontMenu,fill=0)
    draw.text((indent('Back',fontMenu,w/4)+130,250),'Back',font=fontMenu,fill=0)
    draw.text((indent(str(pageNum),fontMenu,w)+80, 235), str(pageNum), font = fontMenu, fill = 0)

def printMenuInterface(draw):
    draw.line((0,250,174,250),fill=0,width=1)
    draw.line((43,250,43,264),fill=0,width=1)
    draw.line((87,250,87,264),fill=0,width=1)
    draw.line((130,250,130,264),fill=0,width=1)
    draw.text((indent('Sel.',fontMenu,w/4),250),'Sel.',font=fontMenu,fill=0)
    draw.text((indent('Prev',fontMenu,w/4)+43,250),'Prev',font=fontMenu,fill=0)
    draw.text((indent('Next',fontMenu,w/4)+87,250),'Next',font=fontMenu,fill=0)
    draw.text((indent('Quit',fontMenu,w/4)+130,250),'Quit',font=fontMenu,fill=0)

def loadBook(bookPath):
    global fullBook
    fullBook = []
    bookRead = epub.read_epub(bookPath)
    for chapter in bookRead.get_items_of_type(ebooklib.ITEM_DOCUMENT): # loop all chapters in book
        soup = BeautifulSoup(chapter.get_body_content(),'html5lib')
        chapterString = soup.get_text()
        chapterString = chapterString.replace("\t","").replace("\r","").replace("    "," ")##.replace("\n","")
        chapterText = wrap(chapterString,width=screenWidthChar)
        for x in chapterText: # append chapter to fullBook
            fullBook.append(x)

def printPage(pageNum):
    HBlackImage = Image.new('1', (w, h), 255)  # 264x174
    draw = ImageDraw.Draw(HBlackImage)
    for i in range(screenHeightChar):
        listIndex = (pageNum * screenHeightChar) + i
        if listIndex < len(fullBook):
            draw.text((1,i*lineHeight),fullBook[listIndex],font=fontBook,fill=0)
    printInterface(draw)
    screenCleanup()
    epd.display(epd.getbuffer(HBlackImage))
    pageNumCache()
    lastReadCache()

def screenCleanup():
    global refreshCount
    refreshCount +=1
    if refreshCount == 10:
        epd.init()
        epd.Clear()
        refreshCount = 0

def nextPage():
    global pageNum
    pageNum +=1

def prevPage():
    global pageNum
    if pageNum > 0:
        pageNum -=1

def nextBook():
    global book
    global bookNum
    if bookNum < len(bookNameList): 
        bookNum +=1
    book = bookNameList[bookNum]

def prevBook():
    global book
    global bookNum
    if bookNum > 0:
        bookNum -=1
    book = bookNameList[bookNum]
    
def handleBtnPress(btn):
    if btn.pin.number == 5:
        printPage(pageNum)
    if btn.pin.number == 6:
        prevPage()
        printPage(pageNum)
    if btn.pin.number == 13:
        nextPage()
        printPage(pageNum) 
    if btn.pin.number == 19:
        printToDisplay('Welcome!')

def handleMenuBtn(btn):
    if btn.pin.number == 6:
        prevBook()
        printToDisplay('Welcome!')
    if btn.pin.number == 13:
        nextBook()
        printToDisplay('Welcome!')
    if btn.pin.number == 19:
        printToSplash('Goodbye')

def menuLoop():
    global books_dir
    global book
    global bookNum
    while True:
        if btn1.is_pressed:
            printToSplash('Loading')
            checkLastPage()
            loadBook(books_dir + book)
            pageTurnLoop()
        btn2.when_pressed = handleMenuBtn
        btn3.when_pressed = handleMenuBtn
        if btn4.is_pressed:
            btn4.when_pressed = handleMenuBtn
            sleep(3)
            raise Exception("Quit")

def pageTurnLoop():
    printPage(pageNum)
    while True:
        btn2.when_pressed = handleBtnPress
        btn3.when_pressed = handleBtnPress
        if btn4.is_pressed:
            btn4.when_pressed = handleBtnPress
            sleep(1.5)
            break

try:
    getCharScrSz(fontBook,fontBookTitle)
    checkLastRead()
    printToDisplay('Welcome!')
    menuLoop()

except IOError as e:
    print(e)
