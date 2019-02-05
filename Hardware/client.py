import run_motors
import paho.mqtt.client as mqtt
client=mqtt.Client("ev3")

def onConnect(client,userdata,flags,rc):
    print("connected with result code %i" % rc)
    client.subscribe("move")
def onMessage(client,userdata,msg):
    print(msg.topic+" "+str(msg.payload))
    print(msg.payload)
    if msg.topic=="move":
        run_motors.move(*(msg.payload.split(",")))

client.on_connect=onConnect
client.on_message=onMessage
client.connect("192.168.17.130")
#client.connect("localhost")

client.loop_forever()
