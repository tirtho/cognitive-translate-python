# -*- coding: utf-8 -*-

# This simple app uses the '/detect' resource to identify the language of
# the provided text or texts.

# This sample runs on Python 2.7.x and Python 3.x.
# You may need to install requests and uuid.
# Run: pip install requests uuid

import environment as env
import os, requests, uuid, json
from utils import *
from TranslationFunctions import *

# Main
# Get input args
if needHelp(False) == True:
    exit() 
status, jobId = getArgumentValue("-j", "--jobId")
if status == False:
    print('JobId not passed')
    needHelp(True)
    exit()
getJobStatus(jobId)

print("### Documents Status ###")
getDocumentsStatus(jobId)
