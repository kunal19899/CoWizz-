#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/demosite/Covid19/v2/")

from v3 import app as application
application.secret_key = "b'\xe5\xd1\x81\x9e\x95\xfd\x8a\xf8h\xed\x95\xe9>-\\\x87"
