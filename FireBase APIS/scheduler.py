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
import time
import threading

q=queue.PriorityQueue()
stoplisteners={}
lock=threading.Condition()




def plant_processor(doc_snapshot):
    print("snapshot",doc_snapshot)
    global t
    a=doc_snapshot.to_dict()
    if a!=None and a["valid"]:
        a=doc_snapshot.to_dict()
        print(doc_snapshot)
        b=ScheduleEntry(doc_snapshot.id,a['plantXCoordinate'],a['plantYCoordinate'],a['day'],a['time'],a['plantNoOfPetals'],doc_snapshot)

        if b.datetime< dt.datetime(1999,1,1).now():
            b.datetime=b.datetime+dt.timedelta(7)

        q.put(b)
        print(list(q.queue))
        print((q.queue[0].datetime-dt.datetime(1999,1,1).now()).total_seconds())
        
    else:
        print("documentGone")
    

def water_writer(doc_snapshot, changes,read_time):
    global q
    docnames1=doc_snapshot[0]
    docnames2=docnames1.to_dict()
    docnames=docnames2['names']
    print(docnames)
    print(read_time)
    q=queue.PriorityQueue()
    for docname in docnames:
            print(docname)
            doc=db.collection(u'Users').document(u'test@gmail.com').collection(u'Schedules').document(docname).get()
            print(doc)
            plant_processor(doc)

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

def on_connect(client, userdata, flacgs, rc):
    print("mqtt connected")
    client.subscribe("navigate-finish")

def on_message(client,userdata,message):
    global lock
    print("message")
    if message.topic=="navigate-finish":
        with lock:
            lock.notify()
        print("navigate finished")

class ScheduleEntry:
    def __init__(self,docname, xcoord,ycoord,day,time,plant,docid):
        self.docname=docname
        self.xcoord=xcoord 
        self.ycoord=ycoord
        rn=dt.datetime(2019,1,1).today().weekday()
        self.datetime=dt.datetime(2018,1,1,).today()
        self.datetime+=dt.timedelta((day-rn )%7)
        self.docid=docid
        self.datetime=self.datetime.replace(
                hour=int(time.split(":")[0]),
                minute=int(time.split(":")[1]),
                second=0,
                microsecond=0
                )


        self.plant=plant
        
    def send_if_ok(self):
        doc=db.collection(u'Users').document(u'test@gmail.com').collection(u'Schedules').document(self.docname).get()
        loc=doc.to_dict()
        if loc!=None:
            if loc['valid']:
                client.publish('navigate-start',(str(self.xcoord)+","+str(self.ycoord)), qos=2)
                print("going")
                with lock:
                    lock.wait()
                self.datetime+=dt.timedelta(7)
                q.put(self)
                client.publish('close-navigate',str(self.plant), qos=2)

    
        
    def __repr__(self):
        return "ScheduleEntry("+str(self.plant)+str(self.datetime)+"::"+str(self.xcoord) +","+ str(self.ycoord)+")"

    def __lt__(self, other):
        return self.datetime<other.datetime

    def __gt__(self, other):
        return self.datetime>other.datetime

db = init_fb()
client=mqtt.Client("water_watcher")

client.on_connect=on_connect
client.on_message=on_message

client.connect("129.215.3.65")

client.loop_start()

while True:
    now=dt.datetime(1999,1,1).now()
    while not q.empty() and q.queue[0].datetime<now:
        loc=q.get()
        
        loc.send_if_ok()

        
        if q.empty() or q.queue[0].datetime>now:
            print("going home")
    time.sleep(1)
    if q.empty():
        print("empty")
    else:
        print(q.queue[0])

