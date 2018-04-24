#!/usr/bin/env python
#Created by Austin Jones
#This script creates schedule for a protection domain

import pprint
import json
import os
import random
import requests
import sys
import traceback

class TestRestApi():

    def __init__(self):

        #Initialize
        self.serverIpAddress = "10.1.11.6"
        self.username = "admin"
        self.password = "Nutanix4u!"
        # Base URL at which REST services are hosted in Prism Gateway.
        BASE_URL = 'https://%s:9440/PrismGateway/services/rest/v2.0/'
        self.base_url = BASE_URL % self.serverIpAddress
        self.session = self.get_server_session(self.username, self.password)
    
    def get_server_session(self, username, password):

        #Creating REST client session for server connection, after globally setting
        #Authorization, content type, and character set for the session.
        session = requests.Session()
        session.auth = (username, password)
        session.verify = False
        session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
        return session

    def createPDSchedule(self):
        clusterURL = self.base_url + "/protection_domains/testPD/schedules"
        print("Creating a schedule for the protection domain")
        payload = {}
        #payload["appConsistent"] = True
        #payload["everyNth"] = "30"
        #payload["pdName"] = "testPD"
        #payload["retentionPolicy"] = {"localMaxSnapshots": "1", "remoteMaxSnapshots": {}}
        payload["start_times_in_usecs"] = ["1525118400000000"]
        #payload["suspended"] = False
        #payload["userStartTimeInUsecs"] = "1525118400000000"
        #payload["durationInUsecs"] = "1525118400000000"
        #payload["endTimeInUsecs"] = "1525118400000000"
        #payload["values"] = []
        payload["type"] = "WEEKLY"
        payloadInJson = json.dumps(payload)
        print(("=" * 79))
        print(("=" * 79))
        print(("=" * 79))
        print(payloadInJson)
        print(("=" * 79))
        print(("=" * 79))
        print(("=" * 79))
        serverResponse = self.session.post(clusterURL, data=payloadInJson)
        print("Response code: %s" % serverResponse.status_code)
        return json.loads(serverResponse.text)

    def getProtectionDomainSchedule(self):
        clusterURL = self.base_url + "/protection_domains/testPD/schedules"
        print("Getting protection domain schedules for testProtectionDomain:")
        serverResponse = self.session.get(clusterURL)
        print("Response code: %s" % serverResponse.status_code)
        return serverResponse.status_code, json.loads(serverResponse.text)


if __name__ == "__main__":

    try:    

        pp = pprint.PrettyPrinter(indent=2)

        testRestApi = TestRestApi()
        print(("=" * 79))

        #Create a replication schedule for the Protection Domain
        newSchedule = testRestApi.createPDSchedule()
        print("Text: ")
        pp.pprint(newSchedule)
        print(("=" * 79))
        print(("=" * 79))
        print(("=" * 79))

        #Get the protection domain schedule
        schedules = testRestApi.getProtectionDomainSchedule()
        print("Text: ")
        pp.pprint(schedules)
        print(("=" * 79))
        print(("=" * 79))
        print(("=" * 79))
            
    
    except Exception as ex:
        print(ex)
        sys.exit(1)