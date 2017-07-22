

import network
import time
import machine
import gc
from machine import Pin
from dht import DHT11
from umqtt.simple import MQTTClient

d = DHT11(Pin(14))

#
# connect the ESP8266 to local wifi network
#
yourWifiSSID = "xxxxxxxxxx"
yourWifiPassword = "xxxxxxxx"
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(yourWifiSSID, yourWifiPassword)
while not sta_if.isconnected():
  pass

#
# connect ESP8266 to Adafruit IO using MQTT
#
myMqttClient = "startup-house-mqtt-client"  # can be anything unique
adafruitIoUrl = "io.adafruit.com"
adafruitUsername = "eMicro"  # can be found at "My Account" at adafruit.com
adafruitAioKey = "xxxxxxxxxxxx"  # can be found by clicking on "VIEW AIO KEYS" when viewing an Adafruit IO Feed
c = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
c.connect()

#
# publish temperature and free heap to Adafruit IO using MQTT
#
# note on feed name in the MQTT Publish:
#    format:
#      "<adafruit-username>/feeds/<adafruitIO-feedname>"
#    example:
#      "MikeTeachman/feeds/feed-TempInDegC"
#
#
while True:
  d.measure()
  c.publish("eMicro/feeds/temp", str(d.temperature()))  # publish temperature to adafruit IO feed
  c.publish("eMicro/feeds/humid", str(d.humidity()))  # publish temperature to adafruit IO feed
  c.publish("eMicro/feeds/feed-micropythonFreeHeap", str(gc.mem_free()))  #publish num free bytes on the Heap
  time.sleep(5)  # number of seconds between each Publish

c.disconnect()
