FROM osrf/ros:jazzy-desktop-full

SHELL ["/bin/bash", "-c"]

ARG DEBIAN_FRONTEND=noninteractive

# Common ROS 2 development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    nano \
    vim \
    tmux \
    python3-pip \
    python3-rosdep \
    python3-colcon-common-extensions \
    python3-vcstool \
    && rm -rf /var/lib/apt/lists/*

# Create a persistent ROS workspace
RUN mkdir -p /ros2_ws/src
WORKDIR /ros2_ws

# Automatically source ROS and the local workspace
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo 'if [ -f /ros2_ws/install/setup.bash ]; then source /ros2_ws/install/setup.bash; fi' \
        >> /root/.bashrc

CMD ["bash"]