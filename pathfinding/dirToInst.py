def orient_self(direction, robot_orientation, instructions_list):
    # number directions to allow orientation by subtracting
    robot_dir_num = dirs_to_ints[robot_orientation]
    direction_num = dirs_to_ints[direction]

    # turns difference in direction into degrees TO THE RIGHT to turn
    degrees_to_turn = 90*((direction_num-robot_dir_num) % 4)
    
    #if this is > 180, go the other way instead
    if degrees_to_turn>180:
        degrees_to_turn = degrees_to_turn-360

    add_turn_instruction(degrees_to_turn, instructions_list)

def add_turn_instruction(degrees, instructions_list):
    instructions_list.append(('r',degrees))

def add_move_instruction(squares, instructions_list):
    instructions_list.append(('m',squares))

# while dirs_list
    # orient self
    # keep taking instructions until orientation changes

dirs_to_ints = {'u':0,'r':1,'d':2,'l':3}

def main(dirs_list):
    instructions_list = []

    if(dirs_list is not None and len(dirs_list)>0):
        # we track subsequent squares in the same direction
        squares_to_move=0

        #first we tell the robot how to orient itself initally
        # note the first direction is not consumed yet (as we haven't moved)
        robot_orientation = dirs_list[0]
        instructions_list.append(robot_orientation)

        # read list backwards so we can use .pop()
        dirs_list.reverse()

        # now, take directions until we run out of them
        while len(dirs_list)>0:
            current = dirs_list.pop()

            if current!=robot_orientation:
                # add squares to far as one move inst,
                # note there should never be two subsequent rotations
                if squares_to_move:
                    add_move_instruction(squares_to_move, instructions_list)

                # turn to match new direction of travel
                orient_self(current,robot_orientation, instructions_list)
                robot_orientation = current # we are now facing this direction

                # we must move at least once following the direction change,
                # otherwise, all we did was turn on the spot [:(]
                squares_to_move = 1
            else:
                # keep counting up movement in this direction
                squares_to_move+=1

        # we must add any remaining move insts since last rotation
        if squares_to_move:
            add_move_instruction(squares_to_move, instructions_list)

    return instructions_list
        

