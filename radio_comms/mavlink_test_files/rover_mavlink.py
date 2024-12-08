from pymavlink import mavutil

#CONN_STR = "udpin:localhost:12345"
CONN_STR = "/dev/cu.usbserial-BG00HO5R"

connection = mavutil.mavlink_connection(CONN_STR)

while True:
    connection.wait_heartbeat()
    print(f"heartbeat from system (system {connection.target_system}, component {connection.target_component})")


#connection.mav.system_time_send(time_unix_usec, time_boot_ms)