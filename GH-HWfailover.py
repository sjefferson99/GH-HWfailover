#!/bin/env python3
import requests
import json
import argparse
import time

#Logic for assessing the delta in window is untested so may need tweaking
#Sleep for 60 will skew the window time as it increases as it does not consider execution time of loop

#argparser config
parser = argparse.ArgumentParser(description='Query the Genius Hub API for a primary zone active state and boost the secondary zone if the temperature does not rise sufficiently quickly. A good example is a boiler controlled HW zone as primary with an immersion as secondary with the temp probe feeding both zones.')
parser.add_argument('token', help='The auth token provided by mygenius hub portal https://my.geniushub.co.uk/#/tokens')
parser.add_argument('primary', help='The zone to be monitored')
parser.add_argument('secondary', help='The zone to boost on failure')
parser.add_argument('delta', help='Degrees change expected in the assessment window in the primary zone when heating')
parser.add_argument('window', help='Assessment window size in minutes')
parser.add_argument('--debug', action='store_true', help='Enable debug output on run')

args = parser.parse_args()

if args.debug:
    print("Arguments supplied:")
    print(args)

#custom functions
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def ghquery(apipath):
    #Query the GH API and print info on debug
    token = args.token
    baseurl = "https://my.geniushub.co.uk/v1/"
    headers = {"Authorization": "Bearer " + token}
    url = baseurl + apipath
    
    response = requests.get(url, headers=headers)

    if args.debug:
        print("Requested path: " + apipath)
        print("Request status: ")
        print(response.status_code)
        print("Response: ")
        jprint(response.json())
        print("Raw response JSON")
        print(response.json())

    return response

def ghpost(apipath,jsondata):
    #Post the GH API
    token = args.token
    baseurl = "https://my.geniushub.co.uk/v1/"
    headers = {"Authorization": "Bearer " + token}
    url = baseurl + apipath
    
    response = requests.post(url, headers=headers, json=jsondata)

    if args.debug:
        print("Requested path: " + apipath)
        print("Request status: ")
        print(response.status_code)
        print("Response: ")
        jprint(response.json())
        print("Raw response JSON")
        print(response.json())

    return response

zonelist = {}
response = ghquery("zones")
zones = response.json()
window = int(args.window)
delta = int(args.delta)

for zone in zones:
    zonelist[zone['name']] = zone['id']
    
history = []

while True:

    #get primary zone info
    response = ghquery("zones/" + str(zonelist[args.primary]))
    primaryzonedata = response.json()

    #get secondary zone data
    response = ghquery("zones/" + str(zonelist[args.secondary]))
    secondaryzonedata = response.json()

    if primaryzonedata['output'] == 1:
        print("primary zone calling for heat")
        history.append(primaryzonedata['temperature'])
        
        if len(history) >= (window + 1):
            print("Enough history data")
            if history[(len(history) - 1)] - history[len(history) - (window + 1)] < delta:
                print("Primary zone not heating fast enough")
                if secondaryzonedata['output'] != 1:
                    print("Boosting immersion")
                    apipath = "zones/" + str(zonelist[args.secondary]) + "/override"
                    print(apipath)
                    jsondata = '{"duration": 1800, "setpoint": 25.0}' #Seems setpoint is always 30 on GH regardless of setpoint value - possible bug?
                    print(jsondata)
                    result = ghpost(apipath, jsondata)
                    print(result)
                else:
                    print("Immersion already boosted")
            else:
                print("Primary zone is heating fast enough")
        else:
            print("Not enough history data")
    else:
        print("primary zone not calling for heat")
        history = []

    time.sleep(60)