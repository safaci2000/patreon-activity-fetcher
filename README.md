# Patreon Activity Fetcher (and Parser)

##Note

This app should run on python 2.x but it has been mainly developed under python 3.x. You'll probably run into less issues if you use 3.x but if there any issues with py 2.x, do let me know.

## Installation.

pip install -r requirements.txt

## Usage instructions

copy config/patreon.yaml.example and rename it config/patreon.yaml.  Update the email and password 
fields accordingly.

to execute simply run:

./patreon.py

## Configuration

email and password are the only field that you need to update for this script to function. Optionally there are other customizations you can make.

under properties you can configure:

datetime:  https://docs.python.org/3/library/datetime.html for strftime formatting options.
folder:  destination folder of the reports.  Please create the folder before executing the script
file:  the file name of the report.  

Final file name will be something like:  folder/datefomrat_filename.csv

## Database

Currently, sqlite and mysql is supported.

###SQLite

I would highly encourage using MySQL over sqlite.  sqlite implementation seems to have issue with rounding and representing decimals properly.   For now, sqlite support is left in since its requires virtually no setup.

###MySQL

Requirements:

 - Requires InnoDB.  
 - encoding: utf8  (You can probably get away with latin1, though this will explode if you have an international user base) 


###Other Databases
The engine being used is SQLAlchemy.  In theory any backend engine which SQLAlchemy [supports](http://docs.sqlalchemy.org/en/latest/dialects/index.html) can be enabled with a trivial amount of code.  Though I'm focusing primarily on MySQL at the moment. 


