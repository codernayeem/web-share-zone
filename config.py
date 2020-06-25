DEBUG_MODE = True

WSZ_VERSION = '1.0'
MAX_CONTENT_LENGTH_IN_MB = 560
UPLOAD_ZONE_PATH = 'UPLOADZONE'
DOWNLOAD_ZONE_PATH = 'DOWNLOADZONE'
SHAREZONE_ZONE_PATH = 'SHAREZONE'
CAN_SIGNUP = True

file_type_icon = {
    '.png' : 'file_icon_image.png',
    '.jpg' : 'file_icon_image.png',
    '.ico' : 'file_icon_image.png',
    '.jpeg': 'file_icon_image.png',
    '.gif' : 'file_icon_image.png',
    '.webp': 'file_icon_image.png',

    '.mp4': 'file_icon_video.png',
    '.3gp': 'file_icon_video.png',
    '.avi': 'file_icon_video.png',
    '.mkv': 'file_icon_video.png',
    '.ogg': 'file_icon_video.png',
    '.webm': 'file_icon_video.png',
    '.mpeg': 'file_icon_video.png',

    '.mp3': 'file_icon_audio.png',
    '.amr': 'file_icon_audio.png',
    '.m4a': 'file_icon_audio.png',
    '.acc': 'file_icon_audio.png',

    '.zip': 'file_icon_zip.png',
    '.rar': 'file_icon_zip.png',
    '.iso': 'file_icon_zip.png',
    '.7z' : 'file_icon_zip.png',

    '.txt' : 'file_icon_text.png',
    '.log' : 'file_icon_text.png',
    '.html': 'file_icon_text.png',
    '.css' : 'file_icon_text.png',
	'.cs'  : 'file_icon_text.png',
    '.py'  : 'file_icon_text.png',
    '.c'   : 'file_icon_text.png',
    '.cpp' : 'file_icon_text.png',
    '.java': 'file_icon_text.png',
    '.js'  : 'file_icon_text.png',
    '.xml' : 'file_icon_text.png',

    '.db'     : 'file_icon_db.png',
    '.sqlite' : 'file_icon_db.png',
    '.sqlite3': 'file_icon_db.png',

    '.doc' : 'file_icon_office.png',
    '.docx': 'file_icon_word.png',
    '.xlsx': 'file_icon_office.png',

    '.qt' : 'file_icon_qt.png',
    '.ai' : 'file_icon_ai.png',
    '.apk': 'file_icon_apk.png',
    '.pdf': 'file_icon_pdf.png',
    '.exe': 'file_icon_exe.png',
    }
default_file_icon = 'file_icon.png'

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + 'database.db'
    SECRET_KEY = 'ABC_123_CBA_321'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH_IN_MB * 1024 * 1024
