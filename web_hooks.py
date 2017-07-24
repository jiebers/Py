#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
import json
import os
from datetime import datetime, timedelta
import logging
import logging.handlers
#import end

# configure log
LOG_FILE = "gitlab-receiver.log"
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=20 * 1024 * 1024, backupCount=10)
fmt = "%(asctime)s – %(message)s]"
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# config_json
app = Flask(__name__)
@app.route('/', methods=['POST'])
def index():
    path = '/srv/salt/scripts/deploy/'
    return _hooks(path, request.data)

def _hooks(path, data):
    post_data = json.loads(data)
    ref = post_data['ref']
    branch_name = ref.split('/')[-1]
    status = os.system("cd %s && git checkout %s && git pull" % (path, branch_name,))
    if status == 0:
        return 'success'
    else:
        return 'error'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9527, debug=True)