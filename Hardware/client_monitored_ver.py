import movement_monitored_ver
import paho.mqtt.client as mqtt
import sys
import ev3dev.ev3 as ev3
import math
import time
from threading import Timer
import ips
import traceback
global currently_moving
global client
global movement_controller

def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)
    client.subscribe("start-instruction")
    client.subscribe("arm")
    client.subscribe("ping-pong")

    ###garbage###
    ev3.Sound.speak("EDEN")
    #############

def on_disconnect(client,userdata,rc):
    print("DISCONNECTED FROM MQTT")
    ev3.sound.speak("disconnected")
    # we've disconnected so tell the robot to stop
    follow_one_instruction("s")

def onMessage(client,userdata,msg):
    try:
        if msg.topic=="start-instruction":
            # single instruction:
            # - face direction, start moving, stop moving, or rotate
            instruction_to_follow = msg.payload.decode().strip()
            follow_one_instruction(instruction_to_follow)
        if msg.topic=="arm":
            movement_controller.arm_to_pos(float(msg.payload.decode()))
        if msg.topic=="ping-pong":
            pl = msg.payload.decode()
            if pl=="pong":
                global received_pong
                print("pong")
                # update global var received_pong for check_for_pong()
                received_pong = True
            elif pl=="ping":
                #our own message
                pass
            else:
                print("useless pong: %s"%pl)

    except:
        # catch any errors to stop alertless crashing
        print("Error")
        traceback.print_exc()
        sys.exit()
        

def follow_one_instruction(instruction_as_string):
    print("about to follow instruction: %s"%instruction_as_string)
    global currently_moving
    global currently_pinging

    if currently_moving:
        # stop (moving) instruction
        if instruction_as_string=='s':
            # not moving or pinging anymore
            currently_moving = False
            currently_pinging = -1
            movement_controller.stop()
            #request next instruction in path
            ask_for_next_inst()
        else:
            print("useless instruction: %s"%instruction_as_string)
    else:
        # fresh instructions

        if instruction_as_string == 's':
            # received a stop when we're already stopped!
            print("ignoring useless s instruction")

        # movement / relative turn instructions (subsequent insts)
        else:
            # in form (r,[degrees],[target dir]), or (m,[squares])
            # note the number of squares is unused for the main navigation
            inst = instruction_as_string.split(",")
            inst_type = inst[0]
            if inst_type=='m':
                currently_moving=True
                # 0 represents active pinging with 0 pings missed so far
                currently_pinging = 0
                movement_controller.forward_forever()
                # send first ping to start playing
                send_ping()
            elif inst_type=='r':
                currently_moving=True
                movement_controller.relative_turn(int(inst[1]))
                ask_for_next_inst()
            else:
                print("received a malformed instruction!: %s"%instruction_as_string)

def check_for_pong():
    global received_pong
    global currently_pinging
    # if this is -1, pinging is not active anymore, due to a stop instruction being sent
    # it must have been sent by vision since when we send one we don't initiate another ping
    # i.e. this means we successfully stopped under normal operation
    if currently_pinging=>0:
        if received_pong:
            #reset missed ping count, and send the next ping
            currently_pinging = 0
            received_pong = False
            send_ping()
        elif:
            #a pong has not been sent in time!
            currently_pinging+=1

            if currently_pinging==3:
                # stop the robot due to x missed pongs.
                # pings will now stop, and currently_pinging will be set to -1
                print("stopping!")
                follow_one_instruction("s")
            else:
                # we've acknowledged the missed pong, but keep trying 
                print("%s missed pongs"%currently_pinging)
                received_pong=False
                send_ping()

def send_ping():
    global publishing_lock
    print("ping")
    client.publish("ping-pong","ping",qos=2)
    #in 3 seconds check for the pong
    Timer(3,check_for_pong,[]).start()

def ask_for_next_inst():
    global currently_moving
    currently_moving = False
    print("about to send finish-instruction")
    client.publish("finish-instruction","",qos=2)
    print("instruction sent!")

def read_battery_status(client):
    # this file contains the current battery voltage
    voltage_file = open("/sys/class/power_supply/legoev3-battery/voltage_now","r")
    # convert reading into string of decimal number
    voltage_level = str(int(voltage_file.readline())/1000000)
    voltage_file.close()
    client.publish("battery-update",voltage_level,qos=2)
    print("sent battery update")
    # starts a threading.Timer object which calls this method again in 300 seconds
    Timer(300,read_battery_status,[client]).start()

# set up client & client functions
client=mqtt.Client("ev3")
client.on_connect=onConnect
client.on_message=onMessage

# if this is true, robot is either turning or moving forever
currently_moving = 0

# tracks whether vision system has responded to the current ping
received_pong=False
# -1 means pinging is not active, [0..) means pinging is active, and counts num missed pings in a row
currently_pinging = -1

# movement object, with initial angle of 0
movement_controller = movement_monitored_ver.Movement()

#connect client and make it wait for inputs
client.connect(ips.ip)
read_battery_status(client) # battery reading thread is started here
client.loop_forever()

################
# robot has three states:
# -- moving - waiting to be told to stop
# -- rotating - using gyro to track whether it's finished
# -- waiting - ready to receive a fresh instruction

# During moving, the robot sends pings every three seconds, listening for pongs from vision
# If x are missed in a row, the robot stops, and asks for the next instruction. This is to
# prevent the robot crashing if the vision system stops working
################
