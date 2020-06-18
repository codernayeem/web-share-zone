from pathlib import Path
from os import listdir
from os.path import join
from datetime import datetime
from random import randint


class ShareZone(object):
    def __init__(self):
        self.sharedFiles = []
        self.config = {}

    def upload(self, user_id, file_id, file_name, file_path, file_link, hidden, password):
        new_file = {}
        new_file['user_id'] = user_id
        new_file['file_id'] = file_id
        new_file['file_name'] = file_name
        new_file['file_path'] = file_path
        new_file['file_link'] = file_link
        new_file['hidden'] = hidden
        new_file['password'] = password
        new_file['datetime'] = datetime.now()

        self.sharedFiles.append(new_file)

    def check_file_id(self, file_id):
        for i in self.sharedFiles:
            if i['file_id'] == file_id:
                return True
        return False

    def generate_new_file_id(self):
        i = randint(100000, 999999)
        while self.check_file_id(i):
            i += 1
        return i

    def get_sharred_file(self, file_id):
        for i in self.sharedFiles:
            if i['file_id'] == file_id:
                return i
        return None
