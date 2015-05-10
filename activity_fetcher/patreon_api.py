import json
import requests
from activity_fetcher.config import Config
from activity_fetcher.database import Database

__author__ = 'sfaci'
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
        r = session.post(url, data=json_foo)
        response  = json.loads(r.text)
        print("Successfully logged as user_id: {id}, name: {name}".format(id=response['data']['id'], name=response['data']['full_name']))
        return session

    @staticmethod
    def process_csv_to_database(raw_data):
        db = Database()
        db.load_data(raw_data)

    def load_api_data(self, file_name=None):
        if file_name is None:
            session = self.cookie_login()
            get_data_url = self.config.url('fetch_data')
            r = session.get(get_data_url)
            return r.text
        else:
            f = open(file_name, 'r')
            return f.read()


    def process_data(self, response):
        if self.config.use_database:
            self.process_csv_to_database(response)
            print("Data has been dumped to: {db}".format(db=self.config.dbname))
        else:
            ## write the data out to a file.
            f = open(self.config.file_name, 'w')
            f.write(response)
            f.close()
            print("Data has been written out to: {file}".format(file=self.config.file_name))


