#!/usr/bin/env python3
"""
Publish Alpha Vantage to MQTT.

Script to grab stock prices from Alpha Vantage and
publish them to MQTT to be consumed by another service.
"""

import os
import time
import sys
import paho.mqtt.client as mqtt
from alpha_vantage.timeseries import TimeSeries
from concurrent.futures.thread import ThreadPoolExecutor
from dotenv import load_dotenv
load_dotenv()

app_mode = os.getenv("app_mode")
api_key = os.getenv("api_key")
symbols = os.getenv("stocks").split(",")
interval = int(os.getenv("interval"))
broker = os.getenv("broker")
port = int(os.getenv("port"))
user = os.getenv("user")
password = os.getenv("password")

def getCurrentStockPrice(api_key, symbols):
    """Get Current Stock Price for a list of symbols."""
    if app_mode == 'debug':
        print("Starting Alpha Vantage Call...\n")
    timeseries = TimeSeries(key=api_key)

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            generator = executor.map(lambda stock:timeseries.get_quote_endpoint(symbol=stock), symbols)
        for data in generator:
            # Lets publish this to MQTT....
            publishToMqtt(data[0]['01. symbol'], data[0]['05. price'])
            if app_mode == 'debug':
                print("{} - {}".format(data[0]['01. symbol'],data[0]['05. price']))
    except ValueError:
        if app_mode == 'debug':
            print("API Key is not valid or symbols not known")
    if app_mode == 'debug':
        print("Alpha Vantage Call Complete...\n")
    return data

def on_publish(client, userdata, result):
    """Pass publish."""
    pass

def publishToMqtt(symbol, price):
    """Publish stock info to MQTT."""
    if app_mode == 'debug':
        print("Sending {} to MQTT...\n".format(symbol))
    paho = mqtt.Client("stock_monitor")
    paho.username_pw_set(user, password=password)
    paho.on_publish = on_publish
    paho.connect(broker, port)
    paho.publish("stock/{}/price".format(symbol), price)
    if app_mode == 'debug':
        print("Published {} with price {} to MQTT...\n".format(symbol, price))
    paho.disconnect()

def main(interval):
    """Start The Main Show."""
    while True:
        if app_mode == 'debug':
            print("Starting Script...\n")
        start = time.time()
        result = getCurrentStockPrice(api_key, symbols)
        api_end_time = time.time()
        records = len(symbols)
        if app_mode == 'debug' and result:
            print("Processed {} stocks...\n".format(records))

        end = time.time()
        api_call_time = (api_end_time - start)
        total_elapsed_time = (end - start)
        if app_mode == 'debug' and result:
            print("Script Completed...")
        if interval > 0:
            print("Time to sleep for {} seconds\n".format(interval))
            time.sleep(interval)
        else:
            if app_mode == 'debug':
                print("No Interval set...exiting...\n")
            sys.exit()


if __name__ == "__main__":
    main(interval)
