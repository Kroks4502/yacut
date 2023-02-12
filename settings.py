import os
import re
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')


URL_PATTERN = re.compile(
    '^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}'
    '\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$')
SHORT_URL_ALLOW_CHARACTERS = string.ascii_letters + string.digits
SHORT_URL_AUTO_GEN_LEN = 6
SHORT_URL_USER_MAX_LEN = 16
