#!/usr/bin/env python

"""
Mobile robot simulation setup
@author: Eshant
"""
import test1_search

import test1_maze
import test1_maze_map
import time

#Import files
import sim_interface
import control
import math

def main():
    if (sim_interface.sim_init()):

        #Obtain handles to sim elements
        sim_interface.get_handles()

        #Start simulation
        if (sim_interface.start_simulation()):
            
            #Stop robot
            sim_interface.setvel_pioneers(0.0, 0.0)
            
            current_maze=test1_maze.Maze(1)
            robot_state = sim_interface.localize_robot()
           
            current_maze.test1_maze_map.r1_start = [round(robot_state[0]), round(robot_state[1])]
            goal_state = current_maze.test1_maze_map.r1_goal
           
           
            while robot_state != goal_state:
                
                print("fianl destinatiom",goal_state)
                r_path=test1_search.aStarSearch(current_maze)
                next_state = r_path[0]
                
                k=sim_interface.localize_bills()
                                   
                                     
                if (abs(k[0][0] - next_state[0]) + abs(k[0][1] - next_state[1])) <2 or (abs(k[1][0] - next_state[0]) + abs(k[1][1] - next_state[1])) <2:   #if close to bill
                   print("obstacle near by wait") 
                   
                   
                   sim_interface.setvel_pioneers(0.0, 0.0)
                   time.sleep(0.5)
                   continue
            
                else:    
                    
                    [V,W] = control.gtg(robot_state, next_state)
                    sim_interface.setvel_pioneers(V, W)
                    time.sleep(0.5)
                    robot_state = sim_interface.localize_robot()
                    current_maze.test1_maze_map.r1_start = [round(robot_state[0]), round(robot_state[1])]
                
                
            #Stop robot
            sim_interface.setvel_pioneers(0.0, 0.0)

        else:
            print ('Failed to start simulation')
    else:
        print ('Failed connecting to remote API server')
    
    #stop robots
    sim_interface.setvel_pioneers(0.0, 0.0)
    sim_interface.sim_shutdown()
    time.sleep(2.0)
    return

#run
if __name__ == '__main__':

    main()                    
    print ('Program ended')
            

 
