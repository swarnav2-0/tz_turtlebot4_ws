# TurtleBot 4 Lite Simulation Launch Guide

This document covers the optimized command used to launch the TurtleBot 4 Lite simulation in Ignition Gazebo with dedicated NVIDIA GPU offloading, as well as essential operational commands.

---

## Quick Start Command

Run this command in your terminal to launch the simulation:

```bash
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia ros2 launch turtlebot4_ignition_bringup turtlebot4_ignition.launch.py hmi:=false model:=lite rviz:=true

__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia ros2 launch turtlebot4_ignition_bringup turtlebot4_ignition.launch.py world:=arena hmi:=false model:=lite rviz:=true namespace:=catcher


swarnav@swarnav-s-laptop:~/turtlebot4_ws$ __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia ros2 launch turtlebot4_ignition_bringup turtlebot4_ignition.launch.py world:=arena hmi:=false model:=lite rviz:=true nav2:=true localization:=true slam:=false map:=/home/swarnav/turtlebot4_ws/arena_map.yaml

__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia ros2 launch turtlebot4_ignition_bringup turtlebot4_ignition.launch.py world:=arena hmi:=false model:=lite rviz:=true nav2:=true localization:=true slam:=false map:=$(pwd)/arena_map.yaml

