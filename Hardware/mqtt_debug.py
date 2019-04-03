"""provides a remoteMove method and a debug to access it"""

import paho.mqtt.client as mqtt
import ips

def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)

client=mqtt.Client("desktopMachine")

client.on_connect=onConnect
client.connect(ips.ip)

client.loop_start()
def remoteMove(insts_string):
    """send a command to the ev3 to move remotely"""
    client.publish("instructions",insts_string)

def debugfunc():
    while True:
        ##wait for input
        inputs = input("e:").split(" ")

        ##check input format, and perform action
        client.publish(inputs[0],inputs[1].encode())

if __name__ == "__main__":
    debugfunc()
