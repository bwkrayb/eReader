from bs4 import BeautifulSoup
import ebooklib
import time
from ebooklib import epub

book = epub.read_epub('books/84.epub')

for html in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    #print(html.get_body_content())
    soup = BeautifulSoup(html.get_body_content(),'html5lib')
    #print(soup.prettify())
    htmlString = soup.get_text()
    htmlString = htmlString.replace("\t","  ").replace("\r","  ").replace("\n","  ").replace("      "," ")
    #print(html.get_id())
    #print(html.is_chapter())
    print(html)
    htmlList = [htmlString[i:i+28] for i in range(0,len(htmlString),28)]
    #print(htmlList)
    x = 0
    for i in htmlList:
        print(i)
        x+=1
        if x % 20 == 0:
            nextInput = input()
            if nextInput == 'q':
                break
    contVar = input()
    if contVar == 'q':
        break

#htmlItems = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
#print(type(htmlItems))

#print(html(1))

#html.get_body_content()
