#!/usr/bin/env python3
#
# Retrieves status data from a SB8200/PM8200 modem and prints relevant data to stdout
#
# This was developed in July 2020 using a SB8200 on Comcast/Xfinity consumer 1g/40m service
#
# The firmware version at the start of development is AB01.01.009.32.01_122319_183.0A.NSH
#
# Future Comcast/Xfinity firmware revisions may result in this script failing to operate due
# to changes in HTTP accessibility or raw HTML returned by HTTP requests
#
# Useful device info: http://en.techinfodepot.shoutwiki.com/wiki/Arris_CM8200
#                     http://en.techinfodepot.shoutwiki.com/wiki/Arris_SB8200
#                     https://github.com/net-wayfarer/Arris-CM8200B-Reverse-Engineering
#
# Todo: Dump and unpack flash to look at the filesystem and see if there are more pages accessible

import requests
import re
import json
from bs4 import BeautifulSoup

# Get HTML and Store Relevant Request Metadata
data_requests = {}

# Get connection status HTML and handle errors
try:
    resp = requests.get("http://192.168.100.1/cmconnectionstatus.html")
except Exception as exception:
    print("Error with request, %s", exception)
    quit()

if resp.status_code != 200:
    print("Error code from request, %s", resp.status_code)
    quit()

# Decode response, store metadata, close response
status_html = resp.content.decode("utf-8")
data_requests['connectionstatus'] = {}
data_requests['connectionstatus']['response_microseconds'] = resp.elapsed.microseconds
data_requests['connectionstatus']['response_length'] = len(resp.content)
resp.close()

# Get connection status HTML and handle errors
try:
    resp = requests.get("http://192.168.100.1/cmswinfo.html")
except Exception as exception:
    print("Error with request, %s", exception)
    quit()

if resp.status_code != 200:
    print("Error code from request, %s", resp.status_code)
    quit()

# Decode response, store metadata, close response
info_html = resp.content.decode("utf-8")
data_requests['swinfo'] = {}
data_requests['swinfo']['response_microseconds'] = resp.elapsed.microseconds
data_requests['swinfo']['response_length'] = len(resp.content)
resp.close()

# Fix connectionstatus page HTML, if required
# There are some tr tags missing around some table headers, leading to parse issues
# Since there appear to be two variations of this out there we'll look for either case
status_html = status_html.replace("Bonded Channels</strong></th>\n", "Bonded Channels</strong></th></tr>\n<tr>", 2)
status_html = status_html.replace("Bonded Channels</strong></th></tr>\n", "Bonded Channels</strong></th></tr>\n<tr>", 2)
# As of at least mid-2020 there are some problems with strong tags that lead to parse issues
status_html = re.sub(r'<(/|)(strong)>', "", status_html, flags=re.IGNORECASE)

# Parse key top-level tables from status page
status_soup = BeautifulSoup(status_html, "html.parser")
table_startup = status_soup.find_all("table")[0]
table_downstream = status_soup.find_all("table")[1]
table_upstream = status_soup.find_all("table")[2]

info_soup = BeautifulSoup(info_html, 'html.parser')
table_info = info_soup.find_all("table")[0]
table_status = info_soup.find_all("table")[1]

# Parse startup table data
# Rows to look for in the startup table
rows_status = {
    'Acquire Downstream Channel': 'acquire_downstream_channel',
    'Connectivity State': 'connectivity_state',
    'Boot State': 'boot_state',
    'Configuration File': 'config_file_state',
    'Security': 'security_state',
    'DOCSIS Network Access Enabled': 'docsis_state',
    'Software Version': 'firmware_version'
}

data_status = {}
for row in table_startup.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) == 3 and cells[0].text in rows_status:
        field_descriptor = cells[0].text
        field_name = rows_status[field_descriptor]
        field_data = cells[1].text
        data_status[field_name] = field_data
        if field_descriptor == 'Acquire Downstream Channel':
            data_status['acquire_downstream_channel_state'] = cells[2].text
        if field_descriptor == 'Connectivity State':
            data_status['connectivity_state_comment'] = cells[2].text
        if field_descriptor == 'Boot State':
            data_status['boot_state_comment'] = cells[2].text
        if field_descriptor == 'Security':
            data_status['security_specification'] = cells[2].text

for row in table_info.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) == 2 and cells[0].text in rows_status:
        field_descriptor = cells[0].text
        field_name = rows_status[field_descriptor]
        field_data = cells[1].text
        data_status[field_name] = field_data

# Parse Downstream Channel Data
data_downstream = {}
for row in table_downstream.find_all("tr")[2:]:
    cells = row.find_all("td")
    if len(cells) == 8:
        channel_id = cells[0].text
        data_downstream[channel_id] = {
            'lock_status': cells[1].text,
            'modulation': cells[2].text,
            'frequency': cells[3].text,
            'power': cells[4].text,
            'snr': cells[5].text,
            'corrected': cells[6].text,
            'uncorrectable': cells[7].text
        }

# Parse Upstream Channel Data
data_upstream = {}
for row in table_upstream.find_all("tr")[2:]:
    cells = row.find_all("td")
    if len(cells) == 7:
        channel_id = cells[1].text
        data_upstream[channel_id] = {
            'channel': cells[0].text,
            'lock_status': cells[2].text,
            'us_chanel_type': cells[3].text,
            'frequency': cells[4].text,
            'width': cells[5].text,
            'power': cells[6].text
        }

output_data = {
    'requests': data_requests,
    'status': data_status,
    'downstream': data_downstream,
    'upstream': data_upstream}

print(json.dumps(output_data))
