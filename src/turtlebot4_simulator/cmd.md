# TurtleBot 4 Lite Simulation Launch Guide

This document covers the optimized command used to launch the TurtleBot 4 Lite simulation in Ignition Gazebo with dedicated NVIDIA GPU offloading, as well as essential operational commands.

---

## Quick Start Command

Run this command in your terminal to launch the simulation:

```bash
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia ros2 launch turtlebot4_ignition_bringup turtlebot4_ignition.launch.py hmi:=false model:=lite rviz:=true