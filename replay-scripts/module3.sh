#!/bin/bash
projectId=$(gcloud config list --format 'value(core.project)')
echo $projectId

# Switch to IoT-TAW/python-client Directory
cd ../python-client

# Create a Pub/Sub topic & a subscription for that topic
gcloud pubsub topics create projects/$projectId/topics/iot-data
gcloud pubsub subscriptions create iot-sub \
	--topic=iot-data \
	--topic-project=$projectId

# Add the service account cloud-iot@system.gserviceaccount.com with the role pubsub.publisher
# for all the topics in your project. This service account will be used by IOT Core to publish
# the data to the Cloud Pub/Sub topic created above.
gcloud projects add-iam-policy-binding $projectId \
	--member=serviceAccount:cloud-iot@system.gserviceaccount.com \
	--role=roles/pubsub.publisher

# Create a device registry
gcloud beta iot registries create iot-taw \
	--project=$projectId \
	--region=us-central1 \
	--event-pubsub-topic=projects/$projectId/topics/iot-data

# Generate the private/public key pair & Google's root cert (roots.pem)
./generate_keys.sh

# Add a device to the registry
gcloud beta iot devices create iot-device \
	--project=$projectId \
	--region=us-central1 \
	--registry=iot-taw \
	--public-key path=ec_public.pem,type=es256

# Install the dependencies reqd to execute the python client
sudo pip install -r requirements.txt


bq mk -d --data_location US --default_table_expiration 3600 --description "Inventory dataset" $projectId:inventory
bq mk -t --expiration 3600 --description "IOTtable" $projectId:inventory.iottable count:INTEGER,scanid:STRING,hub_device_id:STRING,timestamp:STRING,storeid:STRING,upc:STRING,latlong:STRING,event:STRING

gcloud beta dataflow jobs run dataflow_job --gcs-location gs://dataflow-templates/latest/PubSub_to_BigQuery --parameters inputTopic=projects/$projectId/topics/iot-data,outputTableSpec=$projectId:inventory.iottable
	
# Execute the python client to send mock data to IOT Core. This streams the data/SampleData.json# line by line to the MQTT device topic '/devices/iot-device/events'
python no_sensor_cloudiot_gen.py \
	--registry_id=iot-taw \
	--project_id=$projectId \
	--device_id=iot-device \
	--algorithm=ES256 \
	--private_key_file=ec_private.pem


