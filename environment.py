########### Python 3.2 #############
import os, uuid

def getRequestHeader():
    subscription_key = getEnvironmentVariable('TRANSLATOR_TEXT_SUBSCRIPTION_KEY')
    endpoint = getEndpoint()
    location = getEnvironmentVariable('TRANSLATOR_RESOURCE_LOCATION')
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    return headers

def getRequestHeaderForDocumentTranslation():
    subscription_key = getEnvironmentVariable('TRANSLATOR_DOCS_SUBSCRIPTION_KEY')
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
    }
    return headers


def getEndpoint():
    return getEnvironmentVariable('TRANSLATOR_TEXT_ENDPOINT')

def getDocumentTranslatorEndpoint():
    return getEnvironmentVariable('TRANSLATOR_DOCS_ENDPOINT')

def getDocumentTranslatorHost():
    return getEnvironmentVariable('TRANSLATOR_DOCS_HOST')

def getDocumentTranslatorKey():
    return getEnvironmentVariable('TRANSLATOR_DOCS_SUBSCRIPTION_KEY')

def getDocumentTranslatorSourceUrl():
    return getEnvironmentVariable('TRANSLATOR_DOCS_SOURCE_CONTAINER_URL')

def getDocumentTranslatorTargetUrl():
    return getEnvironmentVariable('TRANSLATOR_DOCS_TARGET_CONTAINER_URL')

def getDocumentTranslatorGlossaryUrl():
    return getEnvironmentVariable('TRANSLATOR_DOCS_GLOSSARY_CONTAINER_URL')
        
def getEnvironmentVariable(var_name):
    if not var_name in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(var_name))
    return os.environ[var_name]

