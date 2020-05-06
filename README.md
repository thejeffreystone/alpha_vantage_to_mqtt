# Alpha Vantage to MQTT

This script was written to provide stock price to a MQTT sensor in the [HomeAssistant](https://home-assistant.io) home automation platform. Unfortunately the built in Alpha Vantage componet fails if you have more than 1 or 2 stocks that you want to follow. And this script also allows you to offload the sensor update to another system to save your [HomeAssistant](https://home-assistant.io) resources from non-mission critical functions.

Due to API limits the most stocks you can include are 5.

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

This script is meant to run with something like supervisord, and has a default interval of 3600 seconds (1 hour). If you want to have this script to update your stocks continiously set the interval greater than zero. If interval is set to 0 the script will exit after running once. If you want to have cron or some other system mange the script execution then simply set the interval to 0 in the .env 

There is a brief write up about the specific use case I built this for at [https://slackerlabs.org/2019/03/08/home-assistant-alpha-vantage/]


## Features
* This script publishes stock price to topic `stock/<stock_name>/price`
* This script can only handle up to 5 stocks at one time or it will hit the api limit of 5 calls a minute.
* This script is built to run continiously and will pause for the interval set in the `.env` file.
* The script has an app_mode set in the .env file. When app_mode is set to `debug` the script will output status messages to stdout. If you would like to supress these, change app_mode to somethign other than `debug`. Default app_mode is `prod`.   


## You can Splunk It if you want to. You can leave your friends behind...

I removed the ability to log to [Splunk's HTTP Event Collector](https://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector) to reduce code and complexity.

## Compatibility

This script was written and tested using python 3.7.2


