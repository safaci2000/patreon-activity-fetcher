import os
import io
from sqlalchemy.orm import sessionmaker, scoped_session
from activity_fetcher.config import Config
from activity_fetcher.patterns.singelton import Singleton
from activity_fetcher.records import Base, Activity
import csv

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
from sqlalchemy import *


## TODO: currently there is no historical data support.  Add that in.
class Database(metaclass=Singleton):
    db_engine = None

    def __init__(self, engine, db_config):
        self.config = Config()
        if engine == 'sqlite':
            self.init_sqlite(db_config)

    def init_sqlite(self, db_config):
        db_name = os.path.join(self.config.out_folder, db_config['db_name'])
        conn_string = '{engine}:///{db_name}'.format(engine='sqlite', db_name=db_name)
        self.db_engine = create_engine(conn_string)

        try:
            self.db_engine.execute("select * from activity limit 1")
        except:
            print("activity table does not exist, initializing DB schema.")
            self.init_schema()

    def load_data(self, raw_data):
        """
        :param raw_data:  CSV file
        :return:
        """
        ioString = io.StringIO(raw_data)
        cvsFile = csv.reader(ioString)
        data = [row for row in cvsFile]
        count = 0
        session = scoped_session(sessionmaker(bind=self.db_engine))
        print(dir(session))
        for item in data:
            ##skip headers
            if count == 0:
                count += 1
                continue

            activity = Activity()
            activity.name = item[0]
            activity.email = item[1]
            activity.pledge = item[2]
            activity.lifetime = item[3]
            activity.status = item[4]
            activity.twitter = item[5]
            activity.shipping = item[6]
            activity.start = item[7]
            if item[8] == 'No Max Set':
                item[8] = '-1';
            activity.max_amount = item[8]
            ## essentially does an upsert
            session.merge(activity)

        session.commit()


    def init_schema(self):
        """
        This method will create the table schema required for data input.
        :return:
        """
        Base.metadata.create_all(self.db_engine)
        print("created new tables")



