# PM8200/CM8200 Telegraf Script

This script retrieves status data from a PM8200/CM8200 cable modem and returns JSON data via stdout that can be easily parsed by Telegraf.

## Requirements

* Python 3
* `requests`
* `bs4`

## FAQ

Q: This doesn't work for me, why?
A: Like all cable modems, the PM8200/CM8200 can (and almost always will) have its firmware overwritten by the network provider. This can cause problems ranging from total loss of access via HTTP/HTTPS to modified/malformed HTML pages. This script was originally developed using a PM8200 attached to a consumer Comcast/Xfinity connection in July 2020, running firmware version `AB01.01.009.32.01_122319_183.0A.NSH`.

Q: I don't see any argument handling, error handling, or even methods/classes broken out, what gives?
A: This was originally written quickly, over a few hours of curiosity induced research, which led to a "do it fast, keep it simple" approach.

Q: Why not just use SNMP?
A: While the Arris/Broadcomm firmware does support the use of SNMP, it looks like most (if not all) ISPs have disabled it via firmware updates. That's why we've gotta scrape.

Q: Scraping is ridiculous, why scrape HTML?
A: As of July 2020, scraping HTML is the only way to get information on this device. Thankfully the `bs4`/`BeautifulSoup` project makes scraping table data almost trivial. Which is good, since this is pretty much all table data.

## Overview

This script is intended to be used with a Telegraf agent running on a system that can reach the cable modem at `192.168.100.1`. However, any system that executes a script and pulls in JSON data from `stdout` may work fine for this.

Configuring Telegraf to make use of the output data is left as an exercise for the reader/cloner. :)

## Example Output

```json
{
  "requests": {
    "connectionstatus": {
      "response_microseconds": 104752,
      "response_length": 13029
    },
    "swinfo": {
      "response_microseconds": 55178,
      "response_length": 3907
    }
  },
  "status": {
    "acquire_downstream_channel": "501000000 Hz",
    "acquire_downstream_channel_state": "Locked",
    "connectivity_state": "OK",
    "connectivity_state_comment": "Operational",
    "boot_state": "OK",
    "boot_state_comment": "Operational",
    "config_file_state": "OK",
    "security_state": "Enabled",
    "security_specification": "BPI+",
    "docsis_state": "Allowed",
    "firmware_version": "AB01.01.009.32.01_122319_183.0A.NSH"
  },
  "downstream": {
    "13": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "501000000 Hz",
      "power": "-6.3 dBmV",
      "snr": "41.3 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "1": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "423000000 Hz",
      "power": "-5.4 dBmV",
      "snr": "42.2 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "2": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "435000000 Hz",
      "power": "-5.9 dBmV",
      "snr": "41.9 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "3": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "441000000 Hz",
      "power": "-6.9 dBmV",
      "snr": "41.5 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "4": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "447000000 Hz",
      "power": "-7.3 dBmV",
      "snr": "41.3 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "5": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "453000000 Hz",
      "power": "-6.9 dBmV",
      "snr": "41.2 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "6": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "459000000 Hz",
      "power": "-6.1 dBmV",
      "snr": "41.4 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "7": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "465000000 Hz",
      "power": "-6.1 dBmV",
      "snr": "41.1 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "8": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "471000000 Hz",
      "power": "-6.0 dBmV",
      "snr": "40.8 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "9": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "477000000 Hz",
      "power": "-5.8 dBmV",
      "snr": "40.1 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "10": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "483000000 Hz",
      "power": "-5.6 dBmV",
      "snr": "41.6 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "11": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "489000000 Hz",
      "power": "-5.8 dBmV",
      "snr": "41.5 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "12": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "495000000 Hz",
      "power": "-6.6 dBmV",
      "snr": "41.1 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "14": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "507000000 Hz",
      "power": "-7.1 dBmV",
      "snr": "40.8 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "15": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "513000000 Hz",
      "power": "-7.2 dBmV",
      "snr": "40.7 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "16": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "519000000 Hz",
      "power": "-7.2 dBmV",
      "snr": "40.1 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "17": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "525000000 Hz",
      "power": "-9.9 dBmV",
      "snr": "38.8 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "18": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "531000000 Hz",
      "power": "-9.1 dBmV",
      "snr": "39.5 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "19": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "537000000 Hz",
      "power": "-7.4 dBmV",
      "snr": "40.0 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "20": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "543000000 Hz",
      "power": "-7.0 dBmV",
      "snr": "40.6 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "21": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "549000000 Hz",
      "power": "-6.9 dBmV",
      "snr": "40.6 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "22": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "555000000 Hz",
      "power": "-7.6 dBmV",
      "snr": "40.2 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "23": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "561000000 Hz",
      "power": "-7.5 dBmV",
      "snr": "39.5 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "24": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "567000000 Hz",
      "power": "-7.6 dBmV",
      "snr": "40.0 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "25": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "573000000 Hz",
      "power": "-8.1 dBmV",
      "snr": "39.7 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "26": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "579000000 Hz",
      "power": "-7.6 dBmV",
      "snr": "39.9 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "27": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "585000000 Hz",
      "power": "-7.7 dBmV",
      "snr": "39.7 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "28": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "591000000 Hz",
      "power": "-7.4 dBmV",
      "snr": "39.9 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "29": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "597000000 Hz",
      "power": "-7.1 dBmV",
      "snr": "40.0 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "30": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "603000000 Hz",
      "power": "-8.3 dBmV",
      "snr": "39.6 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "31": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "609000000 Hz",
      "power": "-8.1 dBmV",
      "snr": "39.4 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "32": {
      "lock_status": "Locked",
      "modulation": "QAM256",
      "frequency": "615000000 Hz",
      "power": "-8.6 dBmV",
      "snr": "38.7 dB",
      "corrected": "0",
      "uncorrectable": "0"
    },
    "159": {
      "lock_status": "Locked",
      "modulation": "Other",
      "frequency": "690000000 Hz",
      "power": "-9.0 dBmV",
      "snr": "35.8 dB",
      "corrected": "2087222887",
      "uncorrectable": "0"
    }
  },
  "upstream": {
    "3": {
      "channel": "1",
      "lock_status": "Locked",
      "us_chanel_type": "SC-QAM Upstream",
      "frequency": "25000000 Hz",
      "width": "6400000 Hz",
      "power": "50.0 dBmV"
    },
    "1": {
      "channel": "2",
      "lock_status": "Locked",
      "us_chanel_type": "SC-QAM Upstream",
      "frequency": "37800000 Hz",
      "width": "6400000 Hz",
      "power": "50.0 dBmV"
    },
    "2": {
      "channel": "3",
      "lock_status": "Locked",
      "us_chanel_type": "SC-QAM Upstream",
      "frequency": "31400000 Hz",
      "width": "6400000 Hz",
      "power": "51.0 dBmV"
    },
    "4": {
      "channel": "4",
      "lock_status": "Locked",
      "us_chanel_type": "SC-QAM Upstream",
      "frequency": "18600000 Hz",
      "width": "6400000 Hz",
      "power": "50.0 dBmV"
    }
  }
}
```

## To Do

* Critical: Finalize JSON data structure and write Telegraf config to handle ingesting it
* Important: Build a Grafana dashboard to make the data look fancy
* Could Be Fun: Dump and unpack the modem firmware to see if there's other low-level status info available via HTTP without modifications