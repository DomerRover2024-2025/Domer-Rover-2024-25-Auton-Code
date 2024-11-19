#!/usr/bin/env python3
import pygame
import socket
import pickle
import serial
import numpy as np
import math
import time
import Jetson.GPIO as GPIO

#one subprocess for connecting controller,one subprocess for 

arduino = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=0,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False,
    writeTimeout=2
)

def valueMap(val):
    return int(val * 255)

def cart2pol(x, y):
    radius = min(math.sqrt(x**2 + y**2), 1)  # Normalize and ceiling to 1
    angle = math.atan2(y, x) * (180 / math.pi)  # Convert angle to degrees
    return (int(255 * radius), int((angle + 360) % 360))


def calcWheelSpeeds(magnitude, angle):
    # Ensure magnitude is between 0 and 1
    magnitude = min(magnitude, 1)

    # Normalize angle to range [0, 360)
    angle = angle % 360

    # Calculate left and right speeds based on angle and magnitude
    if 0 <= angle <= 90:  # Moving forward with right turn
        left_speed = magnitude
        right_speed = magnitude * (angle / 90)
    elif 90 < angle <= 180:  # Moving forward with left turn
        left_speed = magnitude * (1 - (angle - 90) / 90)
        right_speed = magnitude
    elif 180 < angle <= 270:  # Moving backward with left turn
        left_speed = -magnitude * ((angle - 180) / 90)
        right_speed = -magnitude
    else:  # 270 < angle < 360, Moving backward with right turn
        left_speed = -magnitude
        right_speed = -magnitude * (1 - (angle - 270) / 90)
        
    if 150 < angle < 210:			# slowdown conditions on left / right turns - swapping directions could be tough on motors
        right_speed = right_speed * max(0.3, abs(angle-180)/30)
    if angle > 330:
        left_speed = left_speed * max(0.3, abs(angle-360)/30)
    if angle < 30:
        left_speed = left_speed * max(0.3, angle/30)

    return left_speed, right_speed

def sendDriveSignals(left, right):
    dutyCycleLeft = valueMap(left)
    dutyCycleRight = valueMap(right)
        
    print(f"LPower: {left:.3f} RPower: {right:.3f} dutyLeft: {dutyCycleLeft} dutyRight: {dutyCycleRight}, ")
    # print("Duty Cycle Left:", dutyCycleLeft, "   Duty Cycle Right:", dutyCycleRight, "   axis: ", a_leftx1)
        
    arduino_data = f"{dutyCycleLeft} {dutyCycleRight}\n"
    arduino.write(arduino_data.encode())  # Send as bytes to Arduino
    
    return dutyCycleLeft, dutyCycleRight



class TextPrint: # not necessary, for ensuring correct input
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10
        
        
host = "10.7.4.66" 
port = 8088

pygame.init()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(2)

conn, addr = s.accept()

screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption("Joystick example")

clock = pygame.time.Clock()
text_print = TextPrint()
triggerMult = 1	# init magnitude scalar
stopFlag = False


try:
    while True:
        screen.fill((255, 255, 255))		#not necessary - ensure correct input
        text_print.reset()					#not necessary - ensure correct input
        
        data = conn.recv(4096)
        if not data:
            break

        joystick_data = pickle.loads(data)

        a_lt1 =         joystick_data[0]
        a_rt1 =         joystick_data[1]
        b_lbumper1 =    joystick_data[2]
        b_rbumper1 =    joystick_data[3] 
        a_leftx1 =      joystick_data[4]
        a_lefty1 =      joystick_data[5]
        a_rightx1 =     joystick_data[6]
        a_righty1 =     joystick_data[7]
        b_leftIn1 =     joystick_data[8]
        b_rightIn1 =    joystick_data[9]  
        b_x1 =          joystick_data[10] 
        b_circle1 =     joystick_data[11] 
        b_square1 =     joystick_data[12]  
        b_triangle1 =   joystick_data[13] 
        b_padUp1 =      joystick_data[14]  
        b_padDown1 =    joystick_data[15]  
        b_padLeft1 =    joystick_data[16] 
        b_padRight1 =   joystick_data[17]
        
        mag, angle = cart2pol(a_leftx1, a_lefty1)
        angleRads = math.radians(angle)
        
        triggerMult = triggerMult - a_lt1*0.001 + a_rt1*0.001	#adjust magnitude scalar with triggers (0-2), left decrease, right increase, cancel each other out
        
        triggerMult = max(0.1, min(triggerMult, 2))	#limit to 0.1x to 2x
        
        if b_padUp1 == 1:		# presets - will need sleep() after sending signals w/ time hyperparameter (5secs?)
            pass
        if b_padDown1 == 1:
            pass
        if b_padLeft1 == 1:
            pass
        if b_padRight1 == 1:
            pass
        




        left_power, right_power = calcWheelSpeeds(mag, angle)
        if b_leftIn1 == 1 and stopFlag == False:
            stopFlag = True
            
        if stopFlag == True:
            left_power, right_power = 0, 0
        
        
        
        
        
        dutyCycleLeft, dutyCycleRight = sendDriveSignals(left_power, right_power)
        
        if arduino.in_waiting > 0:		# ensure arduino is reading
            arduino_feedback = arduino.readline().decode().strip()
            print("Arduino Feedback:", arduino_feedback)
            text_print.tprint(screen, f"Arduino Feedback: {arduino_feedback}")

        text_print.tprint(screen, f"Duty Cycle: {dutyCycleLeft}")
        pygame.display.flip()
    
        clock.tick(20)

finally:
    arduino.close()
    conn.close()
    s.close()



# overall speed var (0-2)
# hyperparameter - constant to increment by (0.005, 0.01)
# speedVar = speedVar + constant*rightTrigger - constant*leftTrigger
#   right and left trigger (0-2)
# 	if both triggers unpressed, ==0, no change
# 	upon trigger press, incremented with magnitude corrersponding to trigger press
# 
# 
# 
# 
