#! /usr/bin/env python

import sys
import argparse
import httplib
from urlparse import urlparse

parser = argparse.ArgumentParser(description='Monitor URL for expected response code. Accepts both http and https.')
parser.add_argument('url', help='URL to check. IE http(s)://<url>:<port>/<path>')
parser.add_argument('timeout', help='Time to wait for the response')
parser.add_argument('expected_response_code', help='The response code to expect back from the URL')
parser.add_argument('retry_count', help='The number of times to retry the check')
args = parser.parse_args()

def url_check(url):
    """
       Takes parsed URL and calls the appropriate connector and does the request until
       successful return or hits the retry limit. Returns 0 if successful status code
       is returned or non-zero response otherwise.
    """
    count = 0
    success = False
    while count < int(args.retry_count) :
      if url.scheme == 'http':
        conn = httplib.HTTPConnection(url.netloc, timeout=float(args.timeout))
      else:
        conn = httplib.HTTPSConnection(url.netloc, timeout=float(args.timeout))
      try:
        conn.request("GET", url.path)
        response = conn.getresponse()
        success = True
        break
      except:
        count += 1

    if count < args.retry_count and success :
      if str(response.status) == args.expected_response_code:
        sys.exit()
    else :
      sys.stderr.write('Timeout occurred and retry count hit.\n')
    sys.exit(-1)

if __name__ == "__main__" :
    url = urlparse(args.url)
    url_check(url)
