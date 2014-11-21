#!/usr/bin/python
import sys
import boto
import paho.mqtt.client as mqtt

stream_name = 'MQTT-Kinesis'
topic_name = 'Topic'
partition_key = 'PartitionKey'
hostname = 'localhost'
port = 1883
keepalive = 60
qos = 0

kinesis = boto.connect_kinesis()
records_buffer = []
stream = None

def get_stream(stream_name):
    try:
        stream = kinesis.describe_stream(stream_name)
        print(stream)
    except ResourceNotFoundException as rnfe:
        print('Stream is not found.')
    return stream

def put_record(record):
    print(stream, record, partition_key)
    response = kinesis.put_record(
        stream_name=stream_name,
        data=record,
        partition_key=partition_key)
    print(response)

def on_connect(mqttc, obj, rc):
    print("Connected with result code "+str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.payload))
    put_record(msg.payload)

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

stream = get_stream(stream_name)
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.connect(hostname, port, keepalive)
mqttc.subscribe(topic_name, qos)
mqttc.loop_forever()
