#!/usr/bin/env python3
"""
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import argparse
import json
import requests
from activity_fetcher.config import Config
from activity_fetcher.database import Database


class Patreon():
    """
      The purpose of this class is to encapsulate the Patreon API
    """
    def __init__(self):
        self.config = Config()



    def cookie_login(self):
        payload = {'data': self.config.credentials}
        url = self.config.url('login')
        session = requests.Session()
        session.headers.update({'Content-type': 'application/vnd.api+json'})
        json_foo = json.dumps(payload)
        r = session.post(url, data=json_foo, verify=False)
        print(r.text)
        return session


    def process_csv_to_database(self, raw_data):
        db_config= self.config.get_db_config(self.config.database_engine)
        db = Database(self.config.database_engine, db_config)
        db.load_data(raw_data)

    def get_data(self):
        session = self.cookie_login()
        get_data_url = self.config.url('fetch_data')
        r = session.get(get_data_url, verify=False)
        response = r.text
        if self.config.use_database:
            self.process_csv_to_database(response)
            print("Data has been dumped to: {db}".format(db=self.config.dbname))
        else:
            ## write the data out to a file.
            f = open(self.config.file_name, 'w')
            f.write(response)
            f.close()
            print("Data has been written out to: {file}".format(file=self.config.file_name))


def main():
    """
    Arge parsing is a bit pointless atm, but might be useful at some point in the future.
    :return:
    """
    parser = argparse.ArgumentParser(description='Patreon Activity Fetcher')
    parser.add_argument('--fetch', dest='fetch', default=False, action='store_true', help='fetch report')
    patreon = Patreon()

    args = parser.parse_args()

    if args.fetch:
        patreon.get_data()
    else: #default case
        patreon.get_data()


if __name__ == "__main__":
    main()

