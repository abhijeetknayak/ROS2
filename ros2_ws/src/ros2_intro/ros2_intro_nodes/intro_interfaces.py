#!/usr/bin/env python3
"""Small, complete examples of a ROS message, service, and action."""

import asyncio
import math
import time
from typing import Optional

import rclpy
from ros2_intro.action import ObserveCamera
from ros2_intro.msg import RobotSnapshot
from ros2_intro.srv import GetRobotStatus
from nav_msgs.msg import Odometry
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image


class IntroInterfaces(Node):
    """Publish a snapshot and expose one short service and one action."""

    def __init__(self) -> None:
        super().__init__('intro_interfaces')

        image_topic = self.declare_parameter(
            'image_topic', '/camera/image_raw').value
        odom_topic = self.declare_parameter('odom_topic', '/odom').value
        snapshot_period = float(
            self.declare_parameter('snapshot_period', 1.0).value)

        self._last_odom: Optional[Odometry] = None
        self._camera_frames = 0
        self._last_image_wall_time: Optional[float] = None

        self._snapshot_pub = self.create_publisher(
            RobotSnapshot, '/robot_snapshot', 10)
        self.create_subscription(
            Image, image_topic, self._on_image, qos_profile_sensor_data)
        self.create_subscription(Odometry, odom_topic, self._on_odom, 10)
        self.create_timer(snapshot_period, self._publish_snapshot)

        self.create_service(
            GetRobotStatus, '/get_robot_status', self._get_status)
        self._action_server = ActionServer(
            self,
            ObserveCamera,
            '/observe_camera',
            execute_callback=self._observe_camera,
            goal_callback=self._goal_callback,
            cancel_callback=self._cancel_callback,
        )

        self.get_logger().info(
            'Publishing /robot_snapshot; service /get_robot_status; '
            'action /observe_camera')

    def _on_image(self, _message: Image) -> None:
        self._camera_frames += 1
        self._last_image_wall_time = time.monotonic()

    def _on_odom(self, message: Odometry) -> None:
        self._last_odom = message

    @staticmethod
    def _yaw_from_odom(message: Odometry) -> float:
        q = message.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        return math.atan2(siny_cosp, cosy_cosp)

    def _camera_ok(self) -> bool:
        if self._last_image_wall_time is None:
            return False
        return (time.monotonic() - self._last_image_wall_time) < 2.0

    def _values(self) -> tuple[bool, float, float, float, float]:
        if self._last_odom is None:
            return False, 0.0, 0.0, 0.0, 0.0
        pose = self._last_odom.pose.pose
        twist = self._last_odom.twist.twist
        speed = math.hypot(twist.linear.x, twist.linear.y)
        ready = self._camera_ok()
        return (
            ready,
            pose.position.x,
            pose.position.y,
            self._yaw_from_odom(self._last_odom),
            speed,
        )

    def _publish_snapshot(self) -> None:
        ready, x, y, yaw, speed = self._values()
        message = RobotSnapshot()
        message.stamp = self.get_clock().now().to_msg()
        message.x = x
        message.y = y
        message.yaw = yaw
        message.planar_speed = float(speed)
        message.camera_frames_received = self._camera_frames
        message.camera_ok = ready
        self._snapshot_pub.publish(message)

    def _get_status(
        self,
        _request: GetRobotStatus.Request,
        response: GetRobotStatus.Response,
    ) -> GetRobotStatus.Response:
        ready, x, y, yaw, speed = self._values()
        response.ready = ready
        response.x = x
        response.y = y
        response.yaw = yaw
        response.planar_speed = float(speed)
        response.camera_frames_received = self._camera_frames
        response.summary = (
            f'position=({x:+.2f}, {y:+.2f}) m, '
            f'yaw={math.degrees(yaw):+.1f} deg, speed={speed:.2f} m/s, '
            f'camera={"ok" if self._camera_ok() else "waiting"}'
        )
        return response

    def _goal_callback(self, goal_request: ObserveCamera.Goal) -> GoalResponse:
        if 1.0 <= goal_request.duration <= 15.0:
            return GoalResponse.ACCEPT
        self.get_logger().warning('Rejecting duration outside 1 to 15 seconds')
        return GoalResponse.REJECT

    @staticmethod
    def _cancel_callback(_goal_handle) -> CancelResponse:
        return CancelResponse.ACCEPT

    async def _observe_camera(self, goal_handle) -> ObserveCamera.Result:
        duration = float(goal_handle.request.duration)
        start_time = time.monotonic()
        start_frames = self._camera_frames

        while True:
            elapsed = time.monotonic() - start_time
            observed = self._camera_frames - start_frames

            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = ObserveCamera.Result()
                result.success = False
                result.frames_received = observed
                result.summary = 'Observation canceled by the client.'
                return result

            feedback = ObserveCamera.Feedback()
            feedback.elapsed = float(min(elapsed, duration))
            feedback.frames_received = observed
            goal_handle.publish_feedback(feedback)

            if elapsed >= duration:
                break
            await asyncio.sleep(0.2)

        goal_handle.succeed()
        result = ObserveCamera.Result()
        result.frames_received = self._camera_frames - start_frames
        result.success = result.frames_received > 0
        result.summary = (
            f'Received {result.frames_received} camera frames '
            f'in {duration:.1f} seconds.'
        )
        return result

    def destroy_node(self) -> bool:
        self._action_server.destroy()
        return super().destroy_node()


def main(args=None) -> None:
    rclpy.init(args=args)
    node = IntroInterfaces()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
