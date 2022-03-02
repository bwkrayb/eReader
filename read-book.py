from bs4 import BeautifulSoup
import ebooklib
import time
from ebooklib import epub

book = epub.read_epub('books/84.epub')

for html in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    #print(html.get_body_content())
    soup = BeautifulSoup(html.get_body_content(),'html5lib')
    #print(soup.prettify())
    #print(soup.get_text())
    print(html.get_id())
    print(html.is_chapter())
    print(html)
    contVar = input()
    if contVar == 'q':
        break

#htmlItems = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
#print(type(htmlItems))

#print(html(1))

#html.get_body_content()
