import http.client
import json
import polyline


from flask import Flask

app = Flask(__name__)


def doAllStravaStuff():
    conn = http.client.HTTPSConnection("www.strava.com")
    payload = ''
    headers = {
      'Authorization': 'Bearer 99e31cb7683695c133429b0397bec240d4535533'
    }
    conn.request("GET", "/api/v3/athlete/activities", payload, headers)
    res = conn.getresponse()
    data = res.read()

    str_data = data.decode("utf-8")
    resp_data_json = json.loads(str_data)
    # print(resp_data_json)
    mything = []
    for activity in resp_data_json:
        # print(activity)
        # print(activity['map'])

        polyl = polyline.decode(activity['map']['summary_polyline'])
        print(f'poly: {polyl}')
        mything = polyl
        #https://developers.google.com/maps/documentation/utilities/polylinealgorithm
        # print( str(activity['id'] ) + ' - ' + str(activity['name']) + ' - ' + str(activity['type']))
        # map': {'id': 'a6585569005', 'summary_polyline'
        break
        # conn.request("GET", f"/activities/{activity['id']}", payload, headers)
        # act_res = conn.getresponse()
        # act_data = act_res.read()
        #
        # str_act_data = act_data.decode("utf-8")
        # resp_actjson = json.loads(str_act_data)
    return mything


@app.route("/")
def hello_world():
    s = doAllStravaStuff()
    return f'<p>hello {s}</p>'

