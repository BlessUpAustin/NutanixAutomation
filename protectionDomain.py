#!/usr/bin/env python

import pprint
import json
import os
import random
import requests
import sys
import traceback

#This block initializes the parameters for the request.
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
    
    #Creating REST client session for server connection, after 
    #globally setting authorization, content type, and character
    #set for the session.
    session = requests.Session()
    session.auth = (username, password)
    session.verify = False
    session.headers.update(
        {'Content-Type': 'application/json; charset=utf-8'})
    return session

  #Prints the cluster information and loads JSON objects to be formatted.

  def getClusterInformation(self):
    clusterURL = self.base_url + "/cluster"
    print("Getting cluster information for cluster %s" % self.serverIpAddress)
    serverResponse = self.session.get(clusterURL)
    print("Response code: %s" % serverResponse.status_code)
    return serverResponse.status_code, json.loads(serverResponse.text)

  #Creates a protection domain with assigned name.

  def createProtectionDomain(self):
       
    protectionDomainURL = self.base_url + "/protection_domains"
    print("Creating a protection domain on cluster %s" % self.serverIpAddress)
    payload = {}
    #Designate a protection domain name.
    payload["value"] = "testPD"

    # The next payload line, which creates the vstore name mapping, 
    # will break the script if the connection to the 
    # remote datastore is inaccessible (as it is in test)
    
    #payload["vstore_name_map"] = {"default-container"}
		
    payloadInJson = json.dumps(payload)
    serverResponse = self.session.post(protectionDomainURL, data=payloadInJson)
    print("Response code: %s" % serverResponse.status_code)
    return json.loads(serverResponse.text)

  #Create the Protection Domain snapshot schedule

  def createPDSchedule(self):
    clusterURL = self.base_url + "/protection_domains/testPD/schedules"
    print("Creating a schedule for the protection domain")
    payload = {}
    payload["appConsistent"] = False
    payload["everyNth"] = "30"
    payload["pdName"] = "testPD"
    payload["retentionPolicy"] = {"localMaxSnapshots": "1", "remoteMaxSnapshots": {}}
    payload["startTimesInUsecs"] = ["1524174840000000"]
    payload["suspended"] = False
    payload["userStartTimeInUsecs"] = "1524174840000000"
    payload["type"] = "DAILY"
    payloadInJson = json.dumps(payload)
    serverResponse = self.session.post(clusterURL, data=payloadInJson)
    print("Response code: %s" % serverResponse.status_code)
    return json.loads(serverResponse.text)

  def getProtectionDomainSchedule(self):
    clusterURL = self.base_url + "/protection_domains/testPD/schedules"
    print("Getting protection domain schedules for testProtectionDomain:")
    serverResponse = self.session.get(clusterURL)
    print("Response code: %s" % serverResponse.status_code)
    return serverResponse.status_code, json.loads(serverResponse.text)

  #Get the list of snapshots in a protection domain
  def getSnapshots(self):
    snapshotsURL = self.base_url + "/protection_domains/testPD/dr_snapshots/"
    print("Getting the list of snapshots on cluster %s" % self.serverIpAddress)
    serverResponse = self.session.get(snapshotsURL)
    print("Response code: %s" % serverResponse.status_code)
    return json.loads(serverResponse.text)

  #Get the list of unprotected VMs.
  def getUnprotectedVMs(self):
    unprotectedVMURL = self.base_url + "/protection_domains/unprotected_vms/"
    print("List of unprotected VMs in cluster %s" % self.serverIpAddress)
    serverResponse = self.session.get(unprotectedVMURL)
    print("Response code: %s" % serverResponse.status_code)
    return json.loads(serverResponse.text)
    
  # Uncomment the below function if you wish to add all unprotected VMs  
  #def addVMtoPD(self):
    #addVMtoPDURL = self.base_url + "/protection_domains/testPD/protect_vms/"  
    #print("Added unprotected VMs to a Protection Domain on cluster %s" % self.serverIpAddress)
    #payload = {}
    #vms = testRestApi.getUnprotectedVMs()
    #vmNames = []
   ##Designate the name for the unprotected VM.
    #for vm in vms:
    #    vmNames.append(vm["vm_id"])					
    #payload["names"] = vmNames
    #payloadInJson = json.dumps(payload)
    #serverResponse = self.session.post(addVMtoPDURL, data=payloadInJson)
    #print("Response code: %s" % serverResponse.status_code)
    #return json.loads(serverResponse.text)
   
  #Add a specific VM to a protection domain. 
  def specificVMtoPD(self):
    #Designate the location of the protection domain for "pd_name".
    addVMprotectionDomainURL = self.base_url + "/protection_domains/testPD/protect_vms"  
    print("Added specific VM(s) to a protection domain on cluster %s" % self.serverIpAddress)
    payload = {}
    #Designate the name for the unprotected VM.
    payload["names"] = ["vm_name"]
    payloadInJson = json.dumps(payload)
    serverResponse = self.session.post(addVMprotectionDomainURL, data=payloadInJson)
    print("Response code: %s" % serverResponse.status_code)
    return json.loads(serverResponse.text)
    
if __name__ == "__main__":
  try:    
    #Set the Pretty Printer variable to format data.
    pp = pprint.PrettyPrinter(indent=2)
    
    # Start the execution of test cases.
    testRestApi = TestRestApi()
    print(("=" * 79))
    status, cluster = testRestApi.getClusterInformation()
    print(("=" * 79))
    
    #Uncomment to display cluster authentication response and information.
    #print("Status code: %s" % status)
    #print("Text: ") # %s" % cluster
    #pp.pprint(cluster)
    #print(("=" * 79))
    
    #Get specific cluster elements.
    print("Name: %s" % cluster.get('name'))
    print("ID: %s" % cluster.get('id'))
    print("Cluster External IP Address: %s" % cluster.get('clusterExternalIPAddress'))
    print("Number of Nodes: %s" % cluster.get('numNodes'))
    print("Version: %s" % cluster.get('version'))
    print(("=" * 79))
    print(("=" * 79))
    print(("=" * 79))

    #Create a Protection Domain
    protection_domain = testRestApi.createProtectionDomain()
    print("Text: ")
    pp.pprint(protection_domain)
    print(("=" * 79))
    print(("=" * 79))
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

    #Get the list of snapshots.
    protectionDomainSnapshots = testRestApi.getSnapshots()
    print("Text: ")
    pp.pprint(protectionDomainSnapshots)
    print(("=" * 79))
    print(("=" * 79))
    print(("=" * 79))

    #Get the list of unprotected VMs.
    unprotected_vms = testRestApi.getUnprotectedVMs()
    print("Text: ")
    pp.pprint(unprotected_vms)
    print(("=" * 79))
    print(("=" * 79))
    print(("=" * 79))

    # Uncomment the below block if you wish to add all VMs to the protection domain.
    #Add the list of uprotected VMs to a protection domain.
    #added_vms = testRestApi.addVMtoPD()
    #print("Text: ")
    #pp.pprint(added_vms)
    #print(("=" * 79))
    
    #Add specific VM(s) to a protection domain.
    specific_vm = testRestApi.specificVMtoPD()
    print("Text: ")
    pp.pprint(specific_vm)
    print(("=" * 79))
    
    print(("*" * 79))
    
    print("FINISHED")

  except Exception as ex:
    print(ex)
    sys.exit(1)