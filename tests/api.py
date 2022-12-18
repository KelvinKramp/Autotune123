import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime as dt
from datetime import timedelta
import os
from definitions import ROOT_DIR
import json
import flask

secrets_path = os.path.join(ROOT_DIR, "tests", "secrets.json")
with open(secrets_path) as f:
    secrets = json.load(f)

url = "http://0.0.0.0:8080/api/"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
headers["Accept"] = "application/json"

token = secrets["token"]
NS_HOST = secrets["NS_URL"]
end_date =str(dt.now().date())
start_date = str(dt.now().date() - timedelta(3))
data = flask.json.dumps({
    "start_date" : start_date,
    "end_date" : end_date ,
    "NS_URL" : NS_HOST,
    "token" : token,
    "filter":"Savitzky-Golay 23.3",
    "insulin_type":"rapid-acting",
    "uam":False,
})


resp = requests.post(url, headers=headers, data=data)

print(resp.status_code)
print(resp.text)