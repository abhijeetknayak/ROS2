# ROS2

This repository contains ROS2 tutorials and exercises for learning and practicing ROS2 concepts. The tutorials cover various topics including nodes, topics, services, actions, and more.

We use ROS2 Jazzy as the ROS2 version for these tutorials. To make it easier for you to follow along, we have provided a Dockerfile that sets up a ROS2 Jazzy environment. You can build and run the Docker container to get started with the tutorials:

If you don't have docker yet, install it from [here](https://docs.docker.com/desktop/)

```bash
# Enable GUI support for the Docker container
xhost +local:docker

# Build the Docker image and start the container in the detached mode
docker compose up -d --build
```

If you use VSCode, you can also use the Remote - Containers extension to open the project in a containerized environment. Click the container icon in the left pane and search for the container. Right click to attach vscode to the container. This will allow you to work with the code and run ROS2 commands directly from within the container.


To stop the container, you can use the following command:
```bash
docker compose down
```

# ROS2 Workspace

In the ros2_ws directory, you will find the ROS2 workspace that contains the source code for the tutorials and exercises. The workspace directory is mounted as a volume in the Docker container, so any changes you make to the code will be reflected in the container.

The workspace is structured as follows:

```
ros2_ws/
├── src/          # Source code for ROS2 packages
├── build/        # Build artifacts (generated after building the workspace)
├── install/      # Installed packages (generated after building the workspace)
```

Inside the container, you can build the workspace using the following command:

```bash
cd ros2_ws
colcon build # colcon is the build tool used in ROS2 to build packages

# Don't forget to source the workspace to set up the environment
source install/setup.bash
``` 
