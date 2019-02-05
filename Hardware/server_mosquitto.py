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
        if inputs[0]=='m':
            if inputs[1]=='c' :
                speed = int(inputs[2])
                remoteMove(False,speed,-1)
            elif inputs[1]=='t':
                speed = int(inputs[2])
                time = int(inputs[3])
                remoteMove(False,speed,time)
            else:
                print("NOT WELL FORMED")
        elif inputs[0]=='r':
            if inputs[1]=='c' :
                speed = int(inputs[2])
                remoteMove(True,speed,-1)
            elif inputs[1]=='t':
                speed = int(inputs[2])
                time = int(inputs[3])
                remoteMove(True,speed,time)
            else:
                print("NOT WELL FORMED")
        elif inputs[0] =='s':
            stop()
        else:
            print("NOT WELL FORMED")

if __name__ == "__main__":
    debugfunc()
