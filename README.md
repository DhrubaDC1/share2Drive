# Google Drive File Downloader

## Overview

A simple Python script to download files from Google Drive using file IDs, supporting both public and private files. The script includes progress tracking and creates the destination file if it doesn't exist.

## Features

- Download public and private files from Google Drive.
- Progress tracking during download.
- Automatic creation of the destination file and directory.

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
### Download Public Files
```bash
python download.py <file_id> <destination_path>
```
