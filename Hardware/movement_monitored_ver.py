import ev3dev.ev3 as ev3
import time

# =============== class for controlling ev3 movement =================== #
class Movement:
    def __init__(self,initial_angle):
        self.angle = initial_angle
        # note gyro angle is NOT representitive of robot's real angle
        self.gyro = gyro=ev3.GyroSensor('in1')
        self.gyro.mode="GYRO-ANG"
        self.motors = setupMotors()
        self.start_arm_pos=self.motors[2].position

    def relative_turn(self,degrees):
        # we will measure difference in gyro angle from start to finish
        current_gyro_angle = self.gyro.angle
        target_gyro_angle = degrees + current_gyro_angle

        print("facing: %s,   turning to: %s"%(current_gyro_angle,target_gyro_angle))
        # ##
        # i=0
        # print("c: %s \t t: %s"%(current_gyro_angle,target_gyro_angle))
        # ##
        if degrees>=0:
            # turn right
            self.motors[0].run_forever(speed_sp=-300)
            self.motors[1].run_forever(speed_sp=300)
        else:
            # turn left
            self.motors[0].run_forever(speed_sp=300)
            self.motors[1].run_forever(speed_sp=-300)

        # wait until gyro has changed by target amount
        while abs(current_gyro_angle-target_gyro_angle)>2:
            # ###
            # if (i%10==0):
            #     print("c: %s  t: %s abs: %s "%(current_gyro_angle,target_gyro_angle,abs(current_gyro_angle-target_gyro_angle)))
            # i+=1
            # ###
            current_gyro_angle = self.gyro.angle
            time.sleep(0.00001)


        # stop the motors
        self.motors[0].run_timed(speed_sp=0,time_sp=0)
        self.motors[1].run_timed(speed_sp=0,time_sp=0)

        # update the internal measure of angle
        self.angle+=degrees
        print("finished turn, facing: %s"%(self.angle))

    def absolute_turn(self,degrees):
        # ###
        # print("degrees: %s"%degrees)
        # print("current angle: %s"%self.angle)
        # ###
        rel_angle = rel_from_abs_turn(degrees,self.angle)
        self.relative_turn(rel_angle)

    def forward_forever(self):
        print("beginning to move forever")
        self.motors[0].run_forever(speed_sp=1000,stop_action="brake")
        self.motors[1].run_forever(speed_sp=1000,stop_action="brake")

    def stop(self):
        print("stopping motors")
        self.motors[0].run_timed(speed_sp=0,time_sp=0)
        self.motors[1].run_timed(speed_sp=0,time_sp=0)

    def arm_to_pos(self, degrees):
        self.motors[2].run_to_abs_pos(position_sp=self.start_arm_pos-degrees,speed_sp=50)

# =============helpers=================================================== #

# registers motors - must be plugged in to A and B !
def setupMotors():
    motors = []
    motors.append(ev3.LargeMotor('outA'))
    motors.append(ev3.LargeMotor('outB'))
    motors.append(ev3.LargeMotor('outC'))
    return motors

# derive a relative turn from absolute current and target angles
def rel_from_abs_turn(target_angle,current_angle):
    #rel turn from absolute formula
    rel_angle = (target_angle-current_angle) % 360

    if rel_angle<=180:
        # rel angle in [0,180]
        return rel_angle
    else:
        # rel angle in (180,360)
        # faster to turn the other way
        return rel_angle - 360
