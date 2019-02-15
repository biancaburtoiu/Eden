import movement
import paho.mqtt.client as mqtt
import sys
import ev3dev.ev3 as ev3
import math

calibrated=False
calibrating=False
waiting=False
position=None
angle=None

client=mqtt.Client("ev3")

def forward(x):
    global speed
    global movement
    print(1)
    print(x*1000/speed)

    movement.forward_t(x*1000/speed)

def face(x):
    global angle
    global movement
    print(1)
    movement.turn(300, x-angle)
    angle=x
forward=None
face=None
initial=None

def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)
    client.subscribe("move")
    client.subscribe("turn")
    client.subscribe("pos")

def onMessage(client,userdata,msg):
    global calibrating
    global calibrated
    global waiting
    global position
    global angle
    global movement
    global initial
    global speed
    global forward
    global face
    print(msg.topic+" "+str(msg.payload))
    arguements=msg.payload.decode("ascii").split(",")
    arguements=[int(x) for x in arguements]
    print(arguements)
    if msg.topic=="move":
        if calibrated:
            print("moving")
            movement.forward_t(arguements[0]*1000/speed)
            print("moved")
    if msg.topic=="turn":
        if calibrated:
            print("turning")
            movement.turn(300, arguements[0]-angle)
            angle=x

            print("turned")

    if msg.topic=="pos":
        position=arguements
        print("positional input")
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
            print(5)
            print(6)
            calibrated=True
            print("calibrated")
    

client.on_connect=onConnect
client.on_message=onMessage
client.connect("129.215.202.200")
#client.connect("localhost")

client.loop_forever()
