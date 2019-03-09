#!/usr/local/bin/python3

import os
import time
import paho.mqtt.client as mqtt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("api_key")
symbols = os.getenv("stocks").split(",")
interval = int(os.getenv("interval"))
broker = os.getenv("broker")
port = os.getenv("port")
user = os.getenv("user")
password = os.getenv("password")


def getCurrentStockPrice(api_key, symbols):

	timeseries = TimeSeries(key=api_key)

	try:
		data = timeseries.get_batch_stock_quotes(symbols)
	except ValueError:
		print("API Key is not valid or symbols not known")
	
	return data

def on_publish(client,userdata,result):             
    pass

def publishToMqtt(symbol,price):
	paho= mqtt.Client("stock_monitor") 
	paho.username_pw_set(user, password=password)                           
	paho.on_publish = on_publish                         
	paho.connect(broker,1883)                                 
	ret= paho.publish("stock/{}/price".format(symbol),price) 
	paho.disconnect()

def main(interval):
	while True:
		data = getCurrentStockPrice(api_key, symbols)
		records = len(symbols)
		count = 0
		for s in data:
			while (count < records):
				publishToMqtt(s[count]['1. symbol'], s[count]['2. price'])
				count = count +1
		time.sleep(interval)

if __name__ == "__main__":
    main(interval)