import requests

def post_to_energymeasures(jsondata):
    url = 'https://energymeasures-api.fly.dev/api/energymeter'
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=jsondata, headers=headers)
    if response.status_code != 201:
        print('Unable to post request to energymeasures')
    else:
        print('Data posted to energymeasures, status code: ' + str(response.status_code))