import inspect
import os
import yaml
from activity_fetcher.patterns.singelton import Singleton
import datetime as dt

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


class Config(metaclass=Singleton):
    def __init__(self):
        project_path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "../")
        project_path = os.path.realpath(project_path)

        # file = open(os.path.join()'config/patreon.yaml', 'r')
        file = open(os.path.join(project_path, 'config/patreon.yaml'), 'r')
        self.yaml_data = yaml.load(file)

        ## All Properties should be at the start of the file.

    @property
    def credentials(self):
        return self.yaml_data['credentials']

    @credentials.setter
    def credentials(self, value):
        self.yaml_data['credentials'] = value

    @property
    def use_database(self):
        return self.yaml_data['backends']['database']

    @use_database.setter
    def use_database(self, value):
        self.yaml_data['backends']['database'] = value

    @property
    def database_engine(self):
        return self.yaml_data['backends']['engine']

    @database_engine.setter
    def database_engine(self, value):
        self.yaml_data['backends']['engine'] = value

    @property
    def dbname(self):
        return self.yaml_data['backends'][self.database_engine]['db_name']

    @dbname.setter
    def dbname(self, value):
        self.yaml_data['backends'][self.database_engine]['db_name'] = value

    @property
    def dbuser(self):
        return self.yaml_data['backends'][self.database_engine]['username']

    @dbname.setter
    def dbuser(self, value):
        self.yaml_data['backends'][self.database_engine]['username'] = value

    @property
    def dbpassword(self):
        return self.yaml_data['backends'][self.database_engine]['password']

    @dbname.setter
    def dbpassword(self, value):
        self.yaml_data['backends'][self.database_engine]['password'] = value

    @property
    def dbhostname(self):
        return self.yaml_data['backends'][self.database_engine]['hostname']

    @dbname.setter
    def dbhostname(self, value):
        self.yaml_data['backends'][self.database_engine]['hostname'] = value

    @property
    def dbport(self):
        return self.yaml_data['backends'][self.database_engine]['port']

    @dbname.setter
    def dbport(self, value):
        self.yaml_data['backends'][self.database_engine]['port'] = value



    @property
    def out_folder(self):
        return self.yaml_data['properties']['folder']

    @out_folder.setter
    def out_folder(self, value):
        self.yaml_data['properties']['folder'] = value

    @property
    def file_name(self):
        today = dt.datetime.now()
        folder_name = self.yaml_data['properties']['folder']
        file_name = self.yaml_data['properties']['file']
        return os.path.join(folder_name, today.strftime(self.date_format) + "_" + file_name + ".csv", )

    @property
    def date_format(self):
        return self.yaml_data['properties']['dateformat']


    def url(self, key):
        return self.yaml_data['urls'][key]

    def get_db_config(self, engine):
        return self.yaml_data['backends'][engine];



