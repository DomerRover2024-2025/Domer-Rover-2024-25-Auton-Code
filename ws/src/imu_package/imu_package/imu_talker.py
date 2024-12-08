import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time 
#be able to write to the topic
#create an instance of the serial, open up a serial.write, and then write whatever the message being published is
class IMUReaderNode(Node):
    def __init__(self):
        super().__init__("imu_reader_node")
        self.publisher_ = self.create_publisher(String, '/imu/data', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.read_imu_data)
        self.count = 0

        self.serialPort = serial.Serial('/dev/ttyACM1')

    def read_imu_data(self):
        raw_data = self.serialPort.readline().decode('utf-8')
        #print(raw_data) 
        # Log the raw data
        self.get_logger().info(f"Received IMU Data: {raw_data}")

        # You can process the raw data here if needed
        # For example, split data by a delimiter if it's CSV formatted:
        # imu_values = raw_data.split(',')
        # orientation, angular_velocity, linear_acceleration = imu_values[:3], imu_values[3:6], imu_values[6:]
    
        # Optionally, publish the data to a ROS 2 topic
        #msg = String()
        #msg.data = raw_data

        #self.get_logger().info("Recieved IMU Data: {raw_data}")

def main(args=None):
    rclpy.init(args=args)
    #create node
    imu_reader_node = IMUReaderNode()
    #use node
    rclpy.spin(imu_reader_node)
    #destroy node
    talkerNode.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()
