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
```
sensors:
  - sensor: sensor_1
    topics_sensor: ['/topic_1, '/topic_2']
    msgs_types: ['mensage_type_1', 'mensage_type_2']
    topics_frequency: [topic_1_frequency, topics_2_frequency]
    sampling: [sampling_topic_1, sampling_topic_1]
    frequency_tolerance: [frequency_tolerance_topic_1, frequency_tolerance_topic_2]
    max_downtime: 1 #seconds
    status_topic_pub: '/topic_pub'
```
## How to use
Launch the checker with:
```
roslaunch sensors_status sensors_status.launch
```

