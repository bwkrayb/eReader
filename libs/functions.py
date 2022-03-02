import datetime
import os
import PIL
import time
import logging
import requests
import re
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

data_dir='/home/pi/eink2in7/data/'

logging.basicConfig(level=logging.INFO,filename='/home/pi/eink2in7/logs/eink.log')



def paste(image: Image, position: tuple = (0, 0)) -> None:
    """
    Paste an image onto the buffer
    :param image: Image to paste
    :param position: tuple position to paste at
    :return: None
    """
    image.paste(image, position)


def indent(input,font,width):
    return int((width - font.getsize(input)[0]) / 2)





