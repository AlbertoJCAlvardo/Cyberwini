import os

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import gspread
from .config import settings as env_settings


def get_service():
    # use creds to create a client to interact with the Google Drive API
    print('fskg: ',env_settings.FILE_SECRET_KEY_GCP)
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    path = env_settings.FILE_SECRET_KEY_GCP
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        path, scopes
    )
    service = gspread.authorize(creds)

    return service


def get_sheet_access(service, key):
    sheet = service.open_by_key(key).sheet1

    return sheet

def get_sheet_by_name(service, key,  name):
    sheet = service.open_by_key(key).worksheet(name)
    return sheet

def get_service_drive():
    google_api = {
        'drive': {
            'name': 'drive',
            'version': 'v3',
            'scopes': [
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/drive.readonly.metadata',
            ]
        }
    }
    path = os.path.join(env_settings.FILE_SECRET_KEY_GCP
    )
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        path, google_api['drive']['scopes']
    )

    return build(
        google_api['drive']['name'], google_api['drive']['version'],
        credentials=creds
    )


class StatusCallbackShare():
    status = False
    response = None

    def set_data(self, status, response):
        self.status = status
        self.response = response

    def get_callback(self):
        return self.status, self.response


def share_file_to_user(service, file_id, user_email):
    # share data - sends email on drive of user
    # Return the status and the response of execute
    callback_success = StatusCallbackShare()

    def callback(request_id, response, exception):
        if exception:
            # Handle error
            callback_success.set_data(False, exception)
        else:
            # the permission was updated
            callback_success.set_data(True, response)

    batch = service.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': user_email,
    }
    batch.add(service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='*',
    ))
    batch.execute()

    return callback_success


def notify_users(service, file_key, emails):
    for mail in emails:
        notify = share_file_to_user(service, file_key, mail)
        print(notify.get_callback())
