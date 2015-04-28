#!/usr/bin/env python3
import json
import os
import requests
import yaml
import datetime as dt


class Patreon():
    """
      The purpose of this class is to encapsulate the Patreon API
    """
    yaml_data = {}

    def __init__(self):
        file = open('patreon.yaml', 'r')
        self.yaml_data = yaml.load(file)
        self.credentials = self.yaml_data['credentials']

    def __get_url__(self, url_name):
        return self.yaml_data['urls'][url_name]


    def get_file_name(self):
        today = dt.datetime.now()
        date_format = self.get_date_format()
        folder_name = self.yaml_data['properties']['folder']
        file_name = self.yaml_data['properties']['file']
        return os.path.join(folder_name, today.strftime(date_format) + "_" + file_name + ".csv", )

    def get_date_format(self):
        return self.yaml_data['properties']['dateformat']

    def cookie_login(self):
        payload = {'data': self.credentials}
        url = self.__get_url__('login')
        session = requests.Session()
        session.headers.update({'Content-type': 'application/vnd.api+json'})
        json_foo = json.dumps(payload)
        r = session.post(url, data=json_foo, verify=False)
        print(r.text)
        return session


    def get_data(self):
        session = self.cookie_login()
        get_data_url = self.__get_url__('fetch_data')
        r = session.get(get_data_url, verify=False)
        response = r.text
        f = open(self.get_file_name(), 'w')
        f.write(response)
        f.close()


def main():
    patreon = Patreon()
    patreon.get_data()


if __name__ == "__main__":
    main()

