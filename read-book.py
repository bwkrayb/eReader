import ebooklib
import time
from ebooklib import epub

book = epub.read_epub('books/84.epub')

for html in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    print(html.get_body_content())
    input()

htmlItems = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
print(type(htmlItems))

#print(html(1))

#html.get_body_content()
