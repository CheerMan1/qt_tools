# -*- coding: utf-8 -*-
import requests
import json

TOKEN = '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'  # your github token
OWNER = 'CheerMan1'  # the repository's owner
REPO = 'qt_tools'  # the repository's name
headers = {'Authorization': f'token {TOKEN}'}

url = f'https://api.github.com/repos/{OWNER}/{REPO}/releases'
payload = {
  "tag_name": "v1.0.0",  # your release version tag
  "name": "v1.0.0",  # your release name (optional)
  "body": "Description of the release",  # your release description (optional)
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 201:
  print('Release was created successfully.')
else:
  print(f'Error: {response.content}')
