# -*- coding: utf-8 -*-
import json
import os
import requests
import sys

# TOKEN = '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'  # your github token
TOKEN = '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'
OWNER = 'CheerMan1'  # the repository's owner
REPO = 'qt_tools'  # the repository's name

# GitHub Actions 默认会在每个步骤结束时检查这个步骤的退出代码，如果不是 0，workflow 就会停止执行。


def check_release(release_version):
    print(f"Checking release {release_version}")
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{release_version}"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Release {release_version} already exists.")
    else:
        print(f"Release {release_version} does not exist. Creating now.")
        create_release(release_version)


def create_release(release_version):
    headers = {'Authorization': f'token {TOKEN}'}
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/releases'
    payload = {
        "tag_name": release_version,  # your release version tag
        "name": release_version,  # your release name (optional)
        "body": "Description of the release",  # your release description (optional)
    }
    print(payload)
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        print('Release was created successfully.')
    else:
        print(f'Error: {response.content}')
        return 1


if __name__ == "__main__":
    check_release(sys.argv[1])
