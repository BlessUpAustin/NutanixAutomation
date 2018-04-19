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
    
    #Creating REST client session for server connection, after globally setting
    #Authorization, content type, and character set for the session.
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

  #Delete the previously created protection domain. 
  #Change the URL to fit the desired domain.

  def protectionDomainCleanup(self):

    protectionDomainURL = self.base_url + "/protection_domains/testPD/"
    print ("Deleting a protection domain on cluster %s " % self.serverIpAddress)
    serverResponse = self.session.delete(protectionDomainURL)
    print ("Response code: %s" % serverResponse.status_code)
    return json.loads(serverResponse.text)

if __name__ == "__main__":

    try:
      
      pp = pprint.PrettyPrinter(indent=2)

      testRestApi = TestRestApi()
      print(("=" * 79))
      status, cluster = testRestApi.getClusterInformation()
      print(("=" * 79))

      #Get specific cluster elements.
      print("Name: %s" % cluster.get('name'))
      print("ID: %s" % cluster.get('id'))
      print("Cluster External IP Address: %s" % cluster.get('clusterExternalIPAddress'))
      print("Number of Nodes: %s" % cluster.get('numNodes'))
      print("Version: %s" % cluster.get('version'))
      print("Hypervisor Types: %s" % cluster.get('hypervisorTypes'))
      print(("=" * 79))

      #Delete a protection domain
      deleteProtectionDomain = testRestApi.protectionDomainCleanup()
      print ("Text: ")
      pp.pprint(deleteProtectionDomain)
      print (("=" * 79))

    except Exception as ex:
      print (ex)
      sys.exit(1)