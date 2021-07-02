# -*- coding: utf-8 -*-

# This simple app uses the '/detect' resource to identify the language of
# the provided text or texts.

# This sample runs on Python 2.7.x and Python 3.x.
# You may need to install requests and uuid.
# Run: pip install requests uuid

import environment as env
import os, requests, uuid, json
from utils import *
import http.client

def detectLanguage(thisText):
    # Get input args

    # If you encounter any issues with the base_url or path, make sure
    # that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-detect
    path = '/detect?api-version=3.0'
    constructed_url = env.getEndpoint() + path

    headers = env.getRequestHeader()

    # You can pass more than one object in body.
    body = [{
        'text': thisText
    }]
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()

def whatIsTheLanguage(response):
    l = ''
    s = 0.00
    for aLanguage in response:
        thisL = aLanguage['language']
        thisScore = aLanguage['score']
        if (thisScore > s):
            s = thisScore
            l = thisL
    return l, s

# from is a string, to is an array of strings of multiuple languages
# text is the text to translate
def translateText(fromLanguage, toLanguagesString, textToTranslate):
    path = '/translate'
    constructed_url = env.getEndpoint() + path
    headers = env.getRequestHeader()

    toLanguages = map(str.strip, toLanguagesString.split(','))
    params = {
        'api-version': '3.0',
        'from': fromLanguage,
        'to': toLanguages
    }

    # You can pass more than one object in body.
    body = [{
        'text': textToTranslate
    }]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    return request.json()

def translateDocsInContainer(fromLanguage, toLanguagesString, docsPrefix, docsSuffix):
    path = '/batches'
    constructed_url = env.getDocumentTranslatorEndpoint() + path
    toLanguages = map(str.strip, toLanguagesString.split(','))
    # TODO: Loop through languages to support multiple target languages
    # For now just pick the first language in the array
    toLanguage = list(toLanguages)[0]
    payloadWithPrefixAndSuffix = {
        "inputs": [
            {
                "source": {
                    "sourceUrl": env.getDocumentTranslatorSourceUrl(),
                    "storageSource": "AzureBlob",
                    "language": fromLanguage,
                    "filter":{
                        "prefix": docsPrefix + '/',
                        "suffix": docsSuffix
                    }
                },
                "targets": [
                    {
                        "targetUrl": env.getDocumentTranslatorTargetUrl(),
                        "storageSource": "AzureBlob",
                        "category": "general",
                        "language": toLanguage
                    }
                ]
            }
        ]
    }
    headers = env.getRequestHeaderForDocumentTranslation()
    #print("URL: %s\nHeaders: %s\nPayload: %s\n" %(constructed_url, headers, payloadWithPrefixAndSuffix))
    return requests.post(constructed_url, headers=headers, json=payloadWithPrefixAndSuffix)

def getJobStatus(jobId):

    host = env.getDocumentTranslatorHost()
    parameters = '//translator/text/batch/v1.0/batches/' + jobId
    subscriptionKey =  env.getDocumentTranslatorKey()
    conn = http.client.HTTPSConnection(host)
    payload = ''
    headers = {
    'Ocp-Apim-Subscription-Key': subscriptionKey
    }
    conn.request("GET", parameters , payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(res.status)
    print()
    print(data.decode("utf-8"))

def getDocumentsStatus(jobId):

    host = env.getDocumentTranslatorHost()
    parameters = '//translator/text/batch/v1.0/batches/' + jobId + '/documents/'
    subscriptionKey =  env.getDocumentTranslatorKey()
    conn = http.client.HTTPSConnection(host)
    payload = ''
    headers = {
    'Ocp-Apim-Subscription-Key': subscriptionKey
    }
    conn.request("GET", parameters , payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(res.status)
    print()
    print(data.decode("utf-8"))

def getDocumentStatus(jobId, docId):

    host = env.getDocumentTranslatorHost()
    parameters = '//translator/text/batch/v1.0/' + jobId + '/document/' + docId
    subscriptionKey =  env.getDocumentTranslatorKey()
    conn = http.client.HTTPSConnection(host)
    payload = ''
    headers = {
    'Ocp-Apim-Subscription-Key': subscriptionKey
    }
    conn.request("GET", parameters , payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(res.status)
    print()
    print(data.decode("utf-8"))    
