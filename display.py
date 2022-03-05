import sys        
sys.path.insert(1, "./libs")             
from functions import indent
from libs.waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont 
from time import sleep
from gpiozero import Button              
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
import os.path
from os import path
import glob
from math import ceil
import textwrap

btn1 = Button(5)
btn2 = Button(6)
btn3 = Button(13)
btn4 = Button(19) 
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
refreshCount = 0
pageNum = 0
bookNum = 0
bookLen = 0
screenWidth = 29
screenHeight = 23
books_dir='books/'
cache_dir='cache/'
bookNameList = []
fullBook = []
bookListFull = sorted(glob.glob(books_dir + "*.epub"))
for i in bookListFull:
    x = i.split('/')
    bookNameList.append(x[-1])


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
        #pageNumList = [line.strip() for line in pageNumStr]
        pageNum = int(pageNumStr)
        bookLen = ceil(len(fullBook) / screenHeight)
        f.close()
    else:
        pageNum = 0
        bookLen = ceil(len(fullBook) / screenHeight)
 
epd = epd2in7.EPD() #264 by 174
h = epd.height
w = epd.width
epd.init()              # initialize the display
epd.Clear()             # clear the display

def pageNumCache():
    bookLen = ceil(len(fullBook) / screenHeight)
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
    font = ImageFont.truetype(FONT,30)
    fontPageNum = ImageFont.truetype(FONT,10)
    draw.text((indent(string,font,w), 2), string, font = font, fill = 0)
    draw.text((indent(book,fontPageNum,w),100),book,font=fontPageNum,fill=0)
    printMenuInterface(draw,fontPageNum)
    screenCleanup()
    epd.display(epd.getbuffer(HBlackImage))

def printToSplash(string):
    HBlackImage = Image.new('1', (w, h), 255)  # 264x174
    draw = ImageDraw.Draw(HBlackImage)
    font = ImageFont.truetype(FONT,30)
    fontPageNum = ImageFont.truetype(FONT,10)
    draw.text((indent(string,font,w), 100), string, font = font, fill = 0)
    screenCleanup()
    epd.display(epd.getbuffer(HBlackImage))

def printInterface(draw,font):
    draw.line((0,250,174,250),fill=0,width=1)
    draw.line((43,250,43,264),fill=0,width=1)
    draw.line((87,250,87,264),fill=0,width=1)
    draw.line((130,250,130,264),fill=0,width=1)
    draw.text((indent('Menu',font,w/4),250),'Menu',font=font,fill=0)
    draw.text((indent('Prev',font,w/4)+43,250),'Prev',font=font,fill=0)
    draw.text((indent('Next',font,w/4)+87,250),'Next',font=font,fill=0)
    draw.text((indent('Back',font,w/4)+130,250),'Back',font=font,fill=0)
    draw.text((indent(str(pageNum),font,w)+80, 235), str(pageNum), font = font, fill = 0)

def printMenuInterface(draw,font):
    draw.line((0,250,174,250),fill=0,width=1)
    draw.line((43,250,43,264),fill=0,width=1)
    draw.line((87,250,87,264),fill=0,width=1)
    draw.line((130,250,130,264),fill=0,width=1)
    draw.text((indent('Sel.',font,w/4),250),'Sel.',font=font,fill=0)
    draw.text((indent('Prev',font,w/4)+43,250),'Prev',font=font,fill=0)
    draw.text((indent('Next',font,w/4)+87,250),'Next',font=font,fill=0)
    draw.text((indent('Quit',font,w/4)+130,250),'Quit',font=font,fill=0)
    #draw.text((indent(str(pageNum),font,w)+80, 235), str(pageNum), font = font, fill = 0)

def lineOut():
    global fullBook
    global book
    fullBook = []
    bookRead = epub.read_epub(books_dir + book)
    font = ImageFont.truetype(FONT,30)
    fontPageNum = ImageFont.truetype(FONT,10)
    for html in bookRead.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(html.get_body_content(),'html5lib')
        htmlString = soup.get_text()
        htmlString = htmlString.replace("\t","").replace("\r","").replace("    "," ")##.replace("\n","")
        #htmlString = htmlString.replace("\n","")
        #htmlList = [htmlString[i:i+screenWidth] for i in range(0,len(htmlString),screenWidth)] 
        htmlList = textwrap.wrap(htmlString,width=screenWidth)
        x = 0
        for i in htmlList:
            fullBook.append(i)
            x+=1


def printPage(pageNum):
    HBlackImage = Image.new('1', (w, h), 255)  # 264x174
    draw = ImageDraw.Draw(HBlackImage)
    font = ImageFont.truetype(FONT,10) 
    for i in range(screenHeight):
        listIndex = (pageNum * screenHeight) + i
        if listIndex < len(fullBook):
            #print(fullBook[listIndex])
            #draw.text((indent(fullBook[listIndex],font,w),i*10),fullBook[listIndex],font=font,fill=0)
            draw.text((1,i*10),fullBook[listIndex],font=font,fill=0)
    printInterface(draw,font)
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
    global book
    global bookNum
    while True:
        if btn1.is_pressed:
            #book = bookNameList[bookNum]
            printToSplash('Loading')
            checkLastPage()
            lineOut()
            pageTurnLoop()
            #btn1.when_pressed = handleMenuBtn
        btn2.when_pressed = handleMenuBtn
        btn3.when_pressed = handleMenuBtn
        if btn4.is_pressed:
            btn4.when_pressed = handleMenuBtn
            sleep(3)
            raise Exception("Quit")
    #printToSplash('Loading')
    #lineOut()
    #printPage(pageNum)

def pageTurnLoop():
    printPage(pageNum)
    while True:
        #btn1.when_pressed = handleBtnPress
        btn2.when_pressed = handleBtnPress
        btn3.when_pressed = handleBtnPress
        if btn4.is_pressed:
            btn4.when_pressed = handleBtnPress
            sleep(1.5)
            break

try:
    checkLastRead()
    printToDisplay('Welcome!')
    menuLoop()
    #printToSplash('Loading')
    #lineOut()
    #printPage(pageNum)
    #while True:    
    #    btn1.when_pressed = handleBtnPress
    #    btn2.when_pressed = handleBtnPress
    #    btn3.when_pressed = handleBtnPress
    #    if btn4.is_pressed:
    #        btn4.when_pressed = handleBtnPress
    #        sleep(3)
    #        break

except IOError as e:
    print(e)
