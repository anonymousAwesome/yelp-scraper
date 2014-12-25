# Note: This script requires the rauth python package and python 3.
# Preferably, python 3.4.x.
# Python packages like rauth are usually installed through pip
# (a python installation tool)

# This version of the script takes the location as a command-line argument.
# For a location with more than one word (e.g. "las vegas"), use quotes
# to surround it.  Otherwise, the script will only use the first word.

import rauth
import time
import csv
import math
import sys

location=sys.argv[1]

def main():
    yelp_returned_information=get_results(get_search_parameters(0))
    total=yelp_returned_information["total"]
    
    with open('some.csv', 'w', newline='') as f:
        #comment out whichever line is appropriate
        writer = csv.writer(f,dialect="excel")
        #writer = csv.writer(f)

        for i in range(0,math.ceil(total/20)):
            params = get_search_parameters(i*20)
            yelp_returned_information=get_results(params)
            writer.writerows(extract_information(yelp_returned_information))
            
            #pause to keep Yelp from cutting us off.  
            #No idea how necessary it is, but it really couldn't hurt.
            time.sleep(1.0)

def extract_information(yelp_information):
    
    results_keys=["name", "rating", "review_count", "display_phone", "url"]
    location_keys=[ 'address',  'city', 'state_code', 'postal_code']
    extracted_dict=[]

    for i in range(0, len(yelp_information["businesses"])):
        individual_business=[]
        for j in results_keys:
            individual_business.extend([yelp_information["businesses"][i].get(j,"empty field")])
        for j in location_keys:
            individual_business.extend([yelp_information["businesses"][i]["location"].get(j, "empty field")])
        extracted_dict.append(individual_business)
    return extracted_dict
    
    

def get_results(params):

    #Obtain these from Yelp's manage access page
    consumer_key = "consumer key goes here"
    consumer_secret = "consumer secret goes here"
    token = "token goes here"
    token_secret = "token secret goes here"
    
    session = rauth.OAuth1Session(
        consumer_key = consumer_key
        ,consumer_secret = consumer_secret
        ,access_token = token
        ,access_token_secret = token_secret)
        
    request = session.get("http://api.yelp.com/v2/search",params=params)
    
    #Transforms the JSON API response into a Python dictionary
    data = request.json()
    session.close()
    
    return data

def get_search_parameters(offset):
    #See the Yelp API for more details
    params = {}
    params["term"] = "consignment"
    params["location"]=location
    params["offset"] = offset

    return params

if __name__=="__main__":
    main()
