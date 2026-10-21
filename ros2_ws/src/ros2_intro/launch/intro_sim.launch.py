import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    package_share = get_package_share_directory('ros2_intro')
    world_file = os.path.join(package_share, 'worlds', 'robotics_lab.sdf')
    bridge_config = os.path.join(package_share, 'config', 'bridge.yaml')

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py',
            )
        ),
        launch_arguments={
            'gz_args': f'-r -v 3 {world_file}',
            'on_exit_shutdown': 'true',
        }.items(),
    )

    bridge_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_bridge'),
                'launch',
                'ros_gz_bridge.launch.py',
            )
        ),
        launch_arguments={
            'bridge_name': 'intro_bridge',
            'config_file': bridge_config,
        }.items(),
    )

    interface_demo = Node(
        package='ros2_intro',
        executable='intro_interfaces',
        name='intro_interfaces',
        output='screen',
        parameters=[{'snapshot_period': 1.0}],
    )

    return LaunchDescription([gazebo_launch, bridge_launch, interface_demo])
