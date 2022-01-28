import http.client
import json
import polyline
import time
from flask import Flask

app = Flask(__name__)

# submit a request for a new token
def refeshToken(refreshToken):
    with open("clientInfo.json", "r")as f:  # Use file to refer to the file object
        client_info = json.loads(f.read())
        client_id = client_info['client_id']
        client_secret = client_info['client_secret']

        conn = http.client.HTTPSConnection("www.strava.com")

        requestStr = f'/api/v3/oauth/token?grant_type=refresh_token&refresh_token={refreshToken}&client_id={client_id}&client_secret={client_secret}'
        print(requestStr)
        conn.request("POST",requestStr)# , payload, headers)
        res = conn.getresponse()
        data = res.read()
        str_data = data.decode("utf-8")
        print(str_data)
        json_data = json.loads(str_data)
        new_token = {'access_token': json_data['access_token'],
                     'expires_at': json_data['expires_at'],
                     'refresh_token': json_data['refresh_token'],
                     'expires_in': json_data['refresh_token']}
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
from datetime import datetime, timedelta
# loads a strava access token then hits the activities endpoint
# next it grabs the reported list of recorded points then
# reverses lat/lon so that they can be shown correctly in
# geo json format and returns a list of lists (each list is a lat lon coords)
def doAllStravaStuff():
    token = loadTokens()
    # print(f'token: {token}')
    conn = http.client.HTTPSConnection("www.strava.com")
    payload = ''
    headers = { f'Authorization': f'Bearer {token}'  }
    two_weeks_ago = datetime.now() - timedelta(weeks=2)
    per_page = 100
    req_str = f'/api/v3/athlete/activities?after={two_weeks_ago.timestamp()}&per_page={per_page}'
    print(req_str)
    conn.request("GET", req_str, payload, headers)
    res = conn.getresponse()
    data = res.read()

    str_data = data.decode("utf-8")
    resp_data_json = json.loads(str_data)
    print(f'rcvd activity count: {len(resp_data_json)}')
    revdroutes = []

    for activity in resp_data_json:
        #only care about dog "walks"
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

#meant to be the 'home' page
@app.route("/")
def indexFunc():
    token = loadTokens()
    f = open("mapIndex.html", "r")
    return f.read()

