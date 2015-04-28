#!/usr/bin/env python3
import json
import requests
import yaml

global credentials


def init():
    global credentials
    file = open('patreon.yaml', 'r')
    credentials = yaml.load(file)
    print(credentials)

def cookie_login():
    payload = {}
    payload['data'] = credentials
    url = "https://api.patreon.com/login"
    session = requests.Session()
    session.headers.update({'Content-type': 'application/vnd.api+json'})
    json_foo = json.dumps(payload)
    r = session.post(url, data=json_foo, verify=False)
    print(r.text)
    return session


def get_data(session):
    get_data_url = 'https://www.patreon.com/downloadCsv?hid='
    r = session.get(get_data_url, verify=False)
    response = r.text
    f = open('data.csv', 'w')
    f.write(response)
    f.close()


def main():
    init()
    # session = legacy_login()
    session = cookie_login()
    get_data(session)


if __name__ == "__main__":
    main()

