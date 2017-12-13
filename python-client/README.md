# Cloud IoT Core Python Sample for the TAW

This folder contains a Python client that demonstrate an overview of the
Google Cloud IoT Core platform.

## Quickstart
1. Install the gCloud CLI as described in [the Cloud IoT Core documentation](https://cloud.google.com/iot/docs/how-tos/getting-started#set_up_the_google_cloud_sdk_and_gcloud). If you are using Cloud shell which is the recommended method, it comes with gCloud pre-installed

2. Create a PubSub topic :

        $gcloud beta pubsub topics create projects/iot-taw-project/topics/iot-data

3. Add the service account `cloud-iot@system.gserviceaccount.com` with the role `Publisher` to that
PubSub topic from the [Cloud Developer Console](https://console.cloud.google.com). This service account will be used by IOT Core
to publish the data to the Cloud Pub/Sub topic created above.

4. Create a registry:

        $gcloud beta iot registries create iot-taw-registry \
            --project=iot-taw-project \
            --region=us-central1 \
            --event-pubsub-topic=projects/iot-taw-project/topics/iot-data

5. Use the `generate_keys.sh` script to generate your signing keys. This script creates a RS256 Public/Private Key pair (rsa_cert.pem/rsa_private.pem) and also retrieves the Google root certificate (roots.pem) in the current directory

        $./generate_keys.sh

6. Register a device:

        $gcloud beta iot devices create iot-device \
            --project=iot-taw-project \
            --region=us-central1 \
            --registry=iot-taw-registry \
            --public-key path=rsa_cert.pem,type=rs256

7. Install the dependencies needed to run the python client:
    
        $sudo pip install -r requirements.txt

8. Send mock data using the no_sensor_cloudiot_gen.py script. It publishes data over MQTT every 2 secs:

        $python no_sensor_cloudiot_gen.py --registry_id=iot-taw-registry --project_id=iot-taw-project --device_id=iot-device --algorithm=RS256 --private_key_file=rsa_private.pem

    To see all the command line options the script accepts, use 'python no_sensor_cloudiot_gen.py -h'. It pushes JSON-formatted data in the following format  

    Publishing message #1: '{'scanid': 'scan000001', 'hub_device_id': 'hub06', 'timestamp': '2017-12-13T18:48:47.762445Z', 'storeid': 'nyc-store-03', 'upc': 'A800000017', 'event': 'Removed'}'   
    Publishing message #2: '{'scanid': 'scan000002', 'hub_device_id': 'hub09', 'timestamp': '2017-12-13T18:48:49.764968Z', 'storeid': 'sf-store-01', 'upc': 'A800000012', 'event': 'Removed'}'   
    Publishing message #3: '{'scanid': 'scan000003', 'hub_device_id': 'hub07', 'timestamp': '2017-12-13T18:48:51.767631Z', 'storeid': 'nyc-store-03', 'upc': 'A800000016', 'event': 'Placed'}'   
    Publishing message #4: '{'scanid': 'scan000004', 'hub_device_id': 'hub03', 'timestamp': '2017-12-13T18:48:53.770235Z', 'storeid': 'chi-store-02', 'upc': 'A800000018', 'event': 'Placed'}'

