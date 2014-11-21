Mqtt2Kinesis
============

device -> mqtt -> mosquitto -> mqtt2kinesis.py -> kinesis's stream -> (Lambda???)

### Setup Kinesis's stream by AWS Management Console
```
[Information]
date = 2014.11.21
region = ap-northeast-1
stream name = MQTT-Kinesis
nuber of shards = 1
```
============
### Setup Mqtt2Kinesis
#### Start ec2 instance
```
[Information]
date = 2014.11.21
region = ap-northeast-1
ami = Ubuntu Server 14.04 LTS (HVM), SSD Volume Type - ami-e74b60e6
instance type = m3.medium
security group : TCP/UDP 1883 is opened
```

#### Connect to ec2 instance
```
ssh -i key.pem ubuntu@xx.xx.xx.xx
```

#### Install packages
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install paho-mqtt
sudo pip install boto
```

#### AWS credentials
```
vi ~/.boto
```
```
[Credentials]
aws_access_key_id = XXXXXXX
aws_secret_access_key = XXXXXXX
```

#### Install mosquitto
```
sudo apt-get install gcc make g++ libssl-dev libc-ares-dev libc-ares2
wget http://mosquitto.org/files/source/mosquitto-1.3.5.tar.gz
tar xvzf mosquitto-1.3.5.tar.gz
cd mosquitto-1.3.5
make
sudo make install
sudo cp /etc/mosquitto/mosquitto.conf.example /etc/mosquitto/mosquitto.conf
```

#### Start mosquitto
```
mosquitto -c /etc/mosquitto/mosquitto.conf
```
```
1416558687: mosquitto version 1.3.5 (build date 2014-11-21 08:14:20+0000) starting
1416558687: Config loaded from /etc/mosquitto/mosquitto.conf.
1416558687: Opening ipv4 listen socket on port 1883.
1416558687: Opening ipv6 listen socket on port 1883.
........
```

#### Configure mqtt2kinesis
```
vi mqtt2kinesis.py
```
```
stream_name = 'MQTT-Kinesis' # Kinesis's stream-name you created
topic_name = 'Topic' # 
partition_key = 'PartitionKey'
hostname = 'localhost' 
port = 1883 # Edit security group (TCP/UDP 1883)
keepalive = 60
qos = 0
```

#### Start mqtt2kinesis
```
python mqtt2kinesis.py
```
```
{u'StreamDescription': {u'HasMoreShards': False, u'StreamStatus': u'ACTIVE', u'StreamName': u'MQTT-Kinesis', u'StreamARN':
u'arn:aws:kinesis:xxxxxx:xxxxxx:stream/MQTT-Kinesis', u'Shards': [{u'HashKeyRange': {u'EndingHashKey':
u'3402823669209384634633746074317682', u'StartingHashKey': u'0'}, u'ShardId': u'shardId-000000000000',
u'SequenceNumberRange': {u'StartingSequenceNumber': u'49545085634523975986291702117469842927685899'}}]}}
Connected with result code 0
Subscribed: 1 (0,)
........
```

============

### Publish test
```
python publish_test.py
```
```
Topic HelloWorld
({u'StreamDescription': {u'HasMoreShards': False, u'StreamStatus': u'ACTIVE', u'StreamName': u'MQTT-Kinesis', u'StreamARN':
u'arn:aws:kinesis:xxxxx:xxxxxx:stream/MQTT-Kinesis', u'Shards': [{u'HashKeyRange': {u'EndingHashKey':
u'3402823669209384634633746074317', u'StartingHashKey': u'0'}, u'ShardId': u'shardId-000000000000',
u'SequenceNumberRange': {u'StartingSequenceNumber': u'495450856345239759862917021174698429276858991266'}}]}},
'HelloWorld', 'PartitionKey')
{u'ShardId': u'shardId-000000000000', u'SequenceNumber': u'49545085634523975987065990841771162684117085783'}
........
```
