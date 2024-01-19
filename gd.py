from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import io
import sys

def update_progress_bar(progress):
    bar_length = 20
    block = int(round(bar_length * progress))
    progress_str = f"[{'#' * block}{'-' * (bar_length - block)}] {int(progress * 100)}%"
    sys.stdout.write("\r" + progress_str)
    sys.stdout.flush()

SCOPES = ['https://www.googleapis.com/auth/drive']

def main(folder_id, destination_folder):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    download_folder(service, folder_id, destination_folder)

def download_folder(service, file_id, destination_folder):
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)

    results = service.files().list(
        pageSize=300,
        q="parents in '{0}'".format(file_id),
        fields="files(id, name, mimeType)"
    ).execute()

    items = results.get('files', [])

    for item in items:
        item_name = item['name']
        item_id = item['id']
        item_type = item['mimeType']
        file_path = os.path.join(destination_folder, item_name)

        if item_type == 'application/vnd.google-apps.folder':
            download_folder(service, item_id, file_path)  # Recursive call
        elif not item_type.startswith('application/'):
            download_file(service, item_id, file_path)

def download_file(service, file_id, file_path, max_file_size_mb=2):
    # Check if the file already exists or if its size is greater than 2 MB
    if os.path.exists(file_path) and os.path.getsize(file_path) > max_file_size_mb * 1024 * 1024:
        print(f"File '{file_path}' already exists or is larger than {max_file_size_mb} MB. Skipping download.")
        return

    print("-> Downloading file with id: {0} name: {1}".format(file_id, file_path))
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_path, mode='wb')

    try:
        downloader = MediaIoBaseDownload(fh, request, chunksize=50*1024*1024)
        done = False
        while done is False:
            try:
                status, done = downloader.next_chunk(num_retries=2)
                if status:
                    update_progress_bar(status.progress())
            except Exception as e:
                print(f"Error during download: {e}")

        print("Download Complete!")
    finally:
        fh.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python gd.py folder_id destination_folder")
    else:
        folder_id = sys.argv[1]
        destination_folder = sys.argv[2]
        main(folder_id, destination_folder)
