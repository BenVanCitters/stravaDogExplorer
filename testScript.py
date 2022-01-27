
import http.client
import json
import polyline
import time
from flask import Flask

app = Flask(__name__)

# submit a request for a new token
def refeshToken(refreshToken):

    f = open("clientInfo.json", "r")
    client_info = json.loads(f.read())
    client_id = client_info['client_id']
    client_secret = client_info['client_secret']

    conn = http.client.HTTPSConnection("www.strava.com")
    payload = ''
    headers = ''
    conn.request("POST", f'/api/v3/oauth/token?grant_type=authorization_code&grant_type=refresh_token&refresh_token={refreshToken}&client_id={client_id}&client_secret={client_secret}&', payload, headers)
    res = conn.getresponse()
    data = res.read()
    str_data = data.decode("utf-8")

    new_token = {'access_token': str_data['access_token'],
                 'expires_at': str_data['expires_at'],
                 'refresh_token': str_data['refresh_token'],
                 'expires_in': str_data['refresh_token']}
    # save the data
    f = open("tokens.txt", "w")
    f.write(json.dumps(new_token))
    f.close()

def loadTokens():
    f = open("tokens.txt", "r")
    token_json = json.loads(f.read())
    expirationTime = token_json['expires_at']
    accessToken = token_json['access_token']
    myrefreshToken = token_json['refresh_token']

    print(f'expirationTime: {expirationTime}')
    now = int(time.time())
    print(f'now: {now}')

    needsRefresh = (expirationTime < now)

    print(f'needsRefresh: {needsRefresh}')
    if needsRefresh:
        refeshToken(myrefreshToken)
    return accessToken


def doAllStravaStuff():
    token = loadTokens()
    # print(f'token: {token}')
    conn = http.client.HTTPSConnection("www.strava.com")
    payload = ''
    headers = { f'Authorization': f'Bearer {token}'  }
    conn.request("GET", "/api/v3/athlete/activities", payload, headers)
    res = conn.getresponse()
    data = res.read()

    str_data = data.decode("utf-8")
    resp_data_json = json.loads(str_data)
    # print(resp_data_json)
    revdroutes = []

    for activity in resp_data_json:
        if (activity['type'] == "Walk"):
            #https://developers.google.com/maps/documentation/utilities/polylinealgorithm
            polyl = polyline.decode(activity['map']['summary_polyline'])
            revdRoute = []
            for point in polyl:
                # gotta reverse the lat log for geo json purpose
                pt = [point[1],point[0]]
                revdRoute.append(pt)
            revdroutes.append(revdRoute)

    return revdroutes

#api endpoint for the getting routes
@app.route("/getmap")
def getMap():
    return str(doAllStravaStuff())

@app.route("/")
def indexFunc():
    token = loadTokens()
    print(token)
    f = open("mapIndex.html", "r")
    return f.read()

