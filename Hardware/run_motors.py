import ev3dev.ev3 as ev3
import sys
#motor = sys.argv[2]

def move(rotate,speed,time):
    if speed>1050 or speed < -1050:
        #speed must be in range [-1050,1050]
        print("too fast")
    elif time<0:
        # flag for constant movement
        if rotate:
            motors[0].run_forever(speed_sp=speed)
            motors[1].run_forever(speed_sp=-speed)
        else:
            motors[0].run_forever(speed_sp=speed)
            motors[1].run_forever(speed_sp=speed)
    else:
        #timed movement
        if rotate:
            motors[0].run_timed(speed_sp=speed, time_sp=time)
            motors[1].run_timed(speed_sp=-speed, time_sp=time)
        else:
            motors[0].run_timed(speed_sp=speed, time_sp=time)
            motors[1].run_timed(speed_sp=speed, time_sp=time)


def stop():
    for m in motors:
        m.run_timed(speed_sp=0, time_sp=0)

#add two motors to array, from command line args
#motors[0] is left, motors[1] is right

motors = []
def setupMotors():
    motors.append(ev3.LargeMotor('outA'))
    motors.append(ev3.LargeMotor('outB'))
    #for i in range(1,len(sys.argv)):
    #    motors.append(ev3.LargeMotor('out'+sys.argv[i]))
setupMotors()

def debugfunc():
    while True:
        ##wait for input
        inputs = input("e:").split(" ")

        ##check input format, and perform action
        if inputs[0]=='m':
            if inputs[1]=='c' :
                speed = int(inputs[2])
                move(False,speed,-1)
            elif inputs[1]=='t':
                speed = int(inputs[2])
                time = int(inputs[3])
                move(False,speed,time)
            else:
                print("NOT WELL FORMED")
        elif inputs[0]=='r':
            if inputs[1]=='c' :
                speed = int(inputs[2])
                move(True,speed,-1)
            elif inputs[1]=='t':
                speed = int(inputs[2])
                time = int(inputs[3])
                move(True,speed,time)
            else:
                print("NOT WELL FORMED")
        elif inputs[0] =='s':
            stop()
        else:
            print("NOT WELL FORMED")

if __name__ == "__main__":
    debugfunc()
