import scipy.misc
import firebase_admin as fba
from firebase_admin import storage
from firebase_admin import firestore
from PIL import Image
import numpy as np
import paho.mqtt.client as mqtt

## take np array image
## convert to reel image
## upload to firebase storage
## put path on firebase firestore

## tell app people what you're doing

'''
gotta change it:
    - not gonna be called by vision, just gonna get a webcam frame itself
    - no unwarper in init!
    - doesn't really need to be OO, and the callback cannot be OO, probably don't
      make any of it OO 
'''




class FirebaseInteraction:
    def __init__(self):
        self.db = self.init_fb()
        self.client=mqtt.Client("water_watcher")
        self.client.connect("129.215.202.200")

    def init_fb(self):
        cred = fba.credentials.Certificate("eden-34f6a-firebase-adminsdk-yigr5-b66d22fc0b.json")
        fba.initialize_app(cred,{
            'storageBucket': "eden-34f6a.appspot.com"
        })
        db = firestore.client()
        db.collection(u'Users').document(u'test@gmail.com').collection(u'Trigger').document(u'Trigger').on_snapshot(self.water_writer)
        
        return db

    def water_writer(self,col_snapshot, changes,read_time):
        print("change made")
        print(changes)
        for change in col_snapshot:
            edited=change.to_dict()
            for key in edited:
                if edited[key]:
                    print(key)
                    self.client.publish("water","please")
                    self.db.collection(u'Users').document(u'test@gmail.com').collection(u'Trigger').document(u'Trigger').set({key:False}, merge=True)

if __name__=="__main__":
    FirebaseInteraction()


