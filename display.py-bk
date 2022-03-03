import sys                     # import sys
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


btn1 = Button(5)
btn2 = Button(6)
btn3 = Button(13)
btn4 = Button(19) 
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
pageNum = 1
refreshCount = 0
screenWidth = 28
screenHeight = 23
book = epub.read_epub('books/Harry-Potter-1.epub')


epd = epd2in7.EPD() #264 by 174
h = epd.height
w = epd.width
epd.init()              # initialize the display
epd.Clear()             # clear the display

#print('h:'+str(h)+' w:'+str(w))

def printToDisplay(string):
    HBlackImage = Image.new('1', (w, h), 255)  # 264x174
    draw = ImageDraw.Draw(HBlackImage)
    font = ImageFont.truetype(FONT,30)
    fontPageNum = ImageFont.truetype(FONT,10)
    draw.text((indent(string,font,w), 2), string, font = font, fill = 0)
    printInterface(draw,fontPageNum)
    #lines = ["1234567890123456789012345678", "banana", "cherry","four","five","six","seven","eight","nine","ten","","","","","","","","","","twenty"]
    #lineOut(draw,fontPageNum,HBlackImage)
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


#def lineOut(draw,font,lines):
#    h=10
#    for i in lines:
#        draw.text((indent(i,font,w),20+h),i,font=font,fill=0)
#        h+=10

def lineOut():
    HBlackImage = Image.new('1', (w, h), 255)  # 264x174
    draw = ImageDraw.Draw(HBlackImage)
    font = ImageFont.truetype(FONT,30)
    fontPageNum = ImageFont.truetype(FONT,10)
    printInterface(draw,fontPageNum)
    for html in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(html.get_body_content(),'html5lib')
        htmlString = soup.get_text()
        htmlString = htmlString.replace("\t","").replace("\r","").replace("\n","").replace("    "," ")
        htmlList = [htmlString[i:i+screenWidth] for i in range(0,len(htmlString),screenWidth)] 
        x = 0
        n = 0
        for i in htmlList:
            draw = ImageDraw.Draw(HBlackImage)
            printInterface(draw,fontPageNum)
            draw.text((indent(i,fontPageNum,w),n),i,font=fontPageNum,fill=0)
            n+=10
            x+=1
            if x % screenHeight == 0:
                epd.display(epd.getbuffer(HBlackImage))
                time.sleep(.2)
                HBlackImage = Image.new('1', (w, h), 255) 
                while True:
                    if btn3.is_pressed:
                        screenCleanup()
                        nextPage()
                        break
                    if btn4.is_pressed:
                        printToDisplay('Goodbye')
                        raise Exception("Quit")
                n=0
                x=0


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
        lineOut()
    if btn.pin.number == 6:
        prevPage()
        printToDisplay('Page '+str(pageNum))
#    if btn.pin.number == 13:
#        nextPage()
#        printToDisplay('Page '+str(pageNum)) 
    if btn.pin.number == 19:
        printToDisplay('Goodbye')


try:
    printToDisplay('Welcome!')
    time.sleep(2)
    lineOut()
#    while True:    
#        btn1.when_pressed = handleBtnPress
##        btn2.when_pressed = handleBtnPress
##        btn3.when_pressed = handleBtnPress
#        if btn4.is_pressed:
#            btn4.when_pressed = handleBtnPress
#            time.sleep(5)
#            break

except IOError as e:
    print(e)
