import sys        
sys.path.insert(1, "./libs")             
from functions import indent
from libs.waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont 
import time                                      
from gpiozero import Button              
from bs4 import BeautifulSoup
import ebooklib
import time
from ebooklib import epub
import os.path
from os import path

btn1 = Button(5)
btn2 = Button(6)
btn3 = Button(13)
btn4 = Button(19) 
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
refreshCount = 0
screenWidth = 28
screenHeight = 23
books_dir='books/'
cache_dir='cache/'
book = epub.read_epub(books_dir + 'Harry-Potter-3.epub')
fullBook = []

if path.exists(cache_dir + 'Harry-Potter-3.cache'):
    f = open(cache_dir + 'Harry-Potter-3.cache')
    pageNumStr = f.read()
    pageNum = int(pageNumStr)
    f.close()
else:
    pageNum = 0

epd = epd2in7.EPD() #264 by 174
h = epd.height
w = epd.width
epd.init()              # initialize the display
epd.Clear()             # clear the display

def pageNumCache():
    f = open(cache_dir + 'Harry-Potter-3.cache','w')
    f.write(str(pageNum))
    f.close()

def printToDisplay(string):
    HBlackImage = Image.new('1', (w, h), 255)  # 264x174
    draw = ImageDraw.Draw(HBlackImage)
    font = ImageFont.truetype(FONT,30)
    fontPageNum = ImageFont.truetype(FONT,10)
    draw.text((indent(string,font,w), 2), string, font = font, fill = 0)
    printInterface(draw,fontPageNum)
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
    draw.text((indent('Exit',font,w/4)+130,250),'Exit',font=font,fill=0)
    draw.text((indent(str(pageNum),font,w)+80, 235), str(pageNum), font = font, fill = 0)


def lineOut():
    font = ImageFont.truetype(FONT,30)
    fontPageNum = ImageFont.truetype(FONT,10)
    for html in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(html.get_body_content(),'html5lib')
        htmlString = soup.get_text()
        htmlString = htmlString.replace("\t","").replace("\r","").replace("\n","").replace("    "," ")
        htmlList = [htmlString[i:i+screenWidth] for i in range(0,len(htmlString),screenWidth)] 
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
            draw.text((indent(fullBook[listIndex],font,w),i*10),fullBook[listIndex],font=font,fill=0)
    printInterface(draw,font)
    screenCleanup()
    epd.display(epd.getbuffer(HBlackImage))
    pageNumCache()

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
    if pageNum > 1:
        pageNum -=1
    
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
        printToSplash('Goodbye')

try:
    printToSplash('Loading')
    lineOut()
    printToDisplay('Welcome!')
    while True:    
        btn1.when_pressed = handleBtnPress
        btn2.when_pressed = handleBtnPress
        btn3.when_pressed = handleBtnPress
        if btn4.is_pressed:
            btn4.when_pressed = handleBtnPress
            time.sleep(3)
            break

except IOError as e:
    print(e)
