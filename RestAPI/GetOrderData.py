# Assumptions: python code to access a web commerce Platform, order database is in the backend  and will be accessed through a REST API
# Authentication will be through a Bearer Token. We get from the API JSON data that we will load into a python dictionary

import sys
#import argparse
import json
import requests
import logging

api_token = 'your_api_token'
api_url_base = 'https://api.webpage.com/v3'

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer ' + api_token}
		   
logging.basicConfig(filename="getOrderData.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("Running Script to obtain Order Data")
		   
#parser = argparse.ArgumentParser(description="Insert your Order ID")
#parser.add_argument("orderid", help= "order ID")		
#args = parser.parse_args()
#orderid= args.orderid
orderid = input("To track your order we need your Order ID. What's your Order ID? ")
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






