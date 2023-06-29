# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:04:29 2023

@author: OE22S300
"""
import sim_interface
import control
#Definitions based on color map
r1_start_id = 1
r1_path_id = 2
r1_goal_id = 1

obstacle_id = 16
free_space_id = 3
free_space_cost = 3


class Maps:
    """
    This class outlines the structure of the maps
    """    
    map_data = []
    start = []
    goal = []

#Maze maps
map_1 = Maps()


map_1.map_data = [
     [ 16, 16, 16, 16, 16, 16, 16, 16, 16,  16, 16, 16],
     [ 16,  3, 16,  3,  3,  3,  3,  3,  3,   3,  3, 16],
     [ 16,  3, 16,  3,  3,  3,  3,  3,  3,  16,  3, 16],
     [ 16,  3, 16,  3,  3,  3,  3,  3,  3,  16,  3, 16],
     [ 16,  3, 16,  3,  3,  3,  3,  3,  3,  16,  3, 16],         
     [ 16,  3, 16, 16, 16, 16, 16, 16,  3,  16,  3, 16],
     [ 16,  3, 16,  3,  3,  3,  3,  3,  3,  16,  3, 16],
     [ 16,  3, 16,  3,  3,  3,  3,  3,  3,  16,  3, 16],
     [ 16,  3, 16,  3,  3,  3,  3,  3,  3,  16,  3, 16],
     [ 16,  3, 16,  3,  3,  3,  3,  3,  3,  16,  3, 16],
     [ 16,  3,  3,  3,  3,  3,  3,  3,  3,  16,  3, 16],
     [ 16, 16, 16, 16, 16, 16, 16, 16, 16,  16, 16, 16]]


map_1.r1_start =[0,0]
map_1.r1_goal = [1,9]
maps_dictionary = {1:map_1}