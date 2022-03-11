from bs4 import BeautifulSoup
import ebooklib
import time
from ebooklib import epub

#book = epub.read_epub('/home/pi/reader/books/Harry-Potter-1.epub')
book = epub.read_epub('/home/pi/reader/books/84.epub')
fullBook = []
screenHeight=23

for html in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    #print(html.get_body_content())
    soup = BeautifulSoup(html.get_body_content(),'html5lib')
    #print(soup.prettify())
    htmlString = soup.get_text()
    htmlString = htmlString.replace("\t","  ").replace("\r","  ").replace("\n","  ").replace("      "," ")
    #print(html.get_id())
    #print(html.is_chapter())
    #print(html)
    htmlList = [htmlString[i:i+28] for i in range(0,len(htmlString),28)]
#    x = 0
    for i in htmlList:
        fullBook.append(i)
#        x+=1

title = book.get_metadata('DC','title')[0][0]

print(title)

def printPage(pageNum):
    print("pageNum: " + str(pageNum))

    for i in range(screenHeight):
        listIndex = (pageNum * screenHeight) + i
        if listIndex < len(fullBook):
            print(fullBook[listIndex])

#printPage(0)
#printPage(1)
#printPage(2) # only has 2 lines
#printPage(5) # page doesn't exist, no lines
#printPage(50)
#printPage(51)
#printPage(52)


    #print(htmlList)
    #x = 0
    #for i in htmlList:
    #    print(i)
    #    x+=1
    #    if x % 20 == 0:
    #        nextInput = input()
    #        if nextInput == 'q':
    #            break
    #contVar = input()
    #if contVar == 'q':
    #    break

print(len(fullBook))

print(fullBook[20])

print(fullBook[1500])

print(type(fullBook))

#htmlItems = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
#print(type(htmlItems))

#print(html(1))

#html.get_body_content()
