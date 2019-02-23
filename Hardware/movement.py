import ev3dev.ev3 as ev3

# =============== class for controlling ev3 movement =================== #
class Movement:
    def __init__(self,initial_angle):
        self.angle = initial_angle
        # note gyro angle is NOT representitive of robot's real angle
        self.gyro = gyro=ev3.GyroSensor('in1')
        self.gyro.mode="GYRO-ANG"
        self.motors = setupMotors()
        self.time_per_square = 750
    
    def relative_turn(self,degrees):
        # we will measure difference in gyro angle from start to finish
        current_gyro_angle = self.gyro.angle
        target_gyro_angle = degrees + current_gyro_angle

        print("facing: %s,   turning to: %s"%(current_gyro_angle,target_gyro_angle))
        
        if degrees>=0:
            # turn right
            self.motors[0].run_forever(speed_sp=200)
            self.motors[1].run_forever(speed_sp=-200)
        else:
            # turn left
            self.motors[0].run_forever(speed_sp=-200)
            self.motors[1].run_forever(speed_sp=200)

        # wait until gyro has changed by target amount
        while abs(current_gyro_angle-target_gyro_angle)>2:
            current_angle = self.gyro.angle

        # stop the motors
        self.motors[0].run_timed(speed_sp=0,time_sp=0)
        self.motors[1].run_timed(speed_sp=0,time_sp=0)

        # update the internal measure of angle
        self.angle=current_angle
        print("finished turn, facing: %s"%(self.angle))
    
    def absolute_turn(self,degrees):
        rel_angle = rel_from_abs_turn(degrees,self.angle)
        self.relative_turn(rel_angle)

    def forward(self,num_squares):
        print("beginning to move %s squares"%num_squares)
        self.motors[0].run_timed(time_sp=num_squares*self.time_per_square, speed_sp=1000, stop_action="brake")
        self.motors[1].run_timed(time_sp=num_squares*self.time_per_square, speed_sp=1000, stop_action="brake")
        
        # no more instructions can interrupt this
        self.motors[0].wait_while("running")
        
        print("finished moving!")

# =============helpers=================================================== # 

# registers motors - must be plugged in to A and B !
def setupMotors():
    motors = []
    motors.append(ev3.LargeMotor('outA'))
    motors.append(ev3.LargeMotor('outB'))
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