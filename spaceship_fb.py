import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
import time
# from firebase import Firebase


#! location=firebase.firestore.GeoPoint(latitude, longitude)

# location = firebase.firestore.GeoPoint(latitude, longitude)


class CloudData:
    def __init__(self, token, DroneLatLng, ReceiverLatLng, droneInMotion, loadPackage,
                 SenderLatLng, tokenInserted, unloadPackage, orderComplete, sendDrone):
        self.token = token
        self.DroneLatLng = DroneLatLng
        self.ReceiverLatLng = ReceiverLatLng
        self.droneInMotion = droneInMotion
        self.loadPackage = loadPackage
        self.SenderLatLng = SenderLatLng
        self.tokenInserted = tokenInserted
        self.unloadPackage = unloadPackage
        self.orderComplete = orderComplete
        self.sendDrone = sendDrone

    @staticmethod
    def from_dict(token, source):
        cl = CloudData(source[u'DroneLatLng'], source[u'ReceiverLatLng'], source[u'droneInMotion'], source[u'loadPackage'],
                       source[u'tokenInserted'], source[u'unloadPackage'], source[u'unloadPackage'], source[u'orderComplete'], source[u'sendDrone'])

        cl.token = token,
        cl.DroneLatLng = source[u'DroneLatLng']
        cl.ReceiverLatLng = source[u'ReceiverLatLng']
        cl.droneInMotion = source[u'droneInMotion']
        cl.loadPackage = source[u'loadPackage']
        cl.SenderLatLng = source[u'SenderLatLng']
        cl.tokenInserted = source[u'tokenInserted']
        cl.unloadPackage = source[u'unloadPackage']
        cl.orderComplete = source[u'orderComplete']
        cl.sendDrone = source[u'sendDrone']

        return cl


# Use a service account
cred = credentials.Certificate(
    './spaceship-ea5c4-firebase-adminsdk-la5ic-2da0857e67.json')
firebase_admin.initialize_app(cred)

# db = firestore.client()


# snapshots = db.collection('transports')
# docs = snapshots.stream()

# #! documentField can be used to store and use retrieved data

# documentFields = dict()

# for doc in docs:
#     documentFields = doc.to_dict()
#     if (documentFields[u'orderComplete'] == False):
#         # docData = CloudData.from_dict(doc.id, documentFields)
#         print("\n Document Data: ", doc.id)
#         lat = documentFields['DroneLatLng'].getLongitude()
#         # print("\n Drone LatLng: ", firebase.firestore.GeoPoint(
#         #     documentFields['DroneLatLng']))
#         print("\n Drone LatLng: ", lat)
#         # print('{} => {} '.format(doc.id, doc.to_dict()))


# def updateFirestoreField(token, key, value):
#     snapshots.document(token).update({key: value})

#! Updates document fields

# Set the capital field

# [END update_doc]


#! Rules: when drone is done: Set orderCompelete = True
#! When Drone reach sender and fans stop circulating: Set loadPackage = true
#! When sender loads package and sets loadPackage = false and sendDrone = True. Activate Drone lunch = true
#! When drone reach receiver and fans stop circulating: Set unloadPackage = true
#! When orderComplete = true: Retreive Drone back to base
#! Operation Completed

print('Initializing Firestore connection...')
# Credentials and Firebase App initialization. Always required

# Get access to Firestore
db = firestore.client()
print('Connection initialized')

data = dict()


def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        data = doc
        print(u'Received document snapshot: {}'.format(doc.to_dict()))
        print(data.get(u'orderComplete'))


doc_ref = db.collection('transports')
doc_watch = doc_ref.on_snapshot(on_snapshot)


# Keep the app running
while True:
    time.sleep(1)
    print('processing...')
