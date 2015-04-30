import unittest
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
class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.config = Config()
        self.config.out_folder = "test_data"
        self.config.dbname = "test.db"
        db_config = self.config.get_db_config(self.config.database_engine)
        self.dbObj = Database(self.config.database_engine, db_config)

    def test_reader_csv_file(self):
        f = open('tests/sample_report.csv', 'r')
        raw = f.read()
        print(raw)
        self.dbObj.load_data(raw)
        ## TODO: valide writen data once we have a read functions implemented.


if __name__ == '__main__':
    unittest.main()

