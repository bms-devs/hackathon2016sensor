#!/usr/bin/python2
# vim: expandtab ts=4 sw=4
# Inspired by http://www.raspberrypi-spy.co.uk/2015/03/bh1750fvi-i2c-digital-light-intensity-sensor/


import sys
from bh1750 import *
import time
from time import gmtime, strftime
import requests
import logging
import traceback
from config import *


# working data
last_update_time = 0
last_entries = []

# configuration parameters
refresh_frequency = 30
measurement_frequency = 0.1
number_of_last_entries = 10
number_of_stable_entries = 6
threshold = 10
sensitivity = 200



def formatted_time():
    return strftime("[%Y-%m-%d %H:%M:%S] ", gmtime())


def should_update():
    global last_update_time, refresh_frequency
    current_time = time.time()
    return (current_time - last_update_time) > refresh_frequency


def send_update(occupied_state):
    global last_update_time, endpoint_url
    logging.warning(formatted_time() + "Sending status " + str(occupied_state) + " to " + endpoint_url)
    try:
        headers = {'Content-Type': 'text/plain'}
        response = requests.put(endpoint_url, data=str(occupied_state).lower(), auth=(endpoint_username, endpoint_password), headers=headers)
        if (response.status_code == 200):
            last_update_time = time.time()
        else:
            logging.warning(formatted_time() + "Network call failed, status code " + str(response.status_code))
    except:
        err = sys.exc_info()[0]
        logging.warning(formatted_time() + "Network call failed, exception " + str(err) + " " + traceback.format_exc())


def is_above_threshold(measurement):
    return (measurement > threshold)


def register_entry(above_threshold):
    global last_entries, number_of_last_entries
    last_entries.append(above_threshold)
    last_entries = last_entries[-number_of_last_entries:]


def determine_state():
    global last_entries, number_of_stable_entries
    if len(filter(lambda x: x == True, last_entries)) >= number_of_stable_entries:
        return True
    if len(filter(lambda x: x == False, last_entries)) >= number_of_stable_entries:
        return False
    return None



def main():
    global endpoint_url, sensitivity, refresh_rate, measurement_frequency, smbus_no

    logging.basicConfig(filename='light-sensor.log',level=logging.WARNING)

    #bus = smbus.SMBus(0) # Rev 1 Pi uses 0
    bus = smbus.SMBus(smbus_no)  # Rev 2 Pi uses 1
    sensor = BH1750(bus)
    sensor.set_sensitivity(sensitivity)

    last_state_sent = None

    while True:
        measurement = sensor.measure_low_res()
	#logging.warn(str(measurement))
        register_entry(is_above_threshold(measurement))
        current_state = determine_state()
        
        if (current_state is not None) and (current_state != last_state_sent): 
            send_update(current_state)
            last_state_sent = current_state

        if should_update() and (last_state_sent is not None):
            send_update(last_state_sent)

        time.sleep(measurement_frequency)


if __name__=="__main__":
    main()

