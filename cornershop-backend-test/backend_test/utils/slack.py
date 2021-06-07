from ..celery import app
from ..envtools import getenv
import requests
import json

SLACK_WEBHOOK_URL = getenv("SLACK_WEBHOOK_URL")


@app.task
def send_menu_slack(content):
    print('-'*10, 'IN SLACK TASK', '-'*10)
    return requests.post(SLACK_WEBHOOK_URL, json.dumps({"text": content}))
