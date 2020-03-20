# coding:utf-8

import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import logging
import os
import sys
import traceback
import json
from datetime import datetime, date, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class GoogleCalendar(object):

    def __init__(self):
        self.service_account_id = os.environ['SERVICE_ACCOUNT_ID']

    def get_credentials(self):
        scopes = 'https://www.googleapis.com/auth/calendar'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'google_key.json',
            scopes=scopes
        )

        return credentials

    def get_schedule(self, calendar_id, time_min, time_max):
        try:
            credentials = self.get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build(
                'calendar',
                'v3',
                http=http
            )

            events = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True
            ).execute()

            items = events['items']
            items = list(map(
                lambda x: {'title': x['summary'], 'start': x['start'], "end": x["end"]}, items))

            return items

        except:
            import traceback
            traceback.print_exc()


def main(param):
    cal = GoogleCalendar()
    return cal.get_schedule(param["calendar_id"], param["time_min"], param["time_max"])


def lambda_handler(event, context):

    logger.info(event)
    try:
        response = main(json.loads(event["body"]))
        logger.info(response)

        return {
            'statusCode': 200,
            'body': json.dumps(response, ensure_ascii=False)
        }

    except:
        import traceback
        logger.error(traceback.format_exc(sys.exc_info()[2]))

