from pymavlink import mavutil
import pymavlink
import time
import serial
# MAV_TYPE_GROUND_ROVER - 10
# MAV_AUTOPILOT_GENERIC
# MAV_MODE_FLAG_TEST_ENABLED
# MAV_STATE_STANDBY

#CONN_STR = "udpout:localhost:12345"
CONN_STR = "/dev/cu.usbserial-BG00HO5R"

connection = mavutil.mavlink_connection(CONN_STR)

while True:
    time.sleep(1)
    connection.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GROUND_ROVER, mavutil.mavlink.MAV_AUTOPILOT_GENERIC, 
        mavutil.mavlink.MAV_MODE_FLAG_TEST_ENABLED, 0, mavutil.mavlink.MAV_STATE_STANDBY)