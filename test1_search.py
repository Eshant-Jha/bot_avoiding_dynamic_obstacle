# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 20:31:41 2023

@author: OE22S300
"""

import math
import numpy as np

import operator
heusritic_weight =  2.0

def heuristic_1(problem, state, heusritic_weight):
    """
    Manhattan distance
    """
    goal = problem.getGoalState()
    del_x_1 = abs(state[0] - goal[0])
    del_y_1 = abs(state[1] - goal[1])
    
    return heusritic_weight*(del_x_1 + del_y_1 )






def aStarSearch(problem):
  "Search the node that has the lowest combined cost and weighted heuristic first."
  #Create explored list to store popped nodes
  explored = []
  #Create Fringe to store all nodes to be expaned
  fringe = []
  #Add the start state to Fringe 
  fringe.append([problem.getStartState(), [], 0, (heuristic_1(problem, problem.getStartState(), heusritic_weight))+0])
 
  i = 1 #count number of nodes expanded

  print("Planning...")  
  
  
  while len(fringe)>0:
      
      #print("Number of nodes expanded:", i)
      
      
      fringe = sorted(fringe, key = operator.itemgetter(3))
      
     
      #Pop least cost node and add to explored list
      current_node = fringe.pop(0)
      i = i+1
      explored.append(current_node[0]) # only the state needs to be added to explored list 
      
   
     
      if problem.isGoalState(current_node[0]):
          
        path_coordinates = []
        current_state = problem.getStartState()
        for action in current_node[1]:
            if action == 'stop':
                path_coordinates.append(current_state)
            else:
                successors = problem.getSuccessors(current_state)
                for successor, successor_action, _ in successors:
                    if successor_action == action:
                        path_coordinates.append(successor)
                        current_state = successor
                        break
        return path_coordinates

        
          
          
         
     
      #Expand node and get successors 
      for successor, action, cost in problem.getSuccessors(current_node[0]):
         
          g = current_node[2] + cost
          h = heuristic_1(problem, successor, heusritic_weight)
          path = current_node[1] + [action]
          temp_node = [successor, path, g, h+g,]
          
         
          
          #Check if the successor already exists in explored list
          if successor in explored:
              continue #If so already optimal do not add to list
          
          #Check if duplicate node exists in fringe
          flag_do_not_append = False
          for node in fringe:        
              if node[0] == successor:                  
                  #Check if existing duplicate is actually shorter path than the new node            
                  if node[2] <= temp_node[2]:
                      #In this case do not add the new node to fringe 
                      flag_do_not_append = True
                      #No need to check further in existing fringe
                      break
          
          if flag_do_not_append:
              #In this case do not add the new node 
              continue
          
          #If none of the above then add successor to fringe 
          
          fringe.append(temp_node)
          
         
  return ([])  

