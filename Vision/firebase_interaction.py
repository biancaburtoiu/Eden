import scipy.misc
import firebase_admin as fba
from firebase_admin import storage
from firebase_admin import firestore
import numpy as np
import cv2
#import Vision.LiveUnwarper as luwp
import time

def process_image(image_as_np):
    ''' get image from np array '''
    scipy.misc.toimage(cv2.cvtColor(image_as_np,cv2.COLOR_BGR2RGB)).save("overhead-image-for-app.png")

    '''store image'''
    bucket = storage.bucket()
    image_blob = bucket.blob("overhead-image")
    image_blob.upload_from_filename("overhead-image-for-app.png")

    '''update status in firestore'''
    new_status = {'status':'request_complete'}
    if db is not None:
        db.collection(u'overhead-image').document(u'overhead-image').set(new_status)
    else:
        print("Could not update status file - database was None!")

def init_fb():
    '''log in to firebase and get db instance'''
    ###############################################################################
    # #### you must get a key, put in the directory of this file, and write the name below! ########
    ###############################################################################
    try:
       # cred = fba.credentials.Certificate("Vision/eden-34f6a-firebase-adminsdk-yigr5-83fe6dc575.json")
        cred = fba.credentials.Certificate("eden-34f6a-firebase-adminsdk-yigr5-83fe6dc575.json")
        fba.initialize_app(cred,{
            'storageBucket': "eden-34f6a.appspot.com"
        })
        db = firestore.client()
        
        '''set up listener for changes to overhead-images doc'''
        doc_watch = db.collection(u'overhead-image').document(u'overhead-image').on_snapshot(on_doc_update)
        return db,doc_watch
    except:
        print("Firebase_interaction: You don't have a key !!!")
        return None,None

def on_doc_update(doc_snap,changes,read_time):
    if len(doc_snap)>0:
        #status stored in status field
        #  -'request_pending'   : trigger script to get new image
        #  -'request_complete'  : trigger for app that image is uploaded
        #  -[anything else]     : no image needed right now
        request_status = doc_snap[0].get('status')

        if request_status is not None and request_status == "request_pending":
            image_as_np =get_image_from_vision()
            process_image(image_as_np)

def get_image_from_vision():
    '''spooky vision stuff (ALSO OLD)
    luwp.set_res(cam, 1920, 1080)
    for i in range(50):
        _, img = cam.read()
    print("about to get image")
    while img is None:
        _, img = cam.read()
    print("got image")
    merged_img = unwarper.stitch_one_two_three_and_four(img)
    print("image merged")
    return merged_img '''
    print("get image from vision")
    image = unwarper.get_overhead_image()
    while unwarper.get_overhead_image() is None:
        image = unwarper.get_overhead_image()
    print("got image")
    return image


# takes the new battery status and puts it on firebase. This is called by LiveUnwarper,
# in it's onMessage, when it receives a new battery status over mqtt from the ev3.
def update_battery_status_in_db(new_status):
    # possibly convert to % here?
    if db is not None:
        new_status_dict = {'battery-status':str(new_status)}
        db.collection(u"battery-info-collection").document(u"battery-info-document").set(new_status_dict)
    else:
        print("could not update battery status - database was None!")

# This is called by LiveUnwarper - this class also gives us the image of the room
def start_script(unwarper_instance):
    global unwarper
    unwarper = unwarper_instance
    print("starting script")
    global db
    db, doc_watch = init_fb()
    return db,doc_watch

if __name__ == "__main__":
    global db
    db,_=init_fb()
    update_battery_status_in_db(5000)
