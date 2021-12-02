import logging
from os import system
import requests
import queuemgmt


def post_to_azure_read_info(jsonData):
    logging.info(jsonData)
    url = 'https://func-priv114-em-ingress.azurewebsites.net/api/priv114_em_ingress?code=CdV2Ikqaoglj8jM2YDMxIZy6sZgodWcQVULJJmOvTvxh/lMRS/EWXw=='
    headers = {'Content-type': 'application/json'}

    try:
        response = requests.post(url, data=jsonData, headers=headers)
        if response.status_code != 200:
            queuemgmt.queue_measure(jsonData)
            logging.error('Unable to post request to azure. Responded: ' +
                          response.status_code+' Measure has been added to the queue.')
        else:
            logging.info(len(jsonData)+' chars data posted to Azure')
    except:
        logging.error('An exception has occured: '+sys.exc_info()[1])
