# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 21:26:13 2023

@author: OE22S300
"""
import matplotlib

import time
import copy
import test1_maze_map
import matplotlib.pyplot as plt

class Maze:
  """
  This class outlines the structure of the maze problem
  """
  
  test1_maze_map = []# To store map data, start and goal points
  

  # [delta_x, delta_y, description]
  five_neighbor_actions = {'up':[-1, 0], 'down':[1, 0], 'left': [0, -1], 'right': [0, 1], 'stop': [0, 0]}
  #eight_neighbor_actions = {'up':[-1, 0], 'down':[1, 0], 'left': [0, -1], 'right': [0, 1], 'stop': [0, 0], 
  #                        'upright':[-1, 1], 'upleft':[-1, -1], 'downright':[1, 1], 'downleft':[1, -1]}
  
  #Setup plot
  map_plot_copy = []
  plot_colormap_norm = matplotlib.colors.Normalize(vmin=0.0, vmax=29.0)
  fig,ax = plt.subplots(1)
  plt.axis('equal')
  
  

  def plot_map(self):
      """
      Plot
      """
      #Plotting robot 1
      start = self.getStartState()
      goal = self.getGoalState()
      self.map_plot_copy[start[0]][start[1]] = test1_maze_map.r1_start_id
      self.map_plot_copy[goal[0]][goal[1]] = test1_maze_map.r1_goal_id
      
      
      plt.imshow(self.map_plot_copy, cmap=plt.cm.tab20c, norm=self.plot_colormap_norm)
      plt.show()
      
  # default constructor
  def __init__(self, id):
      """
      Sets the map as defined in file maze_maps
      """
      #Set up the map to be used
      self.test1_maze_map = test1_maze_map.maps_dictionary[id]  #changed to test1_maze_map.maps_dictionary from maze_maps.maps
      self.map_plot_copy = copy.deepcopy(self.test1_maze_map.map_data)
      self.plot_map()
      self.count = 0
      return
     
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
 
     start_state = self.test1_maze_map.r1_start 
    
     return start_state
 
  def getGoalState(self):
     """
     Returns the start state for the search problem 
     """
    
     goal_state = self.test1_maze_map.r1_goal
    
     return goal_state
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     print(state)
     if state == self.getGoalState():
         return True
     else:
         return False

  def isObstacle(self, state):
      """
        state: Search state
     
      Returns True if and only if the state is an obstacle
     
      """

      if self.test1_maze_map.map_data[state[0]][state[1]] == test1_maze_map.obstacle_id:
          #print(self.test1_maze_map.map_data[state[0]][state[1]])
          return True
      else:
          return False
      
     
      
  def getSuccessors(self, state):
 
     """
       state: Seacrh state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     successors = []
     for action in self.five_neighbor_actions:
         
         #Get individual action
         del_x, del_y = self.five_neighbor_actions.get(action) 
         
         #Get successor
         new_successor = [state[0] + del_x , state[1] + del_y]    #new_successor = [state[0] + del_x , state[1] + del_y, state[2]+1]
         new_action = action
         
         # Check for static obstacle 
         
         if self.isObstacle(new_successor):
             continue
     
         
         #cost
         new_cost = test1_maze_map.free_space_cost 
             
         successors.append([new_successor, new_action, new_cost])
         
     return successors