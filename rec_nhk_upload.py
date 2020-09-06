from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient import discovery
from apiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
import json
import base64
from email.mime.text import MIMEText
from email.utils import formatdate
#import pandas as pd
import datetime
import subprocess
import glob
import os

# Setup the Drive v3 API
SECRET_KEY = 'test_pg.json'
SCOPE1 = 'https://www.googleapis.com/auth/drive'
SCOPE2 = 'https://www.googleapis.com/auth/spreadsheets'
SCOPE3 = 'https://mail.google.com/'
SCOPE4 = 'https://www.googleapis.com/auth/calendar'
SCOPES = SCOPE1 + ' ' + SCOPE2 + ' ' + SCOPE3 + ' ' + SCOPE4
GDRIVE_FOLDER_ID = '1KM0BjZNDgxID8ZP97opIiKVyHqsA5XaN'
REC_FOLDER = "/home/pi/nhk"
CHANNNEL = "NHK2"
MAIL_FROM = "zong1yuan2@gmail.com"
MAIL_TO = "zong1yuan2@gmail.com, zong1yuan2@live.jp"


def get_credential():
    store = file.Storage('/home/pi/credentials.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(SECRET_KEY, SCOPES)
        creds = tools.run_flow(flow, store)

    return creds

def rec_radio(channel, rectime, rec_folder):
    cmd = 'sh /home/pi/rec_nhk.sh' + " " + channel + " " + str(rectime) + " " + rec_folder
    process = (subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
    #print('コマンドは\n'+process+'です')#何かしらの処理

def upload_data(creds, rec_folder, upload_folder):
    service = build('drive', 'v3', http=creds.authorize(Http()))
    os.chdir(rec_folder)
    files = glob.glob("./*")
    for file in files:
        print("FILE ===> " + file)
        filename = file.replace('./NHK2_', 'ラジオ英会話_')

        file_metadata = {
            'name': filename,
            'mimeType': "audio/mpeg",
            'parents': [upload_folder]
            }
        media = MediaFileUpload(str(file),
                            mimetype='application/vnd.google-apps-document',
                               resumable=True)
        service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
        pathfile = file.replace('./','')
        path = rec_folder + "/" + pathfile
        print('removefile ===> ' + path)
        os.remove(path)

if __name__ == '__main__':
    creds = get_credential()
    rec_radio(CHANNNEL, 16, REC_FOLDER)
    upload_data(creds, REC_FOLDER, GDRIVE_FOLDER_ID)
