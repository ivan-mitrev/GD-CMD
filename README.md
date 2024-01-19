# Google Drive Download Script
## How to download a folder from google drive using terminal?

This is a Python script intended to download files and folders from Google Drive. The script makes use of Google's Drive API and requires user authentication.

## Getting Started
`git clone https://github.com/ivan-mitrev/GD-CMD.git`

### Prerequisites
This script requires Python and several Python libraries, which are specified below:

- google-auth-oauthlib
- google-auth-httplib2
- google-auth
- google-api-python-client
- pickle
- io
- sys
- os

### 🔧 Installation
-----

The recommended method to install these libraries is via pip:

pip install google-auth-oauthlib google-auth-httplib2 google-auth google-api-python-client `

or

`pip install -r requirements.txt`


### 🔥 Usage
-----

The script can be used from the command line as follows:


`python gd.py <folder_id> <destination_folder>`

Where:

-   `folder_id` is the unique id of the Google Drive folder you want to download.
-   `destination_folder` is the path where you want the downloaded folder to be stored.

-----

### The script requires a  <span style="color:red">credentials.json</span> file for API access.

The script also uses a `token.pickle` file to store the user's access and refresh tokens. This file is created automatically when the authorization flow completes for the first time.

<span style="color:red">If you are using a non-desktop operating system, you must first log in via desktop to generate a token. You can then upload all files to your server, including "token.pickle", which allows you to initiate file downloads directly without authentication.</span>Тhis is necessary because authentication takes place through an internet browser.

License
-------

This project is licensed under the MIT License.
