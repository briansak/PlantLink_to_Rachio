import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth
import json
import time

def main():
   storedCredentials = False

# Replace the username and password field with your PlantLink authentication credentials.

username = ''
password = ''
plantLinkAPI = 'https://dashboard.myplantlink.com/api/v1/plants'

plantLinkAPICall = requests.get(
url = plantLinkAPI,
auth = HTTPBasicAuth(username,password),
verify=False)

#Pull "Plant_Fuel_Level from PlantLink API.  This is a value between 0 and 1 and the support team mentioned that if the value is lower than 0.2, the plant should be watered.

parse = json.loads(plantLinkAPICall.content)
moisture = parse[0]["last_measurements"][0]["plant_fuel_level"]

print "Current Moisture Level: " + str(moisture)

if moisture <= 0.2:
   
   #Change the auth_token with the value from the API Access Token field from the Rachio Web Dashboard
   auth_token = ''

   #Change this to the value obtained under the zone you'd like to trigger if the PlantLink reports watering is needed.
   zone_id = ''

   #Duration that you'd like to run the zone for to water the impacted plant (in minutes).
   duration = 20
   
   iroStartZoneAPI = 'https://api.rach.io/1/public/zone/start'
   startZone = requests.put(
      url = iroStartZoneAPI,
      headers = {"Content-Type":"application/json","Authorization":"Bearer " + auth_token},
      data = "{id : " + zone_id + ", duration : " + str(duration) + " }",
      verify = False)

   print (startZone.text)
