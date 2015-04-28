# Patreon Activity Fetcher (and Parser)

## Installation.

pip install -r requirements.txt

## Usage instructions

copy patreon.yaml.example and rename it patreon.yaml.  Update the email and password 
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

