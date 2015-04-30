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
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Activity(Base):
    __tablename__ = 'activity'
    email = Column(String(250), primary_key=True)
    name = Column(String(250))
    pledge = Column(Float)
    lifetime = Column(Float)
    status = Column(String(200))  ##no idea on the format
    twitter = Column(String(200))
    shipping = Column(String(1000))
    start = Column(String(200))  ##no idea on the format
    max_amount = Column(Float)  ## or -1 if 'No Max Set' returned

    def __repr__(self):
        return "<Activity(name='%s', email='%s', status='%s')>" % (self.name, self.email, self.status)

