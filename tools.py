from pathlib import Path
from os import listdir
from os.path import join, sep
from datetime import datetime
from random import randint


def create_folder(pth):
    s = ''
    for i in pth.split(sep):
        s = join(s, i)
        try:
            Path(s).mkdir()
        except:
            pass


def get_formatted_datetime(format):
    return datetime.now().strftime(format)
