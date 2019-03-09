# Alpha Vantage to MQTT

This script was written to provide stock price to a MQTT sensor in the [HomeAssistant](https://home-assistant.io) home automation platform. Unfortunately the built in Alpha Vantage componet fails if you have more than 1 or 2 stocks that you want to follow. It also allows you to offload the script to another system to save your [HomeAssistant](https://home-assistant.io) resources from non-mission critical functions.

## Requirements
* You will need the ability to execute this script.
* You will need a MQTT sever that you can publish to.
* You will need a Alpha Vantage API key which is free. Sign up at [https://www.alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)

## Installation
* Install the app by cloning this repo
 - `git clone https://github.com/thejeffreystone/alpha_vantage_to_mqtt.git`
* Install the required python libraries:
 - `pip install paho-mqtt`
 - `pip install alpha_vantage`
 - `pip install python-dotenv`
* Edit the env-sample and saved as .env

## Run

This script is meant to run with something like supervisord, but can be executed manually and will stay running until killed. 

## Features
* This script publishes stock price to topic `stock/<stock_name>/price`
* This script utilizes the `get_batch_stock_quotes` method of the Alpha Vantage API to reduce the number of calls to the API to avoid hitting the API more than once a second.
* This script is built to run continiously and will pause for the interval set in the `.env` file.  

## Compaitbility

This script was written and tested using python 3.7.2


