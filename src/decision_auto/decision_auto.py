#TRATANDO DE IMPLEMENTAR UN WHILE
import rospy
import time
from std_msgs.msg import *
from geometry_msgs.msg import Twist
contadorx = 0

def checkCam (cam):
	global contadorx
	if(contadorx == 0):
		twist = Twist()
		linear_vel = .2
		angular_vel = .2
		cam = cam.data
		try:
			bit = cam.index('1')
			pub.publish(cam)
			if bit < int(len(cam) / 3):
				try:
					bit2 = cam.index('0', int(len(cam) / 3 + 1))
				except ValueError as ve2:
					bit2 = len(cam)
				if (bit2 - bit > int(len(cam) / 2)):
					pub.publish("stop")
					twist.linear.x = 0
					twist.angular.z = 0
					cmd_vel_pub.publish(twist)
				else:
					pub.publish("turn right")
					twist.linear.x = 0
					twist.angular.z = angular_vel
					cmd_vel_pub.publish(twist)
			elif bit > int(len(cam) / 3) and bit < int(2 * (len(cam) / 3) + 1):
				pub.publish("stop")
				twist.linear.x = 0
				twist.angular.z = 0
				cmd_vel_pub.publish(twist)
			elif bit > int(2 * (len(cam) / 3)):
				pub.publish("turn left")
				twist.linear.x = 0
				twist.angular.z = -angular_vel
				cmd_vel_pub.publish(twist)
			else:
				cmd_vel_pub.publish(twist)
				pub.publish(str(bit))
				pub.publish("No entro a nada :(")
		except ValueError as ve:
			pub.publish("keep forward")
			twist.linear.x = linear_vel
			twist.angular.z = 0
			cmd_vel_pub.publish(twist)
		contadorx = 1
	else:
		#time.sleep(0.1)
		contadorx += 1
		if(contadorx == 10):
			contadorx = 0

pub = rospy.Publisher('/vision/instrucciones',String,queue_size = 10)
cmd_vel_pub = rospy.Publisher("teleop/cmd_vel", Twist, queue_size=1)
def main():
	rospy.init_node("decision_auto")
	sub = rospy.Subscriber('/vision/obstacle_bool',String, checkCam)
	rate = rospy.Rate(2)
	rospy.spin()
