import numpy as np
import robot_params
import math

try:
  import sim
except:
  print ('--------------------------------------------------------------')
  print ('"sim.py" could not be imported. This means very probably that')
  print ('either "sim.py" or the remoteApi library could not be found.')
  print ('Make sure both are in the same folder as this file,')
  print ('or appropriately adjust the file "sim.py"')
  print ('--------------------------------------------------------------')
  print ('')

client_ID = []


def sim_init():
  global sim
  global client_ID
  
  #Initialize sim interface
  sim.simxFinish(-1) # just in case, close all opened connections
  client_ID=sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim    
  if client_ID!=-1:
    print ('Connected to remote API server')
    return True
  else:
    return False

def get_handles():
  #Get the handles to the sim items

  global pioneer_handle
  global pioneer_left_motor_handle
  global pioneer_right_motor_handle
  global bill1_handle
  global bill2_handle

  # Handle to Pioneer1:
  res , pioneer_handle = sim.simxGetObjectHandle(client_ID, "/Pioneer1", sim.simx_opmode_blocking)
  res,  pioneer_left_motor_handle = sim.simxGetObjectHandle(client_ID, "/Pioneer1/left", sim.simx_opmode_blocking)
  res,  pioneer_right_motor_handle = sim.simxGetObjectHandle(client_ID, "/Pioneer1/right", sim.simx_opmode_blocking)
  
  # Get the position of the Pioneer1 for the first time in streaming mode
  res , pioneer_1_Position = sim.simxGetObjectPosition(client_ID, pioneer_handle, -1 , sim.simx_opmode_streaming)
  res , pioneer_1_Orientation = sim.simxGetObjectOrientation(client_ID, pioneer_handle, -1 , sim.simx_opmode_streaming)
  
  # Stop all joint actuations:Make sure Pioneer1 is stationary:
  res = sim.simxSetJointTargetVelocity(client_ID, pioneer_left_motor_handle, 0, sim.simx_opmode_streaming)
  res = sim.simxSetJointTargetVelocity(client_ID, pioneer_right_motor_handle, 0, sim.simx_opmode_streaming)
  
  # Handle to Bills:
  res , bill1_handle = sim.simxGetObjectHandle(client_ID, "/Bill0/Bill", sim.simx_opmode_blocking)
  res , bill2_handle = sim.simxGetObjectHandle(client_ID, "/Bill1/Bill", sim.simx_opmode_blocking)
  
  # Get the position of the Bills for the first time in streaming mode
  res , pioneer_1_Position = sim.simxGetObjectPosition(client_ID, bill1_handle, -1 , sim.simx_opmode_streaming)
  res , pioneer_1_Position = sim.simxGetObjectPosition(client_ID, bill2_handle, -1 , sim.simx_opmode_streaming)
  
  print ("Succesfully obtained handles")

  return

def start_simulation():
  global sim
  global client_ID

  ###Start the Simulation: Keep printing out status messages!!!
  res = sim.simxStartSimulation(client_ID, sim.simx_opmode_oneshot_wait)

  if res == sim.simx_return_ok:
    print ("---!!! Started Simulation !!! ---")
    return True
  else:
    return False

def localize_robot():
  #Function that will return the current location of Pioneer
  #PS. THE ORIENTATION WILL BE RETURNED IN RADIANS        
  global sim
  global client_ID
  global pioneer_handle
  
  res , pioneer_Position = sim.simxGetObjectPosition(client_ID, pioneer_handle, -1 , sim.simx_opmode_buffer)
  res , pioneer_Orientation = sim.simxGetObjectOrientation(client_ID, pioneer_handle, -1 , sim.simx_opmode_buffer)
  
  x = pioneer_Position[0]
  y = pioneer_Position[1]
  theta  =pioneer_Orientation[2]
  print("robot", x , y)

  return [x,y,theta]   

def localize_bills():
    #Function that will return the current location of Bills      
    global sim
    global client_ID
    global bill1_handle
    global bill2_handle
    
    res , bill1_Position = sim.simxGetObjectPosition(client_ID, bill1_handle, -1 , sim.simx_opmode_buffer)
    res , bill2_Position = sim.simxGetObjectPosition(client_ID, bill2_handle, -1 , sim.simx_opmode_buffer)
    
    print("bill1", int(bill1_Position[0]) , int(bill1_Position[1]))
    print("bill2", int(bill2_Position[0]) , int(bill2_Position[1]))

    return [[bill1_Position[0], bill1_Position[1]], [bill2_Position[0], bill2_Position[1]]]          

def setvel_pioneers(V, W):
  #Function to set the linear and rotational velocity of pioneers
  global sim
  global client_ID
  global pioneer_left_motor_handle
  global pioneer_right_motor_handle

  # Limit v,w from controller to +/- of their max
  w = max(min(W, robot_params.pioneer_max_W), -1.0*robot_params.pioneer_max_W)
  v = max(min(V, robot_params.pioneer_max_V), -1.0*robot_params.pioneer_max_V)
          
  # Compute desired vel_r, vel_l needed to ensure w
  Vr = ((2.0*v) + (w*robot_params.pioneer_track_width))/(2*robot_params.pioneer_wheel_radius)
  Vl = ((2.0*v) - (w*robot_params.pioneer_track_width))/(2*robot_params.pioneer_wheel_radius)
                      
  # Set velocity
  sim.simxSetJointTargetVelocity(client_ID, pioneer_left_motor_handle, Vl, sim.simx_opmode_oneshot_wait)
  sim.simxSetJointTargetVelocity(client_ID, pioneer_right_motor_handle, Vr, sim.simx_opmode_oneshot_wait)
  
  return  

def sim_shutdown():
  #Gracefully shutdown simulation

  global sim
  global client_ID

  #Stop simulation
  res = sim.simxStopSimulation(client_ID, sim.simx_opmode_oneshot_wait)
  if res == sim.simx_return_ok:
    print ("---!!! Stopped Simulation !!! ---")

  # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
  sim.simxGetPingTime(client_ID)

  # Now close the connection to CoppeliaSim:
  sim.simxFinish(client_ID)      

  return            
