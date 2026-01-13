# Sensor Topic Publication Status Checker
Package for verifying the publication status of sensor topics. This package provides status checking for any topic published in ROS environments.
## Installation

### Prerequisites
`ROS Noetic`
### Installation Steps
Create and navigate to your ROS workspace:
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
```
Clone this repository:
```
git clone https://github.com/MarcelloMatoss/sensors_status.git
```
Build your workspace:
```
cd ..
catkin make
```
Load the environment variables:
```
source devel/setup.bash
```
### Configuration
The sensor settings (topics, message types, frequency, sampling rate, tolerance, and status topic) can be configured in the following file:

`catkin_ws/src/espeleo_planning2/config/sensor_status_config.yaml`

Below is an example showing distinct sensors with different topics and message types.
```
sensors:
  - sensor: livox
    topics_sensor: ['/livox/imu', '/livox/lidar']
    msgs_types: ['sensor_msgs/Imu', 'sensor_msgs/PointCloud2']
    topics_frequency: [100, 10]
    sampling: [10, 5]
    frequency_tolerance: [0.2, 0.2]
    max_downtime: 1
    status_topic_pub: '/status/livox'
  - sensor: xsens
    topics_sensor: ['/imu/data', '/imu/mag']
    msgs_types: ['sensor_msgs/Imu', 'sensor_msgs/MagneticField']
    topics_frequency: [400, 100]
    sampling: [200, 50]
    frequency_tolerance: [0.2, 0.2]
    max_downtime: 1
    status_topic_pub: '/status/xsens'
  - sensor: realsense
    topics_sensor: ['/d456/accel/imu_info', '/d456/align_to_color/parameter_descriptions', '/d456/align_to_color/parameter_updates', '/d456/aligned_depth_to_color/camera_info', '/d456/aligned_depth_to_color/image_raw', '/d456/color/camera_info', '/d456/color/image_raw', '/d456/gyro/imu_info', '/d456/imu']
    msgs_types: ['realsense2_camera/IMUInfo','dynamic_reconfigure/ConfigDescription','dynamic_reconfigure/Config','sensor_msgs/CameraInfo','sensor_msgs/Image','sensor_msgs/CameraInfo','sensor_msgs/Image','realsense2_camera/IMUInfo','sensor_msgs/Imu']
    topics_frequency: [30,30,30,30,30,30,30,30,200]
    sampling: [15,15,15,15,15,15,15,15,100]
    frequency_tolerance: [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    max_downtime: 1
    status_topic_pub: '/status/realsense'

```
## How to use
Launch the checker with:
```
roslaunch sensors_status sensors_status.launch
```
### Output

After the launch, the checker will publish, for each sensor, a topic of type `Float32MultiArray` with the name defined in the configuration file. The verified sensor topics are described in the `layout.dim` field, while the data field contains an array of float values representing the state of each topic, preserving the same order defined in `layout.dim`.

The output will contain four distinct values to represent the sensor state:

* 0.0 indicates that the sensor is not publishing;
* 0.5 indicates that the sensor is publishing, but at a rate lower than the defined one;
* 1.0 indicates that the sensor is publishing at the correct rate;
* 1.5 indicates that the sensor is publishing above the defined rate.

Below is an example of the `Float32MultiArray` message published by the checker for a sensor with two monitored topics.
```
layout: 
  dim: 
    - 
      label: "/livox/imu"
      size: 1
      stride: 1
    - 
      label: "/livox/lidar"
      size: 1
      stride: 1
  data_offset: 0
data: [1.5, 1.0]
---

```

