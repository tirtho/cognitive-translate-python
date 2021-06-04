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
status, textToTranslate = getArgumentValue("-q", "--query")
if status == False:
    print('Text to translate not found')
    needHelp(True)
    exit()
status, fromLanguage = getArgumentValue("-f", "--from")
if status == False:
    print('Language of text not passed, detecting it now...')
    response = detectLanguage(textToTranslate)
    fromLanguage, s = whatIsTheLanguage(response)
    print('Detected language of text as %s, with a confidence of %.2f' %(fromLanguage, s))

status, toLanguagesString = getArgumentValue("-t", "--to")
if status == False:
    print('Language(s) to translate to, not found')
    needHelp(True)
    exit()

#toLanguages = ['de', 'it']
#for aLang in toLanguagesString:
#    print(aLang)
#    toLanguages.append(aLang)
response = translateText(fromLanguage, toLanguagesString, textToTranslate)

# If you encounter any issues with the base_url or path, make sure
# that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-detect

print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': ')))
