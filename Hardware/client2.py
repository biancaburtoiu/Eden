import movement
import paho.mqtt.client as mqtt
import sys
import ev3dev.ev3 as ev3
import math
import time

def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)
    client.subscribe("instructions")
    client.subscribe("pos")
    ev3.Sound.speak("connected")

def onMessage(client,userdata,msg):
    try:
        print("Received message with payload:%s "%(msg.payload.decode()))
        if  msg.topic=="instructions":
            print("instruction message!")
            instructions_to_follow= msg.payload.decode().split(";")[:-1]
            print("instructions: %s"%instructions_to_follow)
            follow_insts_in_list(instructions_to_follow)
    except:
        print("Error")
        print(sys.exc_info()[0])
        sys.exit()
        raise

def follow_insts_in_list(instructions_to_follow):
    print("starting to follow instructions")
    print("instructions: %s"%instructions_to_follow)
    if instructions_to_follow:
        while len(instructions_to_follow)>0:
            # instruction type t and value v - i.e. ('m',5)
            inst = instructions_to_follow.pop(0)
            print("following instruction:" , inst)
            if inst in ['u','d','l','r']:
            # used to synch robot's direction to match relative instructions
                print("facing %s"%inst)
                if inst=='u':
                    movement_controller.absolute_turn(0)
                elif inst == 'd':
                    movement_controller.absolute_turn(180)
                elif inst=='r':
                    movement_controller.absolute_turn(90)
                else:
                    movement_controller.absolute_turn(270)
                print("done")
            else:
                # (type,value) format
                (t,v) = tuple(inst.split(","))
                v=int(v)
                if t=='m':
                    print("moving %i squares"%v)
                    movement_controller.forward(v)
                    print("done")
                elif t=='r':
                    print("turning %i degrees"%v)
                    movement_controller.relative_turn(v)
                    print("done")
                else:
                    print("Invalid instruction!: (%s,%i)"%(t,v))
                    ##error

# set up client & client functions
client=mqtt.Client("ev3")
client.on_connect=onConnect
client.on_message=onMessage

# movement object, with initial angle of 0
global movement_controller
movement_controller = movement.Movement(0)

#connect client and make it wait for inputs
client.connect("129.215.202.200")
client.loop_forever()
