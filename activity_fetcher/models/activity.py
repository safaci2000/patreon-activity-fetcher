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
from sqlalchemy import Column, DateTime, String, Integer, Float, Index, Numeric, func, Numeric, Text, ForeignKey
from decimal import Decimal

(12, 2)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Activity(Base):
    __tablename__ = 'activity'
    email = Column(String(250), primary_key=True)
    name = Column(String(250))
    pledge = Column(Numeric(12, 2))
    lifetime = Column(Numeric(12, 2))
    status = Column(String(20))  ##no idea on the format
    twitter = Column(String(200))
    shipping = Column(String(1000))
    start = Column(DateTime)  ##no idea on the format
    max_amount = Column(Numeric(12, 2))  ## or -1 if 'No Max Set' returned
    reward_id = Column(Integer, ForeignKey('rewards.id'),  default=None)

    def __eq__(self, other):

        return other != None and self.email == other.email and \
               self.name == other.name and \
               Decimal(self.pledge) == Decimal(other.pledge) and \
               Decimal(self.lifetime) == Decimal(other.lifetime) and \
               self.status == other.status and \
               self.twitter == other.twitter and \
               self.shipping == other.shipping and \
               self.start == other.start and \
               Decimal(self.max_amount) == Decimal(other.max_amount) and \
               self.reward_id == other.reward_id



    def __repr__(self):
        return "<Activity(name='%s', email='%s', status='%s')>" % (self.name, self.email, self.status)


class HistoricalActivity(Base):
    """
      This is an exacte duplicate of the Activity table with 2 main differences.

      1.  pkey is an autoincremented ID
      2.  modified_date

    """
    __tablename__ = 'activityhistory'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    email = Column(String(250))
    name = Column(String(250))
    pledge = Column(Numeric(12, 2))
    lifetime = Column(Numeric(12, 2))
    status = Column(String(20))
    twitter = Column(String(200))
    shipping = Column(String(1000))
    start = Column(DateTime)
    max_amount = Column(Numeric(12, 2))  ## or -1 if 'No Max Set' returned
    modified_date = Column(DateTime, default=func.now())
    reward_id = Column(Integer, ForeignKey('rewards.id'),  default=None)

    def __init__(self, activity):
        super()
        self.email = activity.email
        self.name = activity.name
        self.pledge = activity.pledge
        self.lifetime = activity.lifetime
        self.status = activity.status
        self.twitter = activity.twitter
        self.shipping = activity.shipping
        self.start = activity.start
        self.max_amount = activity.max_amount
        self.reward_id = activity.reward_id

    Index('idx_email', email)
    Index('idx_modified_date', modified_date)


    def __repr__(self):
        return "<ActivityHistory(name='%s', email='%s', status='%s')>" % (self.name, self.email, self.status)


class Rewards(Base):
    """
      This is an exacte duplicate of the Activity table with 2 main differences.

      1.  pkey is an autoincremented ID
      2.  modified_date

    """
    __tablename__ = 'rewards'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    required_pledge = Column(Numeric(12, 2))
    description = Column(Text)


    def __repr__(self):
        return "<Rewards(id='%s', pledge='%s', description='%s')>" % (self.id, self.pledge, self.description)

