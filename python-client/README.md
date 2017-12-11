# Cloud IoT Core Python Sample for the TAW

This folder contains a Python client that demonstrate an overview of the
Google Cloud IoT Core platform.

## Quickstart
1. Install the gCloud CLI as described in [the Cloud IoT Core documentation](https://cloud.google.com/iot/docs/how-tos/getting-started#set_up_the_google_cloud_sdk_and_gcloud).

2. Install the dependencies needed to run the sample:
    
        $sudo pip install -r requirements.txt

3. Create a PubSub topic :

        $gcloud beta pubsub topics create projects/iot-taw-project/topics/iot-data

4. Add the service account `cloud-iot@system.gserviceaccount.com` with the role `Publisher` to that
PubSub topic from the [Cloud Developer Console](https://console.cloud.google.com). This service account will be used by IOT Core
to publish the data to the Cloud Pub/Sub topic created above.

5. Create a registry:

        $gcloud beta iot registries create iot-taw-registry \
            --project=iot-taw-project \
            --region=us-central1 \
            --event-pubsub-topic=projects/iot-taw-project/topics/iot-data

6. Use the `generate_keys.sh` script to generate your signing keys. This script creates a RS256 Public/Private Key pair (rsa_cert.pem/rsa_private.pem) and also retrieves the Google root certificate (roots.pem) in the current directory

        $./generate_keys.sh

7. Register a device:

        $gcloud beta iot devices create iot-device \
            --project=iot-taw-project \
            --region=us-central1 \
            --registry=iot-taw-registry \
            --public-key path=rsa_cert.pem,type=rs256

8. Send mock data using the no_sensor_cloudiot_gen.py script. It publishes data over MQTT every 2 secs:

        $python no_sensor_cloudiot_gen.py --registry_id=iot-taw-registry --project_id=iot-taw-project --device_id=iot-device --algorithm=RS256 --private_key_file=rsa_private.pem

    To see all the command line options the script accepts, use 'python no_sensor_cloudiot_gen.py -h'. It pushes JSON-formatted data in the following format  

    Publishing message #1: '{'storeid': 'chi-store-02', 'timestamp': '2017-12-11T19:44:51.773058Z', 'scanid': 'scan000001'
, 'hub_device_id': 'hub09', 'upc': 'A800000013'}'   
    Publishing message #2: '{'storeid': 'nyc-store-03', 'timestamp': '2017-12-11T19:44:53.775522Z', 'scanid': 'scan000002'
, 'hub_device_id': 'hub08', 'upc': 'A800000013'}'   
    Publishing message #3: '{'storeid': 'chi-store-02', 'timestamp': '2017-12-11T19:44:55.778152Z', 'scanid': 'scan000003'
, 'hub_device_id': 'hub02', 'upc': 'A800000012'}'   
    Publishing message #4: '{'storeid': 'sf-store-01', 'timestamp': '2017-12-11T19:44:57.780711Z', 'scanid': 'scan000004',
 'hub_device_id': 'hub03', 'upc': 'A800000010'}'

