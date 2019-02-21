import movement
import paho.mqtt.client as mqtt
import sys
import ev3dev.ev3 as ev3
import math

calibrated=False
calibrating=False
waiting=False
position=None
angle=0
instructions_to_follow = []
client=mqtt.Client("ev3")
initial=None



def forward(x):
    movement.forward_t(x/speed)

def face(x):
    global angle
    movement.turn(300, x-angle)
    angle=x

def relativeTurn(x):
    movement.turn(300,x)
    angle+=x

def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)
    client.subscribe("instructions")
    client.subscribe("pos")
    ev3.Sound.speak("connected")

def onMessage(client,userdata,msg):
    try:
        global angle
        global speed
        global calibrating
        global waiting
        global calibrated
        global initial
        print("Received message with payload:%s "%(msg.payload.decode()))
        if (msg.topic=="instructions"):
            print("instruction message!")
            instructions_to_follow= msg.payload.decode().split(";")
            follow_insts_in_list()

        if msg.topic=="pos":
             print("positional input")
             print(msg.payload.decode().split(","))
             position=[float(x) for x in msg.payload.decode().split(",")]
             print(waiting)
             if not calibrating:
                 print("calibrating")
                 calibrating=True
                 initial=position
                 print("right before")
                 movement.forward_t(1000)
                 waiting=True
                 print("past")
             elif waiting:
                 waiting=False
                 print(1)
                 difference=[position[0]-initial[0], position[1]-initial[1]]
                 print("2")
                 print(math.atan(difference[0]/difference[1]))
                 angle=math.atan(difference[0]/difference[1])
                 print(3)
                 speed=math.sqrt(difference[0]^2+difference[1]^2)
                 print(4)
                 calibrated=True
                 print("calibrated")
                 print("speed is %f"% speed)
    except:
        print("Error")
        print(sys.exc_info()[0])
        sys.exit()
        raise

def follow_insts_in_list():
    print("starting to follow instructions")
    while len(instructions_to_follow)>0:
        # instruction type t and value v - i.e. ('m',5)
        inst = instructions_to_follow.remove(0)
        print("following instruction:" + inst)
        if inst in ['u','d','l','r']:
        # used to synch robot's direction to match relative instructions
            print("facing %s"%inst)
            if inst=='u':
                face(0)
            elif inst == 'd':
                face(180)
            elif inst=='r':
                face(90)
            else:
                face(270)
            print("done")
        else:
            # (type,value) format
            (t,v) = inst
            v=int(v)
            if t=='m':
                print("moved %i squares"%v)
                forward(v)
                print("done")
            elif t=='r':
                print("turned %i degrees"%v)
                relativeTurn(v)
                print("done")
            else:
                print("Invalid instruction!: (%s,%i)"%(t,v))
                ##error

client.on_connect=onConnect
client.on_message=onMessage
client.connect("129.215.202.200")
#client.connect("localhost")

client.loop_forever()
