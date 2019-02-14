import ev3dev.ev3 as ev3
import sys

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


def turn(speed,degrees):
    target_angle=gyro.angle+degrees
    
    if degrees>=0:
        motors[0].run_forever(speed_sp=speed)
        motors[1].run_forever(speed_sp=-speed)
        while gyro.angle<target_angle:
            print(gyro.angle)
        motors[0].run_timed(speed_sp=0,time_sp=0)
        motors[1].run_timed(speed_sp=0,time_sp=0)
    else:
        motors[0].run_forever(speed_sp=-speed)
        motors[1].run_forever(speed_sp=speed)
        while gyro.angle>target_angle:
            print(gyro.angle)
        motors[0].run_timed(speed_sp=0,time_sp=0)
        motors[1].run_timed(speed_sp=0,time_sp=0)

def linear(speed, mm):
    print(mm/((speed/motors[0].count_per_rot)*45.03))
    motors[0].run_timed(speed_sp=speed, time_sp=1000*(mm/((speed/motors[0].count_per_rot)*45.03)))
    motors[1].run_timed(speed_sp=speed, time_sp=1000*(mm/((speed/motors[1].count_per_rot)*45.03)))

def stop():
    for m in motors:
        m.run_timed(speed_sp=0, time_sp=0)

#add two motors to array, from command line args
#motors[0] is left, motors[1] is right

motors = []
gyro=ev3.GyroSensor('in1')
gyro.mode="GYRO-ANG"
def setupMotors():
    motors.append(ev3.LargeMotor('outA'))
    motors.append(ev3.LargeMotor('outB'))

    #for i in range(1,len(sys.argv)):
    #    motors.append(ev3.LargeMotor('out'+sys.argv[i]))
setupMotors()

def debugfunc():
    while 1: 
        i=input()
        try:
            args=i.split(" ")
            if args[0]=="s":
                linear(int(args[1]),int(args[2]))
            elif args[0]=="r":
                turn(int(args[1]),int(args[2]))
            else:
                print("Malformed")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    debugfunc()
