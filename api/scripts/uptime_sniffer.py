#!/usr/bin/env python

# How to use: ./uptime_sniffer.py www.somesite.dom

import sys
import time
import timeit
import urllib3

url = sys.argv[1]
start = 0
end = 0
http = urllib3.PoolManager()
fetchedContent = http.request('GET', url)
start = timeit.timeit()
print(start)
page = fetchedContent.read()
end = timeit.timeit()
print(end)
fetchedContent.close()

print("Time consumed :", end - start)
