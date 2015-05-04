import os
import io
from sqlalchemy.orm import sessionmaker
from activity_fetcher.config import Config
from activity_fetcher.patterns.singelton import Singleton
from activity_fetcher.models.activity import Activity, Base, HistoricalActivity
from datetime import datetime as dt
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


class Database(metaclass=Singleton):
    db_engine = None

    def __init__(self, engine, db_config):
        self.config = Config()
        if engine == 'sqlite':
            self.init_sqlite(db_config)
        elif engine == 'mysql':
            self.init_mysql(db_config)

    def init_mysql(self, db_config):
        """
        Note mysqldb driver is not supported.
        :param db_config:
        :return:
        """
        conn_string = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}?use_unicode=1&charset={encoding}' \
            .format(database=db_config['db_name'], username=db_config['username'], password=db_config['password'],
                    host=db_config['hostname'], port=db_config['port'], encoding=db_config['charset'])
        self.db_engine = create_engine(conn_string)

        self.init_schema()

    def init_sqlite(self, db_config):
        """
        This engine is currently unreliable with decimals.  Try using mysql for more accurate and dependable
        behavior.
        :param db_config:
        :return:
        """
        db_name = os.path.join(self.config.out_folder, db_config['db_name'])
        conn_string = '{engine}:///{db_name}'.format(engine='sqlite', db_name=db_name)
        self.db_engine = create_engine(conn_string)

        self.init_schema()


    def init_schema(self):
        try:
            self.db_engine.execute("select * from activity limit 1")
        except:
            print("activity table does not exist, initializing DB schema.")
            self.init_schema()

    @staticmethod
    def sanitize_numeric(value):
        if value is not None and len(value) > 0:
            return value.replace(",", "")
        return value


    def __generate_activity_record__(self, item):
        activity = Activity()
        activity.name = item[0]
        activity.email = item[1]
        activity.pledge = self.sanitize_numeric(item[2])
        activity.lifetime = self.sanitize_numeric(item[3])
        activity.status = item[4]
        activity.twitter = item[5]
        activity.shipping = item[6]
        try:
            activity.start = dt.strptime(item[7], '%Y-%m-%d %H:%M:%S')
        except:
            epoch = dt.fromtimestamp(0)
            print("warning:  invalid start date for record: {item}, using epoch date: {epoch}"
                  .format(item=item, epoch=epoch))
            activity.start = epoch

        if item[8] == 'No Max Set':
            item[8] = '-1';
        activity.max_amount = self.sanitize_numeric(item[8])

        return activity

    def load_data(self, raw_data):
        """
        :param raw_data:  CSV file
        :return:
        """
        ioString = io.StringIO(raw_data)
        cvsFile = csv.reader(ioString)
        data = [row for row in cvsFile]
        count = 0
        Session = sessionmaker(bind=self.db_engine, autoflush=False)
        session = Session()
        for item in data:
            ##skip headers
            if count == 0:
                count += 1
                continue
            if item[0].find("Reward") != -1:
                # TODO: process reward here.
                continue

            new_record = self.__generate_activity_record__(item)

            old_record = session.query(Activity).filter_by(email=new_record.email).first()

            if old_record == None:
                historical_record = HistoricalActivity(new_record)
                session.merge(historical_record)
                session.merge(new_record)
            elif old_record != new_record:
                #record a new entry in the historical archives
                historical_record = HistoricalActivity(new_record)
                session.merge(historical_record)
                #update the values
                session.merge(new_record)
                print("writing new entry for:  item: {values} no changes".format(values=item))
            else:
                pass
                # print("skipping:  item: {values} no changes".format(values=item))


        session.commit()


    def init_schema(self):
        """
        This method will create the table schema required for data input.
        :return:
        """
        Base.metadata.create_all(self.db_engine)
        print("created new tables")
