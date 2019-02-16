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


class FirebaseInteraction:
    def __init__(unwarper):
        self.unwarper = unwarper
        self.db = self.init_fb()

    def main(image_as_np):
        ''' get image from np array '''
        scipy.misc.toimage(image_as_np).save("overhead-image-for-app.png")

        '''store image'''
        bucket = storage.bucket()
        image_blob = bucket.blob("overhead-image")
        image_blob.upload_from_filename("overhead-image-for-app.png")

        new_status = {'status':'request_complete'}
        db.collection(u'overhead-image').document(u'overhead-image').set(new_status)

    ii = np.array([[1,1,0,0,0,0],[0,0,1,1,1,1]])
    main(ii)

    def init_fb():
        cred = fba.credentials.Certificate("eden-34f6a-firebase-adminsdk-yigr5-83fe6dc575.json")
        fba.initialize_app(cred,{
            'storageBucket': "eden-34f6a.appspot.com"
        })
        db = firestore.client()
        
        db.collection(u'overhead-image').document(u'overhead-images').on_snapshot(get_image_from_vision())
        return db

    def get_image_from_vision():



    