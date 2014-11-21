#!/usr/bin/python
import paho.mqtt.publish as publish

publish.single('Topic', 'HelloWorld' , hostname='localhost')
