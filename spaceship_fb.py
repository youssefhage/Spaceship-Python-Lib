import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
import time
# from firebase import Firebase


#! location=firebase.firestore.GeoPoint(latitude, longitude)

# location = firebase.firestore.GeoPoint(latitude, longitude)


class CloudData:
    def __init__(self, token, DroneLatLng, ReceiverLatLng, loadPackage,
                 SenderLatLng, tokenInserted, unloadPackage, orderComplete, sendDrone):
        self.token = token
        self.DroneLatLng = DroneLatLng
        self.ReceiverLatLng = ReceiverLatLng
        self.loadPackage = loadPackage
        self.SenderLatLng = SenderLatLng
        self.tokenInserted = tokenInserted
        self.unloadPackage = unloadPackage
        self.orderComplete = orderComplete
        self.sendDrone = sendDrone

    @staticmethod
    def from_dict(token, source):
        cl = CloudData(source.get('DroneLatLng'), source.get('ReceiverLatLng'), source.get('loadPackage'),
                       source.get('tokenInserted'), source.get('unloadPackage'), source.get('orderComplete'), source.get('sendDrone'))

        cl.token = token,
        cl.DroneLatLng = source.get('DroneLatLng')
        cl.ReceiverLatLng = source.get('ReceiverLatLng')
        cl.loadPackage = source.get('loadPackage')
        cl.SenderLatLng = source.get('SenderLatLng')
        cl.tokenInserted = source.get('tokenInserted')
        cl.unloadPackage = source.get('unloadPackage')
        cl.orderComplete = source.get('orderComplete')
        cl.sendDrone = source.get('sendDrone')

        return cl


# Use a service account
cred = credentials.Certificate(
    './spaceship-ea5c4-firebase-adminsdk-la5ic-2da0857e67.json')
firebase_admin.initialize_app(cred)

print('Initializing Firestore connection...')

db = firestore.client()
print('Connection initialized')
data = dict()


def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        data = doc
        # cl = CloudData.from_dict(doc.id, data)  not usable
        print(data.get(u'orderComplete'))


#doc_ref = db.collection('transports').document(token)
doc_ref = db.collection('transports')
doc_watch = doc_ref.on_snapshot(on_snapshot)

while True:
    time.sleep(1)
    print('processing...')


#! Updates document fields
def updateFirestoreField(token, key, value):
    db.document(token).update({key: value})


#!<Guidlines/Rules>

#! When drone is done: Set orderCompelete = True
#! When Drone reach sender and fans stop circulating: Set loadPackage = true
#! When sender loads package and sets loadPackage = false and sendDrone = True. Activate Drone lunch = true
#! When drone reach receiver and fans stop circulating: Set unloadPackage = true
#! When orderComplete = true: Retreive Drone back to base
#! Operation Completed
