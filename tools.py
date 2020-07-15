from pathlib import Path
from os import listdir
from os.path import join, sep, isfile, getctime, getsize
from datetime import datetime
from random import randint
import time, base64, config as cfg


def get_icon(extension, file_type=None):
    icon = cfg.file_type_icon.get(file_type)
    if not icon:
        icon = cfg.file_type_icon.get(extension)
    if icon:
        return icon
    return cfg.file_type_icon['default']


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


def get_filename_extension(filename):
    if '.' not in filename:
        return filename, ''
    ext = filename.split('.')[-1]
    if '.' + ext == filename:
        return filename, ''
    return filename[:-(len('.'+ext))], ext


def get_filetype(extension):
    if extension:
        extension = extension.lower()
        if extension in cfg.VIDEO_EXTENSION:
            return 'video'
        elif extension in cfg.AUDIO_EXTENSION:
            return 'audio'
        elif extension in cfg.PICTURE_EXTENSION:
            return 'picture'
        elif extension in cfg.TEXT_EXTENSION:
            return 'text'
    
    return ''


def get_file_content(pth):
    try:
        return open(pth, 'r').read()
    except:
        return None


def is_valid_file(fl):
    if fl:
        p = Path(fl)
        return p.exists() and p.is_file()
    return False


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
        data = {}
        data_dir = join(pth, a_file)
        data['name'] = a_file
        data['date_modified_object'] = time.strptime(time.ctime(getctime(data_dir)), '%a %b %d %H:%M:%S %Y')
        data['size'] = getsize(data_dir)
        data['extension'] = get_filename_extension(data['name'])[1]
        data['file_type'] = get_filetype(data['extension'])

        fl_list.append(data)
        
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


def get_downloadzone_single_file(pth, filename):
    pth = Path(pth)
    if not pth.exists():
        create_folder(pth)

    elif filename and is_valid_file(join(pth, filename)):
        data_dir = join(pth, filename)
        data = {}
        data['name'] = filename
        data['date_modified_object'] = time.strptime(time.ctime(getctime(data_dir)), '%a %b %d %H:%M:%S %Y')
        data['date_modified'] = time.strftime("%d %b %Y %I:%M %p", data['date_modified_object'])
        data['size'] = getsize(data_dir)
        data['extension'] = get_filename_extension(data['name'])[1]
        data['file_type'] = get_filetype(data['extension'])
        if data['file_type'] == 'text':
            data['content'] = get_file_content(data_dir)
        return data
        
    return {'error': 'File not found', 'name': filename}


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
