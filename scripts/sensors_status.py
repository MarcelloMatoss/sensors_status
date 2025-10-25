#!/usr/bin/env python3
import rospy
from std_msgs.msg import ByteMultiArray, MultiArrayDimension
from roslib.message import get_message_class


class Topic_create:
    def __init__(self, topics_name, msgs_types, topics_frequency, sampling, frequency_tolerance, max_downtime, topic_status_pub):
        
        self.topics_name = topics_name
        self.msgs_types = msgs_types
        self.topics_frequency = topics_frequency
        self.sampling = sampling
        self.fequency_tolerance = frequency_tolerance
        self.max_downtime = max_downtime
        self.topic_status_pub = topic_status_pub
        self.topics_num = len(topics_name)
        self.status_init = []
        self.msg = ByteMultiArray()
        self.pub =rospy.Publisher(topic_status_pub, ByteMultiArray, queue_size=10, latch=True)

        for i in range(self.topics_num):
            self.msg.layout.dim.append(MultiArrayDimension(label=topics_name[i], size=1, stride=1))
            self.status_init.append(False)
        
        self.msg.data = self.status_init
        self.pub.publish(self.msg)
        self.topics = []

        for i in range(self.topics_num):
            self.topics.append(Sensor_status(self.topics_name[i], self.msgs_types[i], self.topics_frequency[i],sampling[i],self.fequency_tolerance[i], self.max_downtime, self.topic_status_pub,i))

class Sensor_status:
    def __init__(self, topic_name, msg_type, topic_frequency, sampling, fequency_tolerance, max_downtime, topic_status_pub, ind):
        self.topic = topic_name
        self.msg_type = msg_type
        self.topic_frequency = topic_frequency
        self.sampling = sampling
        self.fequency_tolerance = fequency_tolerance
        self.max_downtime = max_downtime
        self.topic_status_pub = topic_status_pub
        self.ind = ind
        self.pub = rospy.Publisher(self.topic_status_pub, ByteMultiArray, queue_size=10, latch=True)
        self.msg = ByteMultiArray()
        self.status = self.msg.data
        self.counter = 0
        self.status_topic = False
        self.msg_class = get_message_class(self.msg_type) 
        self.time_init = rospy.get_time()
        self.downtime_init = rospy.get_time()

        rospy.Subscriber(self.topic_status_pub, ByteMultiArray, self.msg_callback, queue_size=10)
        rospy.Subscriber(self.topic, self.msg_class, self.topic_hz_check, queue_size=10)
        rospy.Timer(rospy.Duration(0.01), self.status_check)

    def msg_callback(self, data):
        self.msg = data
        self.status = list(self.msg.data)

    def topic_hz_check(self, data):
        self.downtime_init = rospy.get_time()
        self.counter += 1
        if self.counter == self.sampling:
            rate = self.sampling / (rospy.get_time() - self.time_init)
            if rate < (self.topic_frequency + (self.topic_frequency*self.fequency_tolerance)) and rate > (self.topic_frequency - (self.topic_frequency*self.fequency_tolerance)):
                if not self.status_topic:
                    self.status_topic = True
                    self.status[self.ind] = True
                    self.msg.data = self.status
                    self.pub.publish(self.msg)
            else:
                if self.status_topic:
                    self.status_topic = False
                    self.status[self.ind] = False
                    self.msg.data = self.status
                    self.pub.publish(self.msg)
            
            self.time_init = rospy.get_time()
            self.counter = 0

    def status_check(self, event):
        if (rospy.get_time() - self.downtime_init) > self.max_downtime:
            if self.status_topic:
                self.status_topic = False
                self.status[self.ind] = False
                self.msg.data = self.status
                self.pub.publish(self.msg)

if __name__ == "__main__":
    try:
        rospy.init_node("status")
        sensors = rospy.get_param('sensors',[])
        for sensor in sensors:
            Topic_create(sensor['topics_sensor'], sensor['msgs_types'], sensor['topics_frequency'], sensor['sampling'], sensor['frequency_tolerance'], sensor['max_downtime'], sensor['status_topic_pub'])
        rospy.spin()
    except rospy.ROSInterruptException:
        pass