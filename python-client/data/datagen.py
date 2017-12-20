#!/usr/bin/env python

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Python sample for connecting to Google Cloud IoT Core via MQTT, using JWT.
This example connects to Google Cloud IoT Core via MQTT, using a JWT for device
authentication. After connecting, by default the device publishes 100 messages
to the device's MQTT topic at a rate of one per second, and then exits.
Before you run the sample, you must follow the instructions in the README
for this sample.
"""

import argparse
import datetime
import time
import random
from random import randint
import json
import numpy as np

def main():
    i = 1
    items_removed = 0
    json_file = 'SampleData.json'
    fh = open(json_file, 'w')
    avail = {}

    while i <= 1000:
	data = {}
    	data['scanid'] = "scan" + str(i).rjust(6,'0')  # assigned uniquely for every scan
    	d = datetime.datetime.utcnow()  # time scanned
    	data['timestamp'] = d.isoformat("T") + "Z"
	event_type = ['Placed', 'Removed']
	event = np.random.choice(event_type, p=[0.7, 0.3])
	data['event'] = event
	
	if event == 'Placed':
	    data['upc'] = "A8000000" + str(randint(1, 50)).rjust(2,'0')  # Universal Product code (UPC)
            data['hub_device_id'] = "hub" + str(randint(0, 9)) # represents a hub positioned in the store
	    data['storeid'] = random.choice(['sfo-store-01', 'chi-store-02', 'nyc-store-03'])   # id of the store
	    # Mark the item as available for checkout
	    item = data['scanid']
	    avail['item'] = 1
	    print "Entry placed on the shelf = [%s, %s, %s]" % (data['upc'], data['hub_device_id'], data['storeid'])
	else:
            fr = open(json_file, 'r')
	    items_removed += 1
            num = sum(1 for line in fr)
	    if num <= 0:
		continue
       	    else:
		fr.seek(0,0)
            	for line in fr:
		    entry = json.loads(line)
		    # Check if the item is available for checkout
		    item = entry['scanid']
		    if avail['item'] == 0:   # Already checked out
			continue
		    else:                    # Available for checkout
                    	probability = random.random()
                    	if probability >= 0.5:    # Flip a coin to decide if this item should be removed
				data['upc'] = entry['upc']
            			data['hub_device_id'] = entry['hub_device_id']
            			data['storeid'] = entry['storeid']
				print "Entry removed from shelf = [%s, %s, %s]" % (data['upc'], data['hub_device_id'], data['storeid'])
                        	break
	    	fr.close()

	j = json.dumps(data)
        fh.write(j + '\n')
	i += 1
    	time.sleep(randint(0, 10))

    fh.close()
    print('Finished.')

if __name__ == '__main__':
    main()
