# Assumptions: python code to access a web commerce Platform order database through its REST API.
# Authentication will be through a Bearer Token. We get from the API JSON data that we will load into a python dictionary

import sys
import argparse
import json
import requests
import logging
parser = argparse.ArgumentParser(description="Script to access order data in a web commerce platform through a REST API")
parser.add_argument("api_url_base",metavar="API_url_base", help="REST API url base ") #the base URL of the REST API
parser.add_argument("api_token",metavar="APIToken", help="Bearer Token to acces the REST API") #Bearer Token to acces the REST API
parser.add_argument("orderid", help= "order ID")
args = parser.parse_args()
		

orderid= args.orderid
api_token = args.api_url_base
api_url_base = args.api_token #### for example 'https://api.webpage.com/v3'
#build the header to gain access to the REST API with the Bearer Token
headerAPI = {'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + api_token}
		   

# create logger with 'Get Order data from REST API'
logger = logging.getLogger('Get Order data from REST API')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('getOrder.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info("Running Script to obtain Order Data")
		   

def get_order_status(orderid)
   api_url = '{0}orders/orderid/status'.format(api_url_base)
   response = requests.get(api_url, headers=headers)
   #This code handles six different error conditions by looking at the HTTP status code in the response.
   #A code of 500 or greater indicates a problem on the server. These should be rare, and they are not caused by problems with the request, so I print only the status code.
   #A code of 404 means "not found," which probably stems from a typo in the URL. For this error, I print the status code and the URL that led to it so you can see why it failed.
   #A code of 401 means the authentication failed. The most likely cause for this is an incorrect or missing api_key.
   #A code in the 300 range indicates a redirect. 
   #A code of 200 means the request was processed successfully. For this, we don't print anything. I just return the order status  as a JSON object
   #If the response code was anything else I print the status code as an "unexpected error."

   if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
		logging.error("Server Error.format(response.status_code)%s")
        return None
     elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
		logging.info("URL not found: '.format(response.status_code, ,api_url)%s")
        return None  
     elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
		logging.error("Authentication Failed'.format(response.status_code)%s")
        return None
    elif response.status_code == 400:
         print('[!] [{0}] Bad Request'.format(response.status_code))
		logging.error("Bad Request'.format(response.status_code)%s")
        return None
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
		logging.error("Unexpected Redirect'.format(response.status_code)%s")
        return None
    elif response.status_code == 200:
        order_status = json.loads(response.content.decode('utf-8'))
        return order_status
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
		logging.error("Unexpected Error'.format(response.status_code, response.content)%s")
    return None

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
		
order_status = get_order_status(orderid)
if order_status is not None:
    if order_status[status] == 'shipped'
       print("Great news your order was shipped on the: ")
       print('{0}'.format(order_status['dateShipped']))
	   print("And it should arrive on: ")
	   print('{0}'.format(order_status['dateArrived']))

else:
    print('[!] Your order number is incorrect')






