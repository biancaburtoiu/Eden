import ev3dev.ev3 as ev3
import sys
#motor = sys.argv[2]
motors = []

for i in range(1,len(sys.argv)):
  motors.append(ev3.LargeMotor('out'+sys.argv[i]))

while True:
    inputs = input("e:").split(" ") 
    if inputs[0]=='c' :
        for m in motors:
            m.run_forever(speed_sp=int(inputs[1]))
    elif inputs[0]=='t':
        for m in motors:
            m.run_timed(speed_sp=int(inputs[1]), time_sp=int(inputs[2]))
    elif inputs[0] =='s':
        for m in motors:
            m.run_timed(speed_sp=0, time_sp=0)
    else:
        print("NOT WELL FORMED")
