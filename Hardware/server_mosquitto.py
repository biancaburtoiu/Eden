"""provides a remoteMove method and a debug to access it"""

import paho.mqtt.client as mqtt

def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)

client=mqtt.Client("desktopMachine")

client.on_connect=onConnect
client.connect("129.215.3.65")


client.subscribe("navigate-finish")

def on_message(cl,ud,fl):
    print("FINISHED UWU")



client.loop_start()
def remoteMove(insts_string):
    """send a command to the ev3 to move remotely"""
    client.publish("instructions",insts_string)

def debugfunc():
    while True:
        ##wait for input
        inputi = input("e:").strip().split("\n")

        ##check input format, and perform action
        client.publish("navigate-finish",inputi[0].encode())

if __name__ == "__main__":
    debugfunc()
