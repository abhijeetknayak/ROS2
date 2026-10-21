#!/usr/bin/env python3
"""A compact example of ROS 2 subscriptions and timer callbacks."""

import math

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image

from .student_helpers import image_megapixels, planar_speed, yaw_from_quaternion


class RobotObserver(Node):
    """Summarize camera and odometry messages without flooding the terminal."""

    def __init__(self) -> None:
        super().__init__('robot_observer')

        image_topic = self.declare_parameter(
            'image_topic', '/camera/image_raw').value
        odom_topic = self.declare_parameter('odom_topic', '/odom').value
        summary_period = float(
            self.declare_parameter('summary_period', 1.0).value)

        self._image_count = 0
        self._last_image = None
        self._last_odom = None
        self._previous_report_time = self.get_clock().now()

        self.create_subscription(
            Image, image_topic, self.on_image, qos_profile_sensor_data)
        self.create_subscription(Odometry, odom_topic, self.on_odom, 10)
        self.create_timer(summary_period, self.report)

        self.get_logger().info(
            f'Observing image={image_topic!r} and odom={odom_topic!r}')

    def on_image(self, message: Image) -> None:
        self._image_count += 1
        self._last_image = message

    def on_odom(self, message: Odometry) -> None:
        self._last_odom = message

    def report(self) -> None:
        now = self.get_clock().now()
        elapsed = (now - self._previous_report_time).nanoseconds / 1.0e9
        fps = self._image_count / elapsed if elapsed > 0.0 else 0.0

        if self._last_image is None:
            image_text = 'camera: waiting for first image'
        else:
            msg = self._last_image
            megapixels = image_megapixels(msg.width, msg.height)
            image_text = (
                f'camera: {msg.width}x{msg.height} {msg.encoding}, '
                f'{megapixels:.3f} MP, about {fps:.1f} Hz')

        if self._last_odom is None:
            motion_text = 'odom: waiting for first message'
        else:
            pose = self._last_odom.pose.pose
            twist = self._last_odom.twist.twist
            yaw = yaw_from_quaternion(
                pose.orientation.x,
                pose.orientation.y,
                pose.orientation.z,
                pose.orientation.w,
            )
            speed = planar_speed(twist.linear.x, twist.linear.y)
            motion_text = (
                f'odom: x={pose.position.x:+.2f} m, '
                f'y={pose.position.y:+.2f} m, '
                f'yaw={math.degrees(yaw):+.1f} deg, '
                f'speed={speed:.2f} m/s')

        self.get_logger().info(f'{image_text} | {motion_text}')
        self._image_count = 0
        self._previous_report_time = now


def main(args=None) -> None:
    rclpy.init(args=args)
    node = RobotObserver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
