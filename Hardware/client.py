#import movement
import paho.mqtt.client as mqtt
import sys
#import ev3dev.ev3 as ev3
import math

###
movement = None
###

calibrated=False
calibrating=False
waiting=False
position=None
angle=0
instructions_to_follow = []
client=mqtt.Client("ev3")
initial=None
SINGLE_SQUARE_TIME_TO_MOVE=500


def forward(x):
    movement.forward_t(x*SINGLE_SQUARE_TIME_TO_MOVE)

def face(x):
    movement.turn(300, x-angle)
    angle=x

def relativeTurn(x):
    movement.turn(300,x)
    angle+=x

def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)
    client.subscribe("instructions")
    client.subscribe("pos")

def onMessage(client,userdata,msg):
    print("Received message with payload:%s "%(msg.payload.decode()))
    if (msg.topic=="instructions"):
        instructions_from_server = msg.payload.decode("ascii").split(",")
        instructions_to_follow = [(t,int(v)) for (t,v) in instructions_from_server]
        follow_insts_in_list()

    # if msg.topic=="pos":
    #     position=arguements
    #     print("positional input")
    #     print(waiting)
    #     if not calibrating:
    #         print("calibrating")
    #         calibrating=True
    #         initial=position
    #         print("right before")
    #         movement.forward_t(1000)
    #         waiting=True
    #         print("past")
    #     elif waiting:
    #         waiting=False
    #         print(1)
    #         difference=[position[0]-initial[0], position[1]-initial[1]]
    #         print("2")
    #         print(math.atan(difference[0]/difference[1]))
    #         angle=math.atan(difference[0]/difference[1])
    #         print(3)
    #         speed=math.sqrt(difference[0]^2+difference[1]^2)
    #         print(4)
    #         print(5)
    #         print(6)
    #         calibrated=True
    #         print("calibrated")
    
def follow_insts_in_list():
    while len(instructions_to_follow)>0:
        # instruction type t and value v - i.e. ('m',5)
        inst = instructions_to_follow.remove(0)
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
        else:
            # (type,value) format
            (t,v) = inst
            if t=='m':
                forward(v)
                print("moved %i squares"%v)
            elif t=='r':
                relativeTurn(v)
                print("turned %i degrees"%v)
            else:
                print("Invalid instruction!: (%s,%i)"%(t,v))
                ##error

client.on_connect=onConnect
client.on_message=onMessage
client.connect("129.215.202.200")
#client.connect("localhost")

client.loop_forever()
