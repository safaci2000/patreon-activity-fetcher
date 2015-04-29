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

    @property
    def credentials(self):
        return self.yaml_data['credentials']

    @credentials.setter
    def credentials(self, value):
        self.yaml_data['credentials'] = value


    def url(self, key):
        return self.yaml_data['urls'][key]

    @property
    def file_name(self):
        today = dt.datetime.now()
        folder_name = self.yaml_data['properties']['folder']
        file_name = self.yaml_data['properties']['file']
        return os.path.join(folder_name, today.strftime(self.date_format) + "_" + file_name + ".csv", )

    @property
    def date_format(self):
        return self.yaml_data['properties']['dateformat']

