import sys                     # import sys
sys.path.insert(1, "./libs")             
from functions import indent
from libs.waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont 
import time                                      
from gpiozero import Button              

btn1 = Button(5)
btn2 = Button(6)
btn3 = Button(13)
btn4 = Button(19) 
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
pageNum = 1

epd = epd2in7.EPD() #264 by 174
h = epd.height
w = epd.width
epd.init()              # initialize the display
epd.Clear()             # clear the display

#print('h:'+str(h)+' w:'+str(w))

def printToDisplay(string):
    HBlackImage = Image.new('1', (w, h), 255)  # 298*126
    draw = ImageDraw.Draw(HBlackImage)
    font = ImageFont.truetype(FONT, 30)
    draw.text((25, 65), string, font = font, fill = 0)
    epd.display(epd.getbuffer(HBlackImage))

def nextPage():
    global pageNum
    pageNum +=1

def prevPage():
    global pageNum
    pageNum -=1
    
def handleBtnPress(btn):
    if btn.pin.number == 5:
        printToDisplay('Button1')
    if btn.pin.number == 6:
        prevPage()
        printToDisplay('Pg:'+str(pageNum))
    if btn.pin.number == 13:
        nextPage()
        printToDisplay('Pg:'+str(pageNum)) 
    if btn.pin.number == 19:
        printToDisplay('Goodbye')

 
    # python hack for a switch statement. The number represents the pin number and
    # the value is the message we will print
    #switcher = {
    #    5: "Hello, World!",
    #    6: "This is my first \nRPi project.",
    #    13: "Hope you liked it.",
    #    19: "Goodbye"
    #}
    # get the string based on the passed in button and send it to printToDisplay()
    #msg = switcher.get(btn.pin.number, "Error")
    #printToDisplay(msg)


try:
    while True:    
        btn1.when_pressed = handleBtnPress
        btn2.when_pressed = handleBtnPress
        btn3.when_pressed = handleBtnPress
        if btn4.is_pressed:
            btn4.when_pressed = handleBtnPress
            time.sleep(5)
            break

except IOError as e:
    print(e)
