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
from urllib.parse import urlparse
from urllib.parse import parse_qs

# Main
# Get input args
if needHelp(False) == True:
    exit() 
status, fromLanguage = getArgumentValue("-f", "--from")
if status == False:
    print('Language of source document not passed')
    needHelp(True)
    exit()

status, toLanguagesString = getArgumentValue("-t", "--to")
if status == False:
    print('Language(s) to translate to, not passed')
    needHelp(True)
    exit()
# The prefix for all documents/files in the Bolb Storage container
# that will be translated
# For example, to translate all docs starting with 'jan-2021-demo'
status, docsPrefix = getArgumentValue("-p", "--prefix")
if status == False:
    print('No document prefix found')
    needHelp(True)
    exit()
# The suffix of the docs to translate. Example to translate all
# pdf docs in the container, pass 'pdf' as suffix
status, docsSuffix = getArgumentValue("-s", "--suffix")
if status == False:
    print('No document suffix found')
    needHelp(True)
    exit()

#toLanguages = ['de', 'it']
#for aLang in toLanguagesString:
#    print(aLang)
#    toLanguages.append(aLang)
response = translateDocsInContainer(fromLanguage, toLanguagesString, docsPrefix, docsSuffix)
print(f'response status code: {response.status_code}\nresponse status: {response.reason}\nresponse headers: {response.headers}')
if (response.status_code == 202 and response.reason == 'Accepted'):
    operationLocation = urlparse(response.headers['Operation-Location'])
    jobId = operationLocation.path.rsplit('/', 1)[-1]    
    print("Job Id: %s" %(jobId))
