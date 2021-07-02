import logging

import azure.functions as func
import requests, json
from urllib.parse import urlparse
import os
import re

from requests.api import request

from azure.cosmos import CosmosClient

def main(myblob: func.InputStream, 
        #myinputdocs: func.DocumentList, 
        myoutputdoc: func.Out[func.Document]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    inputFilename = str(f"{myblob.name}")

    # Get the Cosmos DB endpoint, connect and get the document
    # This is done instead of via input binding of Cosmos DB is 
    # because in the input binding we could not pass the
    # targetFilePath parameter from the blob trigger (in function.json)
    cosmosDBConnectionStr = os.environ['theCosmosDB_DOCUMENTDB']
    splitPattern = "AccountEndpoint=(.*?);AccountKey="
    cosmosDBUri = re.search(splitPattern, cosmosDBConnectionStr).group(1)
    splitPattern = "AccountKey=(.*?);"
    cosmosDBKey = re.search(splitPattern, cosmosDBConnectionStr).group(1)

    cosmosClient = CosmosClient(cosmosDBUri, credential=cosmosDBKey)
    cosmosDB = cosmosClient.get_database_client(os.environ['cosmosDatabaseName'])
    cosmosContainer = cosmosDB.get_container_client(os.environ['cosmosCollectionName'])

    subscription_key = os.environ['TRANSLATOR_DOCS_SUBSCRIPTION_KEY']
    queryResults = cosmosContainer.query_items(query = 'SELECT * FROM C WHERE C.targetFilePath = @filePath',
                                                parameters=[
                                                    dict(name='@filePath', value = str(inputFilename))
                                                ],
                                                enable_cross_partition_query=True
                                            )
    for translationJob in queryResults:
        # Get the document Id
        # Make the cognitive Service call to get document status
        # update the document status in json 
        # write back to cosmosdb
        translationJobJson = json.dumps(translationJob)
        logging.info(f"For 'targetFilePath' as {inputFilename}, CosmosDB document found: {translationJobJson}")
        jobId = translationJob['jobId']
        constructed_url = os.environ['TRANSLATOR_DOCS_ENDPOINT'] + '/batches/' + jobId + '/documents'
        headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        }
        response = requests.get(constructed_url, headers=headers)
        logging.info(f'From Cognitive Document Translation Service, got job [id = {jobId}] status. Response status code: {response.status_code}\nresponse status: {response.reason}\nresponse headers: {response.headers}')
        
        if (response.status_code == 200):
            # Assuming there is only one target document for a given job
            # i.e. we are translating a source document to only one target language
            responseJson = response.json()
            translationJob['documentId'] = responseJson['value'][0]['id']
            translationJob['translatedTo'] = responseJson['value'][0]['to']
            translationJob['translationStartedAtUTC'] = responseJson['value'][0]['createdDateTimeUtc']
            translationJob['translationStatus'] = responseJson['value'][0]['status']
            translationJob['translationLastActionDateUTC'] = responseJson['value'][0]['lastActionDateTimeUtc']
            translationJob['translationProgress'] = responseJson['value'][0]['progress']
            translationJob['characterCharged'] = responseJson['value'][0]['characterCharged']

            # Update the TranslationJob record in cosmos db
            logging.info(f'Updated TranslationJob recordin Cosmos DB: {translationJob}')
            myoutputdoc.set(func.Document.from_json(json.dumps(translationJob)))
        else:
            logging.error(f'Error getting translation status from Cognitive Services for job id, {jobId} : error code - {response.status_code}; error message - {response.reason}')
            logging.error(f'Status not updated in Cosmos DB for job id, {jobId}')

