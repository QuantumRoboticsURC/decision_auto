#TRATANDO DE IMPLEMENTAR UN WHILE
import rospy
import time
from std_msgs.msg import *
from geometry_msgs.msg import Twist

def obstacles (depths):
	depthsStr = str(depths.data)
	depthsArray = depthsStr.split("|")
	depthsArray.pop()
	menor = depthsArray[0]
	for elemento in depthsArray:
		if elemento < menor:
			menor = elemento
	if(float(menor) > 6):
		pub.publish("200-" + str(menor))
	else:
		pub.publish(str(depthsArray.index(menor)) + "-" + str(menor))

pub = rospy.Publisher('/nav/obstacle',String,queue_size = 10)
def main():
	rospy.init_node("decision_auto")
	sub = rospy.Subscriber('/nav/depths',String, obstacles)
	# depths = "2.00|2.13|2.42|2.43|1.9|1.85|1.00|1.40|2.13|"
	# depthsArray = depths.split("|")
	# depthsArray.pop()
	# menor = depthsArray[0]
	# for elemento in depthsArray:
	# 	if elemento < menor:
	# 		menor = elemento
	# obstacle = str(depthsArray.index(menor)) + "-" + str(menor)
	# print(obstacle)
	# print(depthsArray)
	rate = rospy.Rate(2)
	rospy.spin()
