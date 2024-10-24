from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import sys
import time

def upload_to_drive(file_path):
    # Authenticate and create the PyDrive client
    gauth = GoogleAuth()

    # Command-line authentication (No redirect issues)
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # This will give you a link to authenticate manually in your browser
        gauth.CommandLineAuth()  
    elif gauth.access_token_expired:
        gauth.Refresh()  # Refresh the access token if expired
    else:
        gauth.Authorize()  # Use saved credentials

    gauth.SaveCredentialsFile("mycreds.txt")  # Save credentials for future use

    drive = GoogleDrive(gauth)

    try:
        file_size = os.path.getsize(file_path)  # Get file size in bytes
        file_to_upload = drive.CreateFile({'title': file_path.split('/')[-1]})
        file_to_upload.SetContentFile(file_path)

        # Track upload progress
        start_time = time.time()
        file_to_upload.Upload()  # Perform the actual upload

        elapsed_time = time.time() - start_time
        uploaded_bytes = file_size  # Full file size since Upload() doesn't provide progress events
        speed = uploaded_bytes / elapsed_time / (1024 * 1024)  # MB per second
        print(f"Uploaded: {uploaded_bytes}/{file_size} bytes (100.00%) at {speed:.2f} MB/s")

        # Make the file public
        file_to_upload.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'
        })

        # Get the shareable link
        file_link = file_to_upload['alternateLink']
        print(f"File uploaded successfully. Public link: {file_link}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_to_drive.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    upload_to_drive(file_path)
