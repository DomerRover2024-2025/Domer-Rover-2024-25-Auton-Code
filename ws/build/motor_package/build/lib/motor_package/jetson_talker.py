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
        self.count += 1
        self.get_logger().info(f"Recieving {msg.data}")
        
        try:
            joy_x, joy_y, triggerMult, b_x, b_circle, b_triangle, b_square = msg.data.split()

            joy_x = float(joy_x)
            joy_y = float(joy_y)
            triggerMult = float(triggerMult)
            b_x = int(b_x)
            b_circle = int(b_circle)
            b_triangle = int(b_triangle)
            b_square = int(b_square)

            if (b_circle == 1):
                serial_data = f"-25 25\n"
            elif b_square == 1:
                serial_data = f"25 -25\n"
            else:
                serial_data = f"{joy_x} {joy_y}\n"

            self.get_logger().info(f"SERIALDATA: {serial_data}")
            self.serialPort.write(msg.serial_data.encode())
        except ValueError as e:
            self.get_logger().error(f"Error parsing: {e}")
        


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

