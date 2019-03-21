import scipy.misc
import firebase_admin as fba
from firebase_admin import storage
from firebase_admin import firestore
from PIL import Image
import numpy as np
import paho.mqtt.client as mqtt
import queue
import heapq
import datetime as dt
q=queue.PriorityQueue()

def plant_processor(doc_snapshot, changes,read_time):
    print("snapshot",doc_snapshot)
    
    if doc_snapshot:
        a=doc_snapshot[0].to_dict()
        b=ScheduleEntry(a['xcoord'],a['ycoord'],a['day'],a['time'],a['plant'])
        q.put(b)
        print(list(q.queue))
    else:
        print("something has gone horribly wrong")

def water_writer(doc_snapshot, changes,read_time):
    docnames1=doc_snapshot[0]
    docnames2=docnames1.to_dict()
    docnames3=docnames2['names']
    docnames=docnames3.split(",")

    print(docnames)
    print(read_time)
    for docname in docnames:
        try:
            db.collection(u'Users').document(u'test@gmail.com').collection(u'Schedules').document(docname).on_snapshot(plant_processor)
        except:
            print("document name error, please yell at app team")
    #for change in col_snapshot:
    #    edited=change.to_dict()
    #    for key in edited:
    #        if edited[key]:
    #            print(key)
    #            self.client.publish("water","please")
    #            self.db.collection(u'Users').document(u'test@gmail.com').collection(u'Trigger').document(u'Trigger').set({key:False}, merge=True)

def init_fb():
    cred = fba.credentials.Certificate("eden-34f6a-firebase-adminsdk-yigr5-b66d22fc0b.json")
    fba.initialize_app(cred,{'storageBucket': "eden-34f6a.appspot.com"})
    db = firestore.client()
    db.collection(u'Users').document(u'test@gmail.com').collection(u'Schedules').document(u'Schedules').on_snapshot(water_writer)   
    return db



class ScheduleEntry:
    def __init__(self, xcoord,ycoord,day,time,plant):
        self.xcoord=xcoord 
        self.ycoord=ycoord
        rn=dt.datetime(2019,1,1).today().weekday()
        self.datetime=dt.datetime(2018,1,1,).today()
        self.datetime+=dt.timedelta((day-rn )%7)
        
        self.datetime=self.datetime.replace(
                hour=int(time.split(":")[0]),
                minute=int(time.split(":")[1]),
                second=0,
                microsecond=0
                )


        self.plant=plant
    def __repr__(self):
        return "ScheduleEntry("+self.plant+str(self.datetime)+")"

    def __lt__(self, other):
        return self.datetime<other.datetime

    def __gt__(self, other):
        return self.datetime>other.datetime

db = init_fb()
client=mqtt.Client("water_watcher")
client.connect("192.215.3.65")


