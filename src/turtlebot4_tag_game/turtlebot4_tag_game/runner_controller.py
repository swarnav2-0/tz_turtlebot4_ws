#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import random
import math

class RunnerController(Node):
    def __init__(self):
        super().__init__('runner_controller')
        
        # Publishers and Subscribers (Adjust topics/namespaces if needed)
        self.cmd_pub = self.create_publisher(Twist, '/runner/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/runner/scan', self.scan_callback, 10)
        
        # Control Loop (10 Hz)
        self.timer = self.create_timer(0.1, self.control_loop)
        
        self.min_front_dist = 10.0
        self.target_linear = 0.3
        self.target_angular = 0.0
        self.step_counter = 0

    def scan_callback(self, msg: LaserScan):
        # Extract forward-facing LiDAR ranges (approx -35 to +35 degrees)
        front_ranges = []
        angle_range_rad = 0.6  # ~35 deg

        for i, r in enumerate(msg.ranges):
            angle = msg.angle_min + i * msg.angle_increment
            if -angle_range_rad <= angle <= angle_range_rad:
                if not math.isinf(r) and not math.isnan(r) and r > 0.05:
                    front_ranges.append(r)

        self.min_front_dist = min(front_ranges) if front_ranges else 10.0

    def control_loop(self):
        cmd = Twist()

        # 1. OBSTACLE AVOIDANCE: If wall/obstacle is closer than 0.75m
        if self.min_front_dist < 0.75:
            cmd.linear.x = 0.05
            cmd.angular.z = 1.3  # Sharp turn away from wall
        else:
            # 2. VARIABLE SPEED & TURNS: Change speed and direction periodically (~every 2.5s)
            self.step_counter += 1
            if self.step_counter % 25 == 0:
                self.target_linear = random.uniform(0.20, 0.45)
                self.target_angular = random.uniform(-0.8, 0.8)

            cmd.linear.x = self.target_linear
            cmd.angular.z = self.target_angular

        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = RunnerController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()