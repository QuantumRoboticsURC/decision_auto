#TRATANDO DE IMPLEMENTAR UN WHILE
import rospy
import time
from std_msgs.msg import *
from geometry_msgs.msg import Twist
from visualization_msgs.msg import Marker

def checkArViz (marker):
	if(marker.id>=0):
		pub.publish(0)
		time.sleep(3)
		pub.publish(1)

#pub = rospy.Publisher('/vision/instrucciones',String,queue_size = 10)
pub = rospy.Publisher('/matrix',Int64,queue_size = 10)

def main():
	rospy.init_node("lost_comms_recovery")
	subrviz = rospy.Subscriber('/visualization_marker', Marker, checkArViz)
	rate = rospy.Rate(2)
	rospy.spin()
