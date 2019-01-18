import os
import logging
import argparse
import requests
import shutil
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Test Web Scraper")
parser.add_argument("inputURL", metavar="BaseURL", help="URL of the Website we want to scrape for pictures")
parser.add_argument("downloadDir",metavar="Dir", help="Download Directory")
args = parser.parse_args()
base_url = args.inputURL
download_directory= args.downloadDir
# create logger with 'web_scraper'
logger = logging.getLogger('web_scraper')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('scraper.log')
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

#function to download a file from a URL with the capability  to resume the download if interrupted
#########################################################################################################
def download_with_resume(url, file_path, hash=None, timeout=10):
    """
    Performs a HTTP(S) download that can be restarted if prematurely terminated.
    The HTTP server must support byte ranges.
 
    :param file_path: the path to the file to write to disk
    :type file_path:  string
    :param hash: hash value for file validation
    :type hash:  string (MD5 hash value)
    """
     # don't download if the file exists
    if os.path.exists(file_path):
        return
    block_size = 1000 * 1000 # 1MB
    tmp_file_path = file_path + '.part'
    first_byte = os.path.getsize(tmp_file_path) if os.path.exists(tmp_file_path) else 0
    file_mode = 'ab' if first_byte else 'wb'
    logger.debug('Starting download at %.1fMB' % (first_byte / 1e6))
    file_size = -1
    try:
        file_size = int(requests.head(url).headers['Content-length'])
        logger.debug('File size is %s' % file_size)
        headers = {"Range": "bytes=%s-" % first_byte}
        r = requests.get(url, headers=headers, stream=True)
        with open(tmp_file_path, file_mode) as f:
            for chunk in r.iter_content(chunk_size=block_size): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    except IOError as e:
        logger.debug('IO Error - %s' % e)
    finally:
        # rename the temp download file to the correct name if fully downloaded
        if file_size == os.path.getsize(tmp_file_path):
            # if there's a hash value, validate the file
            if hash and not validate_file(tmp_file_path, hash):
                raise Exception('Error validating the file against its MD5 hash')
            shutil.move(tmp_file_path, file_path)
        elif file_size == -1:
raise Exception('Error getting Content-Length from server: %s' % url)

#########################################################################################
#Now starts the scraper

logger.info("The test Web scraper is now running")
logger.info("(requests.get(base_url)).status_code)
to_visit = set((base_url,))
visited = set()

while to_visit:
     #Pick a link to visit.
	 #Visit the link.
	 current_page = to_visit.pop()
	 logger.info("visiting: %s" % current_page)
	 visited.add(current_page)
	 content = urllib.request.urlopen(current_page).read()
     
     # Extract any new links from that page.
	 for link in BeautifulSoup(content, "lxml").findAll("a"):
	     absolute_link = urljoin(current_page, link["href"])
		 if absolute_link not in visited:
		 to_visit.add(absolute_link)
		 else:
			logger.info("Already visited:%s" % absolute_link)
			 
     # Download any images on the page.
	 for img in BeautifulSoup(content, "lxml").findAll("img"):
	      img_href = urljoin(current_page, img["src"]
		  img_size = int(requests.head(img_href).headers['Content-length'])
          logger.debug("File size is %s" % img_size)
		  img_name = img_href.split("/")[-1]
		  
#		  urllib.request.urlretrieve(img_href, os.path.join(download_directory, img_name))
          logger.info("Downloading image%s" % img_href))
          download_with_resume(img_href, os.path.join(download_directory, img_name), hash=None, timeout=10)
		 
		 
