/**
 * Copyright 2016 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
'use strict';

// [START import]
const functions = require('firebase-functions');
// [END import]

// The Firebase Admin SDK to access the Firebase Realtime Database. 
const admin = require('firebase-admin');
admin.initializeApp(functions.config().firebase);

// [START deviceEvent]
/**
 * Cloud Function to be triggered by Pub/Sub that logs a message using the data published to the
 * topic.
 */
// [START trigger]
exports.deviceEventPubSub = functions.pubsub.topic('iot-data').onPublish(event => {
// [END trigger]
  // [START readBase64]
  const pubSubMessage = event.data;
  // Decode the PubSub Message body.
  const messageBody = pubSubMessage.data ? Buffer.from(pubSubMessage.data, 'base64').toString() : null;
  // [END readBase64]
  // Print the message in the logs.
  console.log(`Hello Device Event - ${messageBody}`);
  
    const eventJSON = messageBody;
  // [START adminSdkAdd]
  // Push the new message into the Realtime Database using the Firebase Admin SDK.
  admin.firestore().collection('device-events').add(JSON.parse(eventJSON)).then(writeResult => {
    // Send back a message that we've succesfully written the message
    //res.json({result: `Message with ID: ${writeResult.id} added.`});
  });
  
  
});
// [END deviceEvent]

