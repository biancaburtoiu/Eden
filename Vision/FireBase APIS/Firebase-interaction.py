import scipy.misc
import firebase_admin as fba
from firebase_admin import storage
from firebase_admin import firestore
from PIL import Image
import numpy as np

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
    def __init__(self,unwarper):
        self.unwarper = unwarper
        self.db = self.init_fb()

    def main(self,image_as_np):
        ''' get image from np array '''
        scipy.misc.toimage(image_as_np).save("overhead-image-for-app.png")

        '''store image'''
        bucket = storage.bucket()
        image_blob = bucket.blob("overhead-image")
        image_blob.upload_from_filename("overhead-image-for-app.png")

        '''update status in firestore'''
        new_status = {'status':'request_complete'}
        self.db.collection(u'overhead-image').document(u'overhead-image').set(new_status)

    def init_fb(self):
        cred = fba.credentials.Certificate("eden-34f6a-firebase-adminsdk-yigr5-83fe6dc575.json")
        fba.initialize_app(cred,{
            'storageBucket': "eden-34f6a.appspot.com"
        })
        db = firestore.client()
        
        db.collection(u'overhead-image').document(u'overhead-images').on_snapshot(get_image_from_vision)
        
        return db

    def get_image_from_vision(self):
        image = self.unwarper.get_recent_image()
        self.main(image)


    