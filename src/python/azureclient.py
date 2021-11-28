import requests
from python.queuemgmt import queueMeasure
import queuemgmt

def post_to_azure_read_info(jsonData):
    print(jsonData)
    url = 'https://func-priv114-em-ingress.azurewebsites.net/api/priv114_em_ingress?code=CdV2Ikqaoglj8jM2YDMxIZy6sZgodWcQVULJJmOvTvxh/lMRS/EWXw=='
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=jsonData, headers=headers)
    if response.status_code != 200:
        queueMeasure(jsonData)
        print('Unable to post request to azure. Measure has been added to the queue.')
    else:
        print('Data posted to Azure')
