#!/usr/bin/env python3
###############################################################################
#   @author         :   Jeffrey Stone 
#   @date           :   03/08/2019
#   @script        	:   alpha_vantage_to_mqtt.py
#   @description    :   Script to grab stock prices from Alpha Vantage and publish them to MQTT to be consumed by another service
###############################################################################

import os
import time
import json
import sys
import paho.mqtt.client as mqtt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
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
http_event_collector_key = os.getenv("splunk_hec_key")
http_event_collector_host = os.getenv("splunk_host")
http_event_collector_ssl = os.getenv("splunk_hec_ssl")
http_event_collector_port = int(os.getenv("splunk_hec_port"))

# if splunk hec key set in .env load the splunk libraries
if http_event_collector_key:
	import json
	from splunk_http_event_collector import http_event_collector
	if http_event_collector_ssl == "False":
		http_event_collector_ssl = False
	else:
		http_event_collector_ssl = True

def getCurrentStockPrice(api_key, symbols):
	if app_mode == 'debug':
		print("Starting Alpha Vantage Call...\n")
	timeseries = TimeSeries(key=api_key)

	try:
		data = timeseries.get_batch_stock_quotes(symbols)
	except ValueError:
		if app_mode == 'debug':
			print("API Key is not valid or symbols not known")
	if app_mode == 'debug':
		print("Alpha Vantage Call Complete...\n")
	return data

def on_publish(client,userdata,result):             
    pass

def publishToMqtt(symbol,price):
	if app_mode == 'debug':
		print("Sending {} to MQTT...\n".format(symbol))
	paho= mqtt.Client("stock_monitor") 
	paho.username_pw_set(user, password=password)                           
	paho.on_publish = on_publish                         
	paho.connect(broker,port)                                 
	ret= paho.publish("stock/{}/price".format(symbol),price)
	if app_mode == 'debug':
		print("Published {} with price {} to MQTT...\n".format(symbol,price)) 
	paho.disconnect()

def splunkIt(records, symbols,total_elapsed_time, api_elapsed_time):
	if app_mode == 'debug':
		print("Time to Splunk It Yo...\n")
	logevent = http_event_collector(http_event_collector_key, http_event_collector_host, http_event_port = http_event_collector_port, http_event_server_ssl = http_event_collector_ssl)
	logevent.popNullFields = True

	payload = {}
	payload.update({"index":"homeassistant"})
	payload.update({"sourcetype":"alpha_vantage_mqtt"})
	payload.update({"source":"alpha_vantage_script"})
	payload.update({"host":"jarvis"})
	event = {}
	event.update({"action":"success"})
	event.update({"records":records})
	event.update({"total_elapsed_time":total_elapsed_time})
	event.update({"api_elapsed_time":api_elapsed_time})
	event.update({"stocks":"{}".format(symbols)})
	payload.update({"event":event})
	logevent.sendEvent(payload)
	logevent.flushBatch()
	if app_mode == 'debug':
		print("It has been Splunked...\n")


def main(interval):
	while True:
		if app_mode == 'debug':
			print("Starting Script...\n")
		start = time.time()
		data = getCurrentStockPrice(api_key, symbols)
		api_end_time = time.time()
		records = len(symbols)
		count = 0
		if app_mode == 'debug':
			print("Processing {} stocks...\n".format(records))
		for s in data:
			while (count < records):
				publishToMqtt(s[count]['1. symbol'], s[count]['2. price'])
				count = count +1
		end = time.time()
		api_call_time = (api_end_time - start)
		total_elapsed_time = (end - start)
		if http_event_collector_key:
			splunkIt(records,symbols,total_elapsed_time,api_call_time)
		if app_mode == 'debug':
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