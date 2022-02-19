from __future__ import print_function
import json

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)
        items = []
        page_token = None
        while True:

            # Call the Drive v3 API
            # https://developers.google.com/drive/api/v3/search-files?authuser=3
            results = service.files().list(
                corpora = 'drive',
                spaces='drive',
                driveId='0AIBgH9I4QtkXUk9PVA',
                includeItemsFromAllDrives='true',
                supportsAllDrives='true',
                q="mimeType != 'application/vnd.google-apps.folder' and name contains 'flac'",
                pageToken=page_token, pageSize=1000, fields="nextPageToken, files(id, name)").execute()
            for item in results.get('files', []):
                items.append(item)
                # print(item)
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

        with open("drive_files.json", "w") as jsonfile:
                jsonfile.write(json.dumps(items, indent=4))
                
        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()