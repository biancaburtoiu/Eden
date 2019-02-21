"""provides a remoteMove method and a debug to access it"""

import paho.mqtt.client as mqtt

def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)

client=mqtt.Client("desktopMachine")

client.on_connect=onConnect
client.connect("129.215.202.200")

client.loop_start()
def remoteMove(rotate,speed,time):
    """send a command to the ev3 to move remotely"""
    client.publish("move",'%i,%i,%i'% (rotate,speed,time))
    print('%i,%i,%i'% (rotate,speed,time))

def debugfunc():
    while True:
        ##wait for input
        inputs = input("e:").split(" ")

        ##check input format, and perform action
        client.publish(inputs[0],inputs[1].encode())

if __name__ == "__main__":
    debugfunc()
