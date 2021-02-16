import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "b'\xe5\xd1\x81\x9e\x95\xfd\x8a\xf8h\xed\x95\xe9>-\\\x87"