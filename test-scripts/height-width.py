from PIL import Image,ImageDraw,ImageFont 
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
font = ImageFont.truetype(FONT,14)


w = 174
h = 264
screenWidthChar = 0
screenHeightChar = 0


def getCharScrSz():
    global screenWidthChar
    global screenHeightChar
    global lineHeight
    charStr=''
    while font.getsize(charStr)[0] < (w-4):
        charStr += 'a'
    screenWidthChar = len(charStr)
    screenHeightChar = round((h-30) / font.getsize(charStr)[1])
    lineHeight = font.getsize(charStr)[1]

getCharScrSz()

print(screenWidthChar)
print(screenHeightChar)
print(lineHeight)
