#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from custom_msgs.msg import Coords
import serial
import time
     
class GPSPubNode(Node):
    def __init__(self):
        super().__init__("gps_pub_node")
        
        #self.port_name = self.declare_parameter("port", rclpy.Parameter.Type.STRING)
       
        # Create serial object to communicate with arduino
        self.ser = serial.Serial('/dev/ttyACM2')

        # Coordinate Structure
        self.coordinates = {"latitude": 0.0,
                            "longitude": 0.0,
                            "altitude": 0.0}

        self.publisher_ = self.create_publisher(Coords, "gps_data", 10) # Create publisher object
        time.sleep(3.0) # Sleep for a few seconds so the Arduino can get comms with the GPS set up

        while(not self.ser.is_open): # Wait for port to open
            time.sleep(0.1)     # Wait a bit to not do weird overwhelm stuff

        self.timer_ = self.create_timer(1.0, self.publish_coords) # Create timer to publish coordinates once a second

        self.get_logger().info("Pub sub node started")

    # Helper ftn for publish ftn
    def read_coords(self):
        data = self.ser.readline() # Read line from serial port. Lines come in as a series of bytes, where every 4 bytes makes a number. The numbers are latitude, longitude, and altitude.
        self.coordinates["latitude"] = int.from_bytes(data[0:4], "big", signed=True) # Parse the byte array and convert four bytes into a signed int
        self.coordinates["longitude"] = int.from_bytes(data[4:8], "big", signed=True)
        self.coordinates["altitude"] = int.from_bytes(data[8:12], "big", signed=True)

    def publish_coords(self):
        self.read_coords() # Call helper ftn
        msg = Coords()  # Create msg and assign vals
        msg.latitude = self.coordinates["latitude"]
        msg.longitude = self.coordinates["longitude"]
        msg.altitude = self.coordinates["altitude"]

        self.publisher_.publish(msg) # Publish message
     
def main(args=None):
    rclpy.init(args=args)
    node = GPSPubNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
     
     
if __name__ == "__main__":
    main()
