import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class GNSSPublisher(Node):
    def __init__(self):
        super().__init__('gnss_publisher')
        self.publisher_ = self.create_publisher(String, 'GNSS_data', 10)
        
        self.serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        
        self.timer = self.create_timer(1.0, self.publish_gnss_data) 

    def publish_gnss_data(self):
        if self.serial_port.in_waiting > 0:
            line = self.serial_port.readline().decode('utf-8').strip()
            self.get_logger().info(f"Received GNSS Data: {line}")
            
            msg = String()
            msg.data = line
            self.publisher_.publish(msg)
            # POTENTIAL TIMING ISSUES - calls func every 1Hz, but may also wait for arduino readline so look at timing / skipping
def main(args=None):
    rclpy.init(args=args)
    node = GNSSPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node stopped by user')
    finally:
        node.serial_port.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

