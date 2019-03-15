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
            elif pl=="crashed":
                print("vision system says it's dead")
                on_vision_death()
            else:
                print("useless pong: %s"%pl)

    except:
        # catch any errors to stop alertless crashing
        print("Error")
        traceback.print_exc()
        sys.exit()
        

def follow_one_instruction(instruction_as_string,vision_error=False):
    print("about to follow instruction: %s"%instruction_as_string)
    global currently_moving
    global currently_pinging
    global polling_sonar

    if currently_moving:
        # stop (moving) instruction
        if instruction_as_string=='s':
            # not moving, pinging, or checking sonar  anymore
            currently_moving = False
            currently_pinging = -1
            polling_sonar = False
            movement_controller.stop()
            if not vision_error:
                #request next instruction in path only when stopped 
                # by vision system - not on a self-stop due to lack of pongs
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

                # start checking sonar regularly while we're moving
                polling_sonar = True
                poll_sonar()

                movement_controller.forward_forever()

                # send first ping to start playing
                #send_ping()
                
                # start checking sonar regularly while we're moving
                #polling_sonar = True
                #poll_sonar_mainthread()
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
    if currently_pinging>=0:
        if received_pong:
            #reset missed ping count, and send the next ping
            currently_pinging = 0
            received_pong = False
            send_ping()
        else:
            #a pong has not been sent in time!
            currently_pinging+=1

            if currently_pinging==5:
                # stop the robot due to x missed pongs.
                # pings will now stop, and currently_pinging will be set to -1
                print("five pings! stopping!")
                follow_one_instruction("s",True)
            else:
                # we've acknowledged the missed pong, but keep trying 
                print("%s missed pongs"%currently_pinging)
                received_pong=False
                send_ping()

#called when vision system tells us explicitely it's dead. Instead of
# waiting for next pong check, we just stop immediately
def on_vision_death():
    # stop pinging process, now even when next pong isn't received,
    # check_for_pong() does nothing. This is because robot stopping
    # has already been sorted here.
    follow_one_instruction("s",True)

def poll_sonar():
    if polling_sonar:
        if movement_controller.sonar_value()<=80:
            # robot too close to a wall!

            print("SONAR SAYS STOP~~~")
            # this stops robot, but still asks
            # for next instruction
            follow_one_instruction("s")
        else:
            Timer(0.3,poll_sonar).start()

def poll_sonar_mainthread():
    while polling_sonar:
        if movement_controller.sonar_value()<=80:
            print("SONAR SAYS STOP~~~")
            follow_one_instruction("s")
            
            #follow_one_instruction should make polling_sonar false
            # but break just in case
            break
        else:
            time.sleep(0.2)

def send_ping():
    print("ping")

    try:
        client.publish("ping-pong","ping",qos=2)
    except:
        print("couldn't publish ping :(")
    
    #in x seconds check for the pong
    Timer(1,check_for_pong).start()

def ask_for_next_inst():
    global currently_moving
    currently_moving = False
    print("about to send finish-instruction")
    try:
        client.publish("finish-instruction","",qos=2)
    except:
        print("couldn't publish finish-instruction")
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

# tracks whether we should be checking for sonar input
polling_sonar = False

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
