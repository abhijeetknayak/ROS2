# inspection_robot_intro

A **single ROS 2 package** for the introduction week. It contains everything needed for the exercise:

- a non-empty Gazebo Harmonic robotics-laboratory world;
- a differential-drive inspection robot;
- keyboard teleoperation through `/cmd_vel`;
- an RGB camera publishing `/camera/image_raw` and `/camera/camera_info`;
- odometry on `/odom`;
- a custom message, service, and action defined in this same package;
- an introductory observer node with three student TODO functions;
- tests, the LaTeX exercise sheet, and its PDF.

There are **no additional course ROS packages**. The generated interfaces use these type names:

```text
inspection_robot_intro/msg/RobotSnapshot
inspection_robot_intro/srv/GetRobotStatus
inspection_robot_intro/action/ObserveCamera
```

## 1. Place the package in a workspace

The downloaded folder itself is the ROS package. Put it inside the `src` directory of a workspace:

```bash
mkdir -p ~/ros2_intro_ws/src
cp -r inspection_robot_intro ~/ros2_intro_ws/src/
cd ~/ros2_intro_ws
```

Install missing dependencies, then build only this package:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-select inspection_robot_intro
source install/setup.bash
```

Every new terminal must source both ROS 2 and the workspace:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_intro_ws/install/setup.bash
```

## 2. Launch the simulation

```bash
ros2 launch inspection_robot_intro intro_sim.launch.py
```

The launch file starts:

- Gazebo with `worlds/robotics_lab.sdf`;
- the ROS-Gazebo bridge from `config/bridge.yaml`;
- `intro_interfaces`, which publishes the custom message and provides the service and action.

## 3. Drive with the keyboard

In a sourced terminal:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Keep this terminal focused while driving. Use `k` to stop.

## 4. View the camera

```bash
rqt_image_view
```

Select:

```text
/camera/image_raw
```

Useful checks:

```bash
ros2 topic info /camera/image_raw -v
ros2 topic hz /camera/image_raw
ros2 topic echo /camera/camera_info --once
```

## 5. Explore topics and messages

```bash
ros2 topic list -t
ros2 topic echo /odom --once
ros2 topic echo /robot_snapshot --once
ros2 interface show inspection_robot_intro/msg/RobotSnapshot
```

## 6. Call the service

```bash
ros2 interface show inspection_robot_intro/srv/GetRobotStatus
ros2 service call /get_robot_status \
  inspection_robot_intro/srv/GetRobotStatus "{}"
```

## 7. Send an action goal

```bash
ros2 interface show inspection_robot_intro/action/ObserveCamera
ros2 action send_goal /observe_camera \
  inspection_robot_intro/action/ObserveCamera \
  "{duration: 5.0}" --feedback
```

The server accepts durations from 1 to 15 seconds.

## 8. Record and replay a rosbag

Record a short drive:

```bash
ros2 bag record -o intro_bag \
  /cmd_vel /odom /robot_snapshot /camera/camera_info
```

Stop recording with `Ctrl+C`, then inspect and replay it:

```bash
ros2 bag info intro_bag
ros2 bag play intro_bag
```

## 9. Student programming task

Complete the three `TODO(student)` functions in:

```text
inspection_robot_intro_nodes/student_helpers.py
```

Run the tests from the workspace root:

```bash
pytest -q src/inspection_robot_intro/test/test_student_helpers.py
```

After completing them, run:

```bash
ros2 run inspection_robot_intro robot_observer
```

The observer summarizes camera resolution/rate and robot position, heading, and speed.

## Package layout

```text
inspection_robot_intro/
├── action/ObserveCamera.action
├── config/bridge.yaml
├── docs/sheet01_ros2_intro.tex
├── docs/sheet01_ros2_intro.pdf
├── inspection_robot_intro_nodes/
│   ├── intro_interfaces.py
│   ├── robot_observer.py
│   └── student_helpers.py
├── launch/intro_sim.launch.py
├── msg/RobotSnapshot.msg
├── scripts/
├── srv/GetRobotStatus.srv
├── test/test_student_helpers.py
└── worlds/robotics_lab.sdf
```

## Troubleshooting

**Package not found**

Rebuild and source the workspace:

```bash
cd ~/ros2_intro_ws
colcon build --symlink-install --packages-select inspection_robot_intro
source install/setup.bash
```

**No image in `rqt_image_view`**

Check that Gazebo is running and that the bridge publishes the topic:

```bash
ros2 topic info /camera/image_raw -v
ros2 topic hz /camera/image_raw
```

**Robot does not move**

Keep the teleoperation terminal focused and verify that commands are being published:

```bash
ros2 topic echo /cmd_vel --once
```

**A custom interface cannot be found**

Because the message, service, and action are generated during the build, rebuild the package and source `install/setup.bash` again.

**Gazebo rendering problems in a virtual machine**

Enable 3D acceleration. A software-rendering fallback can sometimes be started with:

```bash
LIBGL_ALWAYS_SOFTWARE=1 ros2 launch inspection_robot_intro intro_sim.launch.py
```

## Official references

- ROS 2 Jazzy beginner CLI tutorials: <https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools.html>
- Topics, services, and actions: <https://docs.ros.org/en/jazzy/Concepts/Basic/Interfaces-Topics-Services-Actions.html>
- Creating custom interfaces: <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Single-Package-Define-And-Use-Interface.html>
- Recording and replaying data: <https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html>
- Gazebo ROS 2 integration: <https://gazebosim.org/docs/harmonic/ros2_integration/>
