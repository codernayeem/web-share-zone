DEBUG_MODE = True

WSZ_VERSION = '1.1'
MAX_CONTENT_LENGTH_IN_MB = 560
UPLOAD_ZONE_PATH = 'UPLOADZONE'
DOWNLOAD_ZONE_PATH = 'DOWNLOADZONE'
SHAREZONE_ZONE_PATH = 'SHAREZONE'
CAN_SIGNUP = True
NEED_AUTH_FOR_DOWNLOAD_ZONE = False
NEED_AUTH_FOR_UPLOAD_ZONE = False
DEFAULT_PORT = 1999

VIDEO_EXTENSION = ['mp4', '3gp', 'avi', 'mkv', 'ogg', 'webm']
AUDIO_EXTENSION = ['mp3', 'amr', 'm4a', 'acc']
PICTURE_EXTENSION = ['png', 'jpg', 'ico', 'jpeg', 'gif', 'webp']
TEXT_EXTENSION = ['txt', 'log', 'py', 'html', 'js', 'jsx', 'css', 'c', 'cpp', 'java', 'xml', 'json', 'cs', 'md']


file_type_icon = {
    'picture' : 'file_icon_image.png',
    'video': 'file_icon_video.png',
    'audio': 'file_icon_audio.png',
    'text' : 'file_icon_text.png',
    'default' : 'file_icon.png',
    
    'zip': 'file_icon_zip.png',
    'rar': 'file_icon_zip.png',
    'iso': 'file_icon_zip.png',
    '7z' : 'file_icon_zip.png',

    'db'     : 'file_icon_db.png',
    'sqlite' : 'file_icon_db.png',
    'sqlite3': 'file_icon_db.png',

    'doc' : 'file_icon_office.png',
    'docx': 'file_icon_word.png',
    'xlsx': 'file_icon_office.png',

    'qt' : 'file_icon_qt.png',
    'ai' : 'file_icon_ai.png',
    'apk': 'file_icon_apk.png',
    'pdf': 'file_icon_pdf.png',
    'exe': 'file_icon_exe.png',
    }

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + 'database.db'
    SECRET_KEY = 'ABC_123_CBA_321'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH_IN_MB * 1024 * 1024
