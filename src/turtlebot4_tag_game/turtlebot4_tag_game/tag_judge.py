#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from std_msgs.msg import ColorRGBA
import tf2_ros
import math

class TagJudge(Node):
    def __init__(self):
        super().__init__('tag_judge')

        # TF Buffer and Listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # RViz Marker Publisher for 0.5m visual zone
        self.marker_pub = self.create_publisher(Marker, '/tag_zone_marker', 10)

        # Judge Loop at 10Hz (0.1s interval)
        self.timer = self.create_timer(0.1, self.judge_loop)

        # Rules
        self.TAG_RADIUS = 0.5       # 0.5 meters
        self.HOLD_TIME_REQ = 1.0    # 1.0 continuous second
        
        self.in_zone_time = 0.0
        self.is_tagged = False

    def judge_loop(self):
        # Always publish the 0.5m visual circle attached to runner/base_link
        self.publish_visual_circle()

        if self.is_tagged:
            return

        try:
            # Lookup transform from runner base link to catcher base link
            tf_stamped = self.tf_buffer.lookup_transform(
                'runner/base_link',
                'catcher/base_link',
                rclpy.time.Time()
            )

            dx = tf_stamped.transform.translation.x
            dy = tf_stamped.transform.translation.y
            distance = math.sqrt(dx * dx + dy * dy)

            # Check distance threshold
            if distance <= self.TAG_RADIUS:
                self.in_zone_time += 0.1
                self.get_logger().info(
                    f"Catcher inside tag zone! Distance: {distance:.3f}m | Time inside: {self.in_zone_time:.1f}s"
                )

                if self.in_zone_time >= self.HOLD_TIME_REQ:
                    self.is_tagged = True
                    self.get_logger().warn("=" * 50)
                    self.get_logger().warn("🎉 TAGGED! Catcher has successfully caught the Runner!")
                    self.get_logger().warn(f"Maintained < {self.TAG_RADIUS}m for {self.in_zone_time:.1f} seconds.")
                    self.get_logger().warn("=" * 50)
            else:
                if self.in_zone_time > 0:
                    self.get_logger().info("Catcher left tag zone. Resetting timer.")
                self.in_zone_time = 0.0

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            pass  # Wait for TF frames to become available

    def publish_visual_circle(self):
        marker = Marker()
        marker.header.frame_id = "runner/base_link"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "tag_zone"
        marker.id = 0
        marker.type = Marker.CYLINDER
        marker.action = Marker.ADD

        # Anchor at runner's ground level
        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = -0.05
        marker.pose.orientation.w = 1.0

        # Scale: Diameter = 2 * Radius = 1.0m
        marker.scale.x = self.TAG_RADIUS * 2.0  # 1.0m diameter
        marker.scale.y = self.TAG_RADIUS * 2.0  # 1.0m diameter
        marker.scale.z = 0.01                  # Thin disc

        # Color feedback: Red when inside zone, Translucent Yellow when safe
        if self.in_zone_time > 0:
            marker.color = ColorRGBA(r=1.0, g=0.0, b=0.0, a=0.5)  # Red
        else:
            marker.color = ColorRGBA(r=1.0, g=0.8, b=0.0, a=0.35) # Translucent Yellow

        self.marker_pub.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    node = TagJudge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()