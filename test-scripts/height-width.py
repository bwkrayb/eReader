from PIL import Image,ImageDraw,ImageFont 
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
font = ImageFont.truetype(FONT,15)


w = 174
h = 264
pixelWidth = w
pixelHeight = h - 30
screenWidthChar = 0
screenHeightChar = 0

def getCharScrSz(w,h):
    global screenWidthChar
    global screenHeightChar
    charStr=''
    while font.getsize(charStr)[0] < w:
        charStr += 'a'
    screenWidthChar = len(charStr)
    screenHeightChar = h / font.getsize(charStr)[1]


getCharScrSz(pixelWidth,pixelHeight)

print(screenWidthChar)
print(screenHeightChar)
