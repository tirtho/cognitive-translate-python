import logging

import azure.functions as func
import requests, json
from urllib.parse import urlparse
import os

def main(myblob: func.InputStream):
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

    # Languages
    fromLanguage = 'en'
    toGermanLanguage = 'de'
    toSpanishLanguage = 'es'

    srcFile = str(blobStoreName) + str(inputFilename) + str(sourceKey)

    # Translate to Spanish
    targetFileSpanish = str(blobStoreName) + str(targetContainerName) + str('/') + str(inputFilename.split('/',2)[1]) + \
                    str('-spanish') + str('/') + str(inputFilename.split('/',2)[2]) + str(targetKey)
    targetGlossaryFileSpanish = targetGlossaryUri + str('/glossary-') + toSpanishLanguage + str('.tsv') + targetGlossaryKey

    # Translate to German
    targetFileGerman = str(blobStoreName) + str(targetContainerName) + str('/') + str(inputFilename.split('/',2)[1]) + \
                    str('-german') + str('/') + str(inputFilename.split('/',2)[2]) + str(targetKey)
    targetGlossaryFileGerman = targetGlossaryUri + str('/glossary-') + toGermanLanguage + str('.tsv') + targetGlossaryKey

    payloadWithPrefixAndSuffix = {
        "inputs": [
            {
                "storageType": "File",
                "source": {
                    "sourceUrl": srcFile,
                    "storageSource": "AzureBlob",
                    "language": fromLanguage,
                },
                "targets": [
                    {
                        "targetUrl": targetFileSpanish,
                        "storageSource": "AzureBlob",
                        "category": "general",
                        "language": toSpanishLanguage,
                        "glossaries": [
                            {
                                "glossaryUrl": targetGlossaryFileSpanish,
                                "format": "TSV"
                            }
                        ]
                    },
                    {
                        "targetUrl": targetFileGerman,
                        "storageSource": "AzureBlob",
                        "category": "general",
                        "language": toGermanLanguage,
                        "glossaries": [
                            {
                                "glossaryUrl": targetGlossaryFileGerman,
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
