# Patreon Activity Fetcher (and Parser)

##Note

This app should run on python 2.x but it has been mainly developed under python 3.x. You'll probably run into less issues if you use 3.x but if there any issues with py 2.x, do let me know.

##Author Note.  

The main data source for this project is the .csv file that can be downloaded.  The current state of the projects allows for historical queries.  It can generate some basic simple graphs and 
visualization though I'm honestly not sure what is and isn't interesting to see.  It probably depends on the person heavily.  

The last feature I wanted to implement was integration with something like mailman.  Though seeing as you already have a database with all the user's name/emails.  You could easily 
link postfix or any decent mail server to send a broadcast. 

(Patreon has an issue with sending duplicates and triplicates of some email communications)

Future possible improvements:

 - generate an RSS feed of activity since for whatever reason patreon doesn't seem to allow for it. 
 - more visualization and effects.  Though for the time being this is release 0.1
 

## Installation.

pip install -r requirements.txt

## Usage instructions

copy config/patreon.yaml.example and rename it config/patreon.yaml.  Update the email and password 
fields accordingly.

to execute simply run:

./patreon.py

##Crontab Operations

crontab -e 

@hourly patreon.py --fetch 
@daily  patreon.py --visualize 

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



