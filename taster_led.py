from machine import Pin
import network  
from umqtt.simple import MQTTClient
import time
import json
from HTU2X import HTU21D

MQTT_SERVER = "10.50.217.98"
CLIENT_ID = "MQTT_BAUM"
MQTT_TOPIC = "BZTG/Anzeige/LED"

htu = HTU21D(22,21)

wlan = network.WLAN(network.STA_IF)     #Objekt wlan als station interface

wlan.active(True)                       #System einschalten

if not wlan.isconnected():              #Wenn Wlan nicht verbunden ist -> 

    wlan.connect("BZTG-IoT", "WerderBremen24")      #Wlan verbinden

    while not wlan.isconnected():                   #Solange es nicht verbunden ist -> mache nichts

        pass

    print("Netzwerkkonfiguration: ", wlan.ifconfig())   #Netzwerkinfos ausgeben (IP Adresse, Subnetzmaske, Gateway, DNS-Server)


led_gruen = Pin(17, Pin.OUT)
taster = Pin(15, Pin.IN)

was_off_before = True
led_on = False

while True:
    eingang = taster.value()
    if eingang and was_off_before:
        led_on = not led_on
        was_off_before = False
    if not eingang:
        was_off_before = True
    if led_on:
        led_gruen.on()
    else:
        led_gruen.off()

    led_ein = led_on

    mqtt_Baum = MQTTClient(CLIENT_ID, MQTT_SERVER)
    mqtt_Baum.connect()

    anzeige_Werte = {
        "LED_an" :[
            {
                "Anzeige": led_ein 
            }
        ]
    }

    print("MQTT verbunden!")

    mqtt_Baum.publish(MQTT_TOPIC,json.dumps(anzeige_Werte))
    mqtt_Baum.disconnect()
