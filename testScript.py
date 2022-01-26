import http.client
import json

conn = http.client.HTTPSConnection("www.strava.com")
payload = ''
headers = {
  'Authorization': 'Bearer 9b8412bcb3be47dca11818cd2b9a06a5b2b20ebf'
}
conn.request("GET", "/api/v3/athlete/activities", payload, headers)
res = conn.getresponse()
data = res.read()

str_data = data.decode("utf-8")
resp_data_json = json.loads(str_data)
for activity in resp_data_json:
    print(str(activity['id']) + ' - ' + str(activity['name']) + ' - ' + str(activity['type']))
