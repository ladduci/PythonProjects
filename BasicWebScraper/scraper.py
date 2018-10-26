import os
import logging
import argparse
import requests
import shutil
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Test Web Scraper")

parser.add_argument("inputURL", metavar="BaseURL", help="URL of the Website we want to scrape")
parser.add_argument("downloadDir",metavar="Dir", help="Download Directory")
args = parser.parse_args()

base_url = args.inputURL
download_directory= args.downloadDir

logging.basicConfig(filename="scraper.log",format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)
logging.info("The test Web scraper is now running")
to_visit = set((base_url,))
visited = set()

while to_visit:
     #Pick a link to visit.
	 #Visit the link.
	 current_page = to_visit.pop()
	 print("visiting:", current_page)
	 logging.info("visiting: %s" % current_page)
	 visited.add(current_page)
	 content = urllib.request.urlopen(current_page).read()
     
     # Extract any new links from that page.
	 for link in BeautifulSoup(content, "lxml").findAll("a"):
	     absolute_link = urljoin(current_page, link["href"])
		 if absolute_link not in visited:
		 to_visit.add(absolute_link)
		 else:
		     print("Already visited:", absolute_link)
			logging.info("Already visited:%s" % absolute_link)
			 
     # Download any images on the page.
	 for img in BeautifulSoup(content, "lxml").findAll("img"):
	      img_href = urljoin(current_page, img["src"]
		  print("Downloading image", img_href)
		  logging.info("Downloading image%s" % img_href))
		  img_name = img_href.split("/")[-1]
		  urllib.request.urlretrieve(img_href, os.path.join(download_directory, img_name))
		  img_size = int(requests.head(img_href).headers['Content-length'])
          logging.debug('File size is %s' % img_size)