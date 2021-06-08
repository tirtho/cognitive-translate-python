# cognitive-translate-python

In order to run the command line translation tasks, set the following environment variables 

```
set TRANSLATOR_TEXT_SUBSCRIPTION_KEY=<Key1 or Key 2 from your Azure Cognitive Translation Services API>
set TRANSLATOR_TEXT_ENDPOINT=https://api.cognitive.microsofttranslator.com/
set TRANSLATOR_RESOURCE_LOCATION=<location where you instantiated your Azure Cognitive Translation Service, e.g. eastus2>

set TRANSLATOR_DOCS_SUBSCRIPTION_KEY=<Key from your Azure Cognitive Document Translator Service>
set TRANSLATOR_DOCS_HOST=<name of the translator instance, e.g. trtranslator>.cognitiveservices.azure.com
set TRANSLATOR_DOCS_ENDPOINT=https://<name of your document translator>.cognitiveservices.azure.com/translator/text/batch/v1.0
set TRANSLATOR_DOCS_SOURCE_CONTAINER_URL=<blob storage source container url, e.g. https://tbdemostoragev2.blob.core.windows.net/<name of source container>?sp=rl^&st=2021-05-31T01:02:12Z^&se=2041-06-01T09:02:12Z^&spr=https^&sv=2020-02-10^&sr=c^&sig=xxxxxxu%%2Fxxxxx%%3D>
set TRANSLATOR_DOCS_TARGET_CONTAINER_URL=<blob storage source url, e.g. https://tbdemostoragev2.blob.core.windows.net/tr-translator-target-docs?sp=rwl^&st=2021-05-31T01:13:36Z^&se=2041-06-01T09:13:36Z^&spr=https^&sv=2020-02-10^&sr=c^&sig=xxxxxx>
set TRANSLATOR_DOCS_GLOSSARY_CONTAINER_URL=<blob storage glossary container url, e.g. https://tbdemostoragev2.blob.core.windows.net/tr-translator-glossary-files?sp=rl^&st=2021-05-31T01:16:32Z^&se=2041-06-01T09:16:32Z^&spr=https^&sv=2020-02-10^&sr=c^&sig=xxxxxxxxxxxxxxx>
```
Notes: 
1. The keys above could be the same if you are running the document translation and text translation from the same instance of the Azure Cognitive Translation Service.
2. The examples above do not have real keys or secrets. These just show you how these string look like typically. 
3. If you are setting these environment variables from command line in Windows, some characters need escaping, like you need to prefix ^ before an &, or an additional % before a % character

Now you are ready to run the command line translation tasks.
Example: 
```
python TranslateText.py -f en -t de -q "My name is TR"
```
