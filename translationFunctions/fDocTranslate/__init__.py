import logging

import azure.functions as func
import requests, json
from urllib.parse import urlparse
import os

from requests.api import request

def main(myblob: func.InputStream, mydoc: func.Out[func.Document]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
   
    inputFilename = str(f"{myblob.name}")

    # Blob Storage details
    
    blobStoreName = os.environ['DOCS_CONTAINER_HOST']
    sourceKey = os.environ['DOCS_CONTAINER_SOURCE_KEY']
    targetContainerName = os.environ['DOCS_TARGET_CONTAINER_NAME']
    targetKey = os.environ['DOCS_CONTAINER_TARGET_KEY']
    targetGlossaryKey = os.environ['GLOSSARY_CONTAINER_KEY']
    targetGlossaryUri = os.environ['GLOSSARY_URI']
    
    # Azure Document Translator details
    constructed_url = os.environ['TRANSLATOR_DOCS_ENDPOINT'] + '/batches'
    subscription_key = os.environ['TRANSLATOR_DOCS_SUBSCRIPTION_KEY']

    toLanguage = os.environ['TRANSLATE_TO']
    # TODO: Find out from language using a Congnitive Services call
    fromLanguage = 'en'

    srcFile = str(blobStoreName) + str(inputFilename) + str(sourceKey)

    # Translate to Spanish
    targetFilePath = str(targetContainerName) + str('/') + str(fromLanguage) + \
                    str('-') + str(toLanguage) + str('/') + str(inputFilename.split('/',2)[2])
    targetFile = str(blobStoreName) + str(targetFilePath) + str(targetKey)
    targetGlossaryFile = targetGlossaryUri + str('/glossary-') + toLanguage + str('.tsv') + targetGlossaryKey

    # Translate to German
#    targetFilePathGerman = str(targetContainerName) + str('/') + str(inputFilename.split('/',2)[1]) + \
#                    str('-german') + str('/') + str(inputFilename.split('/',2)[2])
#    targetFileGerman = str(blobStoreName) + targetFilePathGerman + str(targetKey)
#    targetGlossaryFileGerman = targetGlossaryUri + str('/glossary-') + toGermanLanguage + str('.tsv') + targetGlossaryKey

    # Using auto detect for source document language
    payloadWithPrefixAndSuffix = {
        "inputs": [
            {
                "storageType": "File",
                "source": {
                    "sourceUrl": srcFile,
                    "storageSource": "AzureBlob"
                },
                "targets": [
                    {
                        "targetUrl": targetFile,
                        "storageSource": "AzureBlob",
                        "category": "general",
                        "language": toLanguage,
                        "glossaries": [
                            {
                                "glossaryUrl": targetGlossaryFile,
                                "format": "TSV"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
    }

    logging.info(f"Payload: {payloadWithPrefixAndSuffix}")
    logging.info(f"Headers: {headers}")
    logging.info(f"Translator URL: {constructed_url}")
    response = requests.post(constructed_url, headers=headers, json=payloadWithPrefixAndSuffix)
    logging.info(f'Azure Document Translator response status code: {response.status_code}\nresponse status: {response.reason}\nresponse headers: {response.headers}')
    if (response.status_code == 202 and response.reason == 'Accepted'):
        operationLocation = urlparse(response.headers['Operation-Location'])
        jobId = operationLocation.path.rsplit('/', 1)[-1]
        logging.info(f"Job Id: {jobId}")
        dateStamp = response.headers['Date']
        requestId = response.headers['X-RequestId']
        payload = json.dumps(payloadWithPrefixAndSuffix)
        cosmosDBTranslationJob = {
            "jobId": jobId,
            "createDate": dateStamp,
            "requestId": requestId,
            "jobStatus": "accepted",
            "sourceFilePath": inputFilename,
            "targetFilePath": targetFilePath,
            "sourceUrl": srcFile,
            "targetUrl": targetFile,
            "translatedFrom": fromLanguage,
            "translatedTo": toLanguage,
            "documentId": ""
        }
        #print("Writing to CsomosDB ==> %s" %(json.dumps(cosmosDBTranslationJob)) )
        mydoc.set(func.Document.from_json(json.dumps(cosmosDBTranslationJob)))
        #return 'OK'
