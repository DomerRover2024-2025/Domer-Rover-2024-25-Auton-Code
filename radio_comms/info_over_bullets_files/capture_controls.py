import pygame
import pickle
import numpy as np
import time
import math

def deadzone(button):
    c_deadzone = 0.05
    c_roundAxis = 4

    if abs(button) < c_deadzone:
        return 0
    else:
        return round(button, c_roundAxis)


def init():
    # initialization
    joysticks = {}
    return joysticks #, text_print, screen

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
            
    return dutyCycleLeft, dutyCycleRight

def run(joysticks, triggerMult, stopFlag):
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        if not joysticks:
            print("No joystick connected. Waiting...")
            time.sleep(3)
            continue
        # joystick 1 sets joystick buttons / axis to values

        if 0 in joysticks:
            guid = joysticks[0].get_guid()

        a_lt1 = deadzone(joysticks[0].get_axis(4) + 1)
        a_rt1 = deadzone(joysticks[0].get_axis(5) + 1)
        
        b_lbumper1 = joysticks[0].get_button(9)
        b_rbumper1 = joysticks[0].get_button(10)

        a_leftx1 = deadzone(joysticks[0].get_axis(0))
        a_lefty1 =  deadzone(joysticks[0].get_axis(1) * -1)

        a_rightx1 = deadzone(joysticks[0].get_axis(2))
        a_righty1 =  deadzone(joysticks[0].get_axis(3) * -1)

        b_leftIn1 = joysticks[0].get_button(7)
        b_rightIn1 = joysticks[0].get_button(8)

        b_x1 = joysticks[0].get_button(0)
        b_circle1 = joysticks[0].get_button(1)
        b_square1 = joysticks[0].get_button(2)
        b_triangle1 = joysticks[0].get_button(3)

        b_padUp1 = joysticks[0].get_button(11)
        b_padDown1= joysticks[0].get_button(12)
        b_padLeft1 = joysticks[0].get_button(13)
        # b_padRight1 = joysticks[0].get_button(14)

        # b_touchpad1 = joysticks[0].get_button(15)

        mag, angle = cart2pol(a_leftx1, a_lefty1)
        angleRads = math.radians(angle)

        triggerMult = triggerMult - a_lt1*0.001 + a_rt1*0.001	#adjust magnitude scalar with triggers (0-2), left decrease, right increase, cancel each other out
        
        triggerMult = max(0.1, min(triggerMult, 2))	#limit to 0.1x to 2x for speed scalar
        
        if b_padUp1 == 1:		# presets - will need sleep() after sending signals w/ time hyperparameter (5secs?)
            pass
        if b_padDown1 == 1:
            pass
        if b_padLeft1 == 1:
            pass
        # if b_padRight1 == 1:
        #     pass
        
        left_power, right_power = calcWheelSpeeds(mag, angle)
        if b_leftIn1 == 1 and stopFlag == False:
            stopFlag = True
            
        if stopFlag == True:
            left_power, right_power = 0, 0
        
        time.sleep(0.75)
        dutyCycleLeft, dutyCycleRight = sendDriveSignals(left_power, right_power)

        yield (dutyCycleLeft, dutyCycleRight, triggerMult, b_padUp1, b_padDown1)

        # ************************
        # for 6 wheel individual inputs, add indiv wheel speed variables to publisher, use testController3 arduino code
        # adapt calcWheelSpeed for indiv speeds
		# ************************
        
        # ***********************
        # HENRY - variables are [dutyCycleLeft, dutyCycleRight, triggerMult, b_padUp1, b_padDown1]
        # will have to pygame.init and pygame.joystick.init + run joysticks command correctly

def main():
    # host = "10.7.4.66"
    # port = 8088

    rclpy.init()
    #create nodes
    joystickNode = TalkerNode()

    pygame.init()
    pygame.joystick.init()
    # joysticks = init()
    joysticks = {}
    run(joysticks, 1, stopFlag=False)
    pygame.quit()

    joystickNode.destroy_node()
    #subscriberNode.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()



