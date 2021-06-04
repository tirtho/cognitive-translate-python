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
if needHelp(False) == True:
    exit() 
status, textToDetectLanguage = getArgumentValue("-q", "--query")
if status == False:
    needHelp(True)
    exit()

languageResponse = detectLanguage(textToDetectLanguage)

l, s = whatIsTheLanguage(languageResponse)
print('The language is %s, with a confidence of %.2f' %(l, s))

print('All possible languages detected are')
for aLanguage in languageResponse:
    print('\t%s, confidence %.2f' %(aLanguage['language'], aLanguage['score']))
print("Detailed JSON Response:")
print(json.dumps(languageResponse, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': ')))
