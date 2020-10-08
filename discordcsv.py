import csv
import os
import pathlib
import urllib.request
import DownloadProgressBar
import jsonUtils

def getContents(d_dir, jsonContent):
    texts = []
    urls = []

    for subdir, dirs, files in os.walk(d_dir):
        for file in files:
            directory = os.path.join(subdir, file)
            if ('messages.csv' in file):
                for dir in jsonContent.keys():
                    if str(dir) in directory:
                        with open(directory, 'rt', newline='', encoding='utf-8') as csvfile:
                            reader = csv.DictReader(csvfile)
                            for row in reader:
                                if ('.com' in row['Contents'] or 'http' in row['Contents']):
                                    urls.append(row['Contents'])
                                elif ('.com' in row['Attachments'] or 'http' in row['Attachments']):
                                    urls.append(row['Attachments'])
                                elif (len(row['Contents']) > 0):
                                    texts.append(row['Contents'])
    return urls, texts;

def download_url(url, output_path):
    with DownloadProgressBar.DownloadProgressBar(unit='B', unit_scale=True,
                                                 miniters=1, desc=url.split('/')[-1]) as pbar:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(url, filename=output_path, reporthook=pbar.update_to)


currentDirectory = os.getcwd()
discord_dir = 'F:\Backup\Discord'
messages_dictionary_json = 'F:\Backup\Discord\messages\index.json'

#este método pode ser usado para filtrar os contatos, assim você apenas baixa os conteúdos que você enviou a esses contatos
#names = ['Abbe']
#jsonData = jsonUtils.filterJson(messages_dictionary_json, names)

jsonData = jsonUtils.filterJson(messages_dictionary_json)
outPath = currentDirectory.join('Download_Discord')
textsDir = outPath.join('Texts') #diretório onde os textos são enviados

urls, texts = getContents(discord_dir, jsonData)

pathlib.Path(textsDir).mkdir(parents=True, exist_ok=True)

errorDownloadFile = open(textsDir + 'errorDownload.txt', "w+", encoding='utf-8')
blankDownloadFile = open(textsDir + 'blankDownload.txt', "w+", encoding='utf-8')
textFile = open(textsDir.join('Texts.txt'), "w+", encoding='utf-8')

for text in texts:
    textFile.write(text + '\n')
textFile.close()

i = 0
for url in urls:
    fileName = os.path.basename(url)
    fileFormat = pathlib.Path(fileName).suffix

    if(fileFormat == ''):
        blankDownloadFile.write(url + '\n')
        continue;

    if 'unknown' in fileName:
        fileName = 'unknown' + str(i) + fileFormat
        i += 1

    outPathFile = outPath + '\\' + fileName

    try:
        download_url(url, outPathFile)
    except:
        errorDownloadFile.write(url + '\n')

errorDownloadFile.close()
blankDownloadFile.close()

