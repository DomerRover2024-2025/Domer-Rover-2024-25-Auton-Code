FROM osrf/ros:iron-desktop-full
LABEL org.opencontainers.image.source=https://github.com/DomerRover2024-2025/Domer-Rover-2024-25-Auton-Code

# Example of installing programs
RUN apt-get update && apt-get install -y nano && rm -rf /var/lib/apt/lists/*

# Example of copying a file
COPY config/ /site_config/

ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create a non-root user
RUN groupadd --gid $USER_GID $USERNAME \ 
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir /home/$USERNAME/.config && chown $USER_UID:$USER_GID /home/$USERNAME/.config

RUN apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

RUN echo "ALL DONE"