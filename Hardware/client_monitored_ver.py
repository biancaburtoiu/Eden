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

    ###garbage###
    ev3.Sound.speak("EDEN")
    #############

def onMessage(client,userdata,msg):
    try:
        if msg.topic=="start-instruction":
            # single instruction:
            # - face direction, start moving, stop moving, or rotate
            instruction_to_follow = msg.payload.decode().strip()
            follow_one_instruction(instruction_to_follow)
        if msg.topic=="arm":
            movement_controller.arm_to_pos(float(msg.payload.decode()))
    except:
        # catch any errors to stop alertless crashing
        print("Error")
        traceback.print_exc()
        sys.exit()
        

def follow_one_instruction(instruction_as_string):
    print("about to follow instruction: %s"%instruction_as_string)
    global currently_moving

    if currently_moving:
        # stop (moving) instruction
        if instruction_as_string=='s':
            currently_moving = False
            movement_controller.stop()
            ask_for_next_inst(movement_controller.angle)
        else:
            print("useless instruction: %s"%instruction_as_string)
    else:
        # fresh instruction / not a stop instruction

        # absolute turn instructions ( first inst received)
        if instruction_as_string in ['u','d','l','r']:
            currently_moving=True
            if instruction_as_string=='u':
                movement_controller.absolute_turn(0)
            elif instruction_as_string=='r':
                movement_controller.absolute_turn(90)
            elif instruction_as_string=='d':
                movement_controller.absolute_turn(180)
            elif instruction_as_string=='l':
                movement_controller.absolute_turn(270)
            ask_for_next_inst(movement_controller.angle)
        # movement / relative turn instructions (subsequent insts)
        elif instruction_as_string == 's':
            # received a stop when we're already stopped!
            print("ignoring useless s instruction")
        else:
            # tuple received is either 'u','d','l','r', or
            # in form (r,[degrees]), or (m,[squares])
            # note the number of squares is unused for the main navigation
            (inst_type,inst_val) = tuple(instruction_as_string.split(","))
            inst_val = int(inst_val)
            if inst_type=='m':
                currently_moving=True
                movement_controller.forward_forever()
            elif inst_type=='r':
                currently_moving=True
                movement_controller.relative_turn(inst_val)
                ask_for_next_inst(movement_controller.angle)
            else:
                print("received a malformed instruction!: %s"%instruction_as_string)

def ask_for_next_inst(current_angle):
    global currently_moving
    currently_moving = False
    print("about to send finish-instruction ",current_angle)
    client.publish("finish-instruction",str(current_angle),qos=2)
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
currently_moving = False

# movement object, with initial angle of 0
movement_controller = movement_monitored_ver.Movement(0)

#connect client and make it wait for inputs
client.connect(ips.ip)
read_battery_status(client) # battery reading thread is started here
client.loop_forever()

################
# robot has three states:
# -- moving - waiting to be told to stop
# -- rotating - using gyro to track whether it's finished
# -- waiting - ready to receive a fresh instruction
################
