import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time 
#be able to write to the arduino serial port
#create an instance of the serial, open up a serial.write, and then write whatever the message being published is
class TalkerNode(Node):
    def __init__(self):
        super().__init__("talker_node")
        self.publisher_ = self.create_publisher(String, 'motor_state', 10)
        self.subscriber_ = self.create_subscription(
            String,
            'manual_controller_input',
            self.listener_callback,
            10)    
        timer_period = 0.1
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0

        self.serialPort = serial.Serial('/dev/ttyACM0')
    def listener_callback(self, msg):
        #msg = String()

        #msg.data = f"Hello everyone {self.count}"
        # self.publisher_.publish(msg.data)
        self.count += 1
        
        self.get_logger().info(f"Recieving {msg.data}")
        
        # self.write(msg.data)

     #def write(x):
        self.serialPort.write(msg.data.encode())
        


def main(args=None):
    rclpy.init(args=args)
    #create node
    talkerNode = TalkerNode()
    #use node
    rclpy.spin(talkerNode)
    #destroy node
    talkerNode.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()

