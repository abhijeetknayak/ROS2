# ROS2

This repository contains ROS2 tutorials and exercises for learning and practicing ROS2 concepts. The tutorials cover various topics including nodes, topics, services, actions, and more.

We use ROS2 Jazzy as the ROS2 version for these tutorials. To make it easier for you to follow along, we have provided a Dockerfile that sets up a ROS2 Jazzy environment. You can build and run the Docker container to get started with the tutorials:

```bash
# Enable GUI support for the Docker container
xhost +local:docker

# Build the Docker image and start the container in the detached mode
docker compose up -d --build
```

If you use VSCode, you can also use the Remote - Containers extension to open the project in a containerized environment. Click the container icon in the left pane and search for the container. Right click to attach vscode to the container. This will allow you to work with the code and run ROS2 commands directly from within the container.
