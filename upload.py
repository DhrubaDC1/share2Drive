import os
import sys
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def authenticate_google_drive():
    """Authenticate and create the Google Drive API client."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service


def upload_large_file(service, file_path, folder_id=None):
    """Uploads a file to a specified folder in Google Drive or to the root if no folder ID is provided."""
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    media = MediaFileUpload(file_path, resumable=True)

    # File metadata for upload
    file_metadata = {
        'name': file_name,
        'mimeType': 'application/octet-stream',
        'parents': [folder_id] if folder_id else []  # Use empty list for root upload
    }

    # Create the file on Drive
    request = service.files().create(body=file_metadata, media_body=media, fields='id')

    # Track upload progress
    start_time = time.time()
    response = None
    uploaded_bytes = 0

    # Use the request to upload in chunks and track progress
    while response is None:
        status, response = request.next_chunk()
        if status:
            uploaded_bytes += status.resumable_progress
            percentage = (uploaded_bytes / file_size) * 100
            elapsed_time = time.time() - start_time
            speed = uploaded_bytes / elapsed_time / (1024 * 1024)  # MB per second
            print(f"Uploaded: {uploaded_bytes}/{file_size} bytes ({percentage:.2f}%) at {speed:.2f} MB/s")

    print(f"Upload complete. File ID: {response['id']}")

    # Make the file public
    service.permissions().create(
        fileId=response['id'],
        body={'type': 'anyone', 'role': 'reader'},
    ).execute()

    # Get the shareable link
    shareable_link = f"https://drive.google.com/file/d/{response['id']}/view"
    print(f"Public link: {shareable_link}")
    return shareable_link


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:  # Expects one or two arguments
        print("Usage: python upload.py <file_path> [<folder_id>]")
        sys.exit(1)

    file_path = sys.argv[1]
    folder_id = sys.argv[2] if len(sys.argv) == 3 else None  # Optional folder ID

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    service = authenticate_google_drive()
    upload_large_file(service, file_path, folder_id)
