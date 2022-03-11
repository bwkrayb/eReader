# eReader Time! #

### The Project ###
This is my project for creating a Python powered eReader using a Raspberry Pi Zero V2 connected to a 2.7 inch Waveshare eInk display. I use the ebooklib to process through epub files, Beautiful Soup to process the HTML that is taken out of the epub, and then the Waveshare drivers to output the book page to the display.
I added an entry to crontab that calls bin/start.sh on boot, so the eReader software starts when the Pi is plugged into a power source. I'm planning on adding a battery at some point. Will look into pressing and holding the exit button to safely shutdown the Pi, at which point you power off the battery.

### Reading ###
* When the software starts, you begin in the book select menu. 
* The book displayed on boot is the last book you read. 
* Select this book by pressing the Sel. button. 
* To change books left or right in the list, press the Prev or Next buttons. 
* Press the Exit button to exit out of the program. 
* When you select a book, you will start reading at the last place you read. 
* Once in the book, press the Prev or Next buttons to flip the pages, and the Back button to return to the book select page. 

#### ChangeLog ####
* Also on 3/11, changed the main menu to use the book title and not the book epub file name.
* On 3/11, added function to make the page width and height dynamic based on font and font size. This can make the pages a little wonky and will mess up the last page you read, but this sets up the future for getting this working on larger screens (that have partial refresh so the page turns could be potentially quicker).
* On 3/6, merged HcNguyen111's suggested changes to optimize the book loading function and for better variable/function names.
* On 3/4, implemented the main menu function to allow for book selection.

