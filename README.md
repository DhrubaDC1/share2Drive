# Google Drive File Uploader

## Overview

A Python script to upload files to Google Drive using the Google Drive API. This script supports both small and large file uploads, provides progress tracking, and makes the uploaded file public.

## Features

- Upload files to Google Drive.
- Supports progress tracking (upload speed, percentage).
- Automatically creates the file if it doesn't exist.
- Makes uploaded files public and retrieves the shareable link.

## Requirements

- Python 3.x
- `requests`, `google-auth`, `google-auth-oauthlib`, `google-api-python-client` libraries

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/yourusername/share2Drive.git
   cd share2Drive
```
2. Install required libraries:
```bash
pip install -r requirements.txt
```
3. Set up Google Drive API and place credentials.json in the project directory.
## Usage
### From Windows
```bash
upload.bat <file_path>
```
### From MacOS
```bash
upload.sh <file_path>
```
### With python
```bash
python download.py <file_path>
```
