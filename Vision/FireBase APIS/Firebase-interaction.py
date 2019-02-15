import scipy.misc
import firebase_admin as fba
from PIL import Image

## take np array image
## convert to reel image
## upload to firebase storage
## put path on firebase firestore

## tell app people what you're doing

def main(image_as_np):
    ''' get image from np array '''
    scipy.misc.toimage(image_as_np).save("overhead-image-for-app.png")

    ''' initialize firebase connection'''
    # depends on the key you're using!!
    cred = fba.credentials.Certificate("eden-34f6a-firebase-adminsdk-yigr5-83fe6dc575.json")
    fba.initialize_app(cred)

    '''store image'''
    bucket = fba.storage.bucket()
    image_blob = bucket.blob("image-blob")
    image_blob.upload_from_filename("overhead-image-for-app.png")


    


    