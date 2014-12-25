A python3 script that pulls a list of companies in the specified area from the Yelp API and saves it as an excel-compatible CSV file.

This script takes the location as a command-line argument.  For a location with more than one word (e.g. "las vegas"), use quotes to surround it.  Otherwise, the script will only use the first word.

Dependencies: 

rauth
https://rauth.readthedocs.org/