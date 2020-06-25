from pathlib import Path
from os import listdir
from os.path import join, sep, isfile, getctime, getsize
from datetime import datetime
from random import randint
import time, base64


def create_folder(pth):
    if pth:
        pth = str(pth)
        s = ''
        for i in pth.split(sep):
            s = join(s, i)
            try:
                Path(s).mkdir()
            except:
                pass


def get_formatted_datetime(format):
    return datetime.now().strftime(format)


def get_downloadzone_files(pth, sort='n', order='a'):
    pth = Path(pth)
    if not pth.exists():
        create_folder(pth)
        return [], None, None, None
    
    try:
        onlyfiles = [f for f in listdir(pth) if isfile(join(pth, f))]
    except:
        return [], None, None, None
    
    fl_list = []
    total_size = 0
    for a_file in onlyfiles:
        aa = {}
        aa_dir = join(pth, a_file)
        aa['name'] = a_file
        aa['date_modified_object'] = time.strptime(time.ctime(getctime(aa_dir)), '%a %b %d %H:%M:%S %Y')
        aa['size'] = getsize(aa_dir)
        fl_list.append(aa)
        
    reverse = False
    if order == 'd':
        reverse = True
    else:
        order == 'a'

    if sort == 'm':
        fl_list.sort(key=lambda x: x['date_modified_object'], reverse=reverse)
    elif sort == 's':
        fl_list.sort(key=lambda x: x['size'], reverse=reverse)
    else:
        sort = 'n'
        fl_list.sort(key=lambda x: x['name'], reverse=reverse)

    for a_fl in fl_list:
        total_size += a_fl['size']
        a_fl['date_modified'] = time.strftime("%d %b %Y %I:%M %p", a_fl['date_modified_object'])

    return fl_list, total_size, sort, order


def sizeSince(byte):
    byte = int(byte)
    if byte < 1024:
        return f'{byte} B'
    elif byte < 1024**2:
        byte = byte / (1024)
        s = " KB"
    elif byte < 1024**3:
        byte = byte / (1024**2)
        s = " MB"
    else:
        byte = byte / (1024**3)
        s = " GB"
    byte = "{0:.2f}".format(byte)
    return byte + s


def encode64(s):
    if s:
        try:
            return base64.encodebytes(str(s).encode()).decode()
        except:
            pass
    return None


def decode64(s):
    if s:
        try:
            return base64.decodebytes(str(s).encode()).decode()
        except:
            pass
    return None
