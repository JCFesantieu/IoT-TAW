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

8. Send some Sample data (data/SampleData.json) using the no_sensor_cloudiot_gen.py script. It publishes all 1000 JSON entries to the device's MQTT topic one by one:

        $python no_sensor_cloudiot_gen.py --registry_id=iot-taw-registry --project_id=iot-taw-project --device_id=iot-device --algorithm=RS256 --private_key_file=rsa_private.pem

    To see all the command line options the script accepts, use 'python no_sensor_cloudiot_gen.py -h'. It pushes JSON-formatted data in the following format. If you need to generate different sample data, you can use the data/datagen.py script and then use the --json_data_file option to specify the json file which contains your new data

    Publishing message #997: '{u'scanid': u'scan000997', u'hub_device_id': u'hub3', u'timestamp': u'2017-12-20T01:51:03.755048Z', u'storeid': u'sfo-store-01', u'upc': u'A800000044', u'event': u'Placed'}'   
    Publishing message #998: '{u'scanid': u'scan000998', u'hub_device_id': u'hub5', u'timestamp': u'2017-12-20T01:51:13.761008Z', u'storeid': u'nyc-store-03', u'upc': u'A800000021', u'event': u'Placed'}'   
    Publishing message #999: '{u'scanid': u'scan000999', u'hub_device_id': u'hub6', u'timestamp': u'2017-12-20T01:51:14.766344Z', u'storeid': u'chi-store-02', u'upc': u'A800000002', u'event': u'Removed'}'   
    Publishing message #1000: '{u'scanid': u'scan001000', u'hub_device_id': u'hub6', u'timestamp': u'2017-12-20T01:51:14.768079Z', u'storeid': u'nyc-store-03', u'upc': u'A800000025', u'event': u'Removed'}'

