# Sensor Topic Publication Status Checker
Package for verifying the publication status of sensor topics. This package provides status checking for any topic published in ROS environments.
## Installation

### Prerequisites
ROS Noetic
### Installation Steps
Crie e navegue até sua workspace ROS:
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
```
Clone este repositório:
```
git clone https://github.com/MarcelloMatoss/sensors_status.git
```
Compile sua workspace:
```
cd ..
catkin make
```
```
source devel/setup.bash
```
### Configuration
Para adicionar ou remover sensores e tópicos para a verificação altere o arquivo de configuração catkin_ws/src/espeleo_planning2/config/sensor_status_config.yaml
```

```
## How to use
```
roslaunch sensors_status sensors_status.launch
```

