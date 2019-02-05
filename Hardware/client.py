import run_motors
import paho.mqtt.client as mqtt
import sys
import ev3dev.ev3 as ev3



client=mqtt.Client("ev3")




def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)
    client.subscribe("move")
def onMessage(client,userdata,msg):
    print(msg.topic+" "+str(msg.payload))
    arguements=msg.payload.decode("ascii").split(",")
    arguements=[int(x) for x in arguements]
    print(arguements)
    if msg.topic=="move":
        print("moving")
        run_motors.move(arguements[0],arguements[1],arguements[2])
        print("moved")

client.on_connect=onConnect
client.on_message=onMessage
client.connect("129.215.202.200")
#client.connect("localhost")

client.loop_forever()
