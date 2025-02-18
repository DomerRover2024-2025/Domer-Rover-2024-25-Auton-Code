import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/domerrover/Domer-Rover-2024-25-Auton-Code/ws/install/gps_pub_sub'
