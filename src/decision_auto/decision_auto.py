#TRATANDO DE IMPLEMENTAR UN WHILE
import rospy
import time
from std_msgs.msg import *
from geometry_msgs.msg import Twist
from visualization_msgs.msg import Marker

## Declaramos dos silenciadores. Estos evitan que las acciones de evacion de obstaculos, se crucen con las acciones de ARVIZ

silenCheckCam = False
silenCheckArViz = False

## Funcion correspondiente al suscriptor (checkArViz)
## Cuando encuentra un codigo con un ID diferente de 0:
	## Publica mensaje "AR tag encontrado" y realiza la accion => + STOP

def checkArViz (marker):
	global silenCheckCam
	global silenCheckArViz
	twist = Twist()
	if(not silenCheckArViz):
		if(marker.id != 0): # > -1 ?
			silenCheckCam = True
			silenCheckArViz = True
			pub.publish("AR tag encontrado")
	
			#Tantito adelante
			twist.linear.x = 0.1
			twist.angular.z = 0
			cmd_vel_pub.publish(twist)
			time.sleep(0.5)
	
			#Tantito atras
			twist.linear.x = -0.1
			twist.angular.z = 0
			cmd_vel_pub.publish(twist)
			time.sleep(0.5)
	
			#Y volvemos a empezar
			twist.linear.x = 0.1
			twist.angular.z = 0
			cmd_vel_pub.publish(twist)
			time.sleep(0.5)
			twist.linear.x = -0.1
			twist.angular.z = 0
			cmd_vel_pub.publish(twist)
			time.sleep(0.5)
	
			#Fin
			twist.linear.x = 0
			twist.angular.z = 0
			cmd_vel_pub.publish(twist)
			silenCheckCam = False
			silenCheckArViz = False
		else:
			pub.publish("No entro a nada :(")

## Funcion correspondiente al suscriptor (checkCam)
## Cuando encuentra un obstaculo toma una decision:
	## Trabaja con velocidades 0.2 para avance y giro

def checkCam (cam):
	global silenCheckCam
	global silenCheckArViz
	if(not silenCheckCam):
		silenCheckCam = True
		silenCheckArViz = True
		twist = Twist()
		linear_vel = .2
		angular_vel = .2
		cam = cam.data
		# BUSCA UN 1 EN EL ARRAY
		try:
			bit = cam.index('1')
			pub.publish(cam)

			# SI ENCUENTRA UN 1 A LA IZQUIERDA
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

			# SI ENCUENTRA UN 1 EN EL CENTRO
			elif bit > int(len(cam) / 3) and bit < int(2 * (len(cam) / 3) + 1):
				pub.publish("stop")
				twist.linear.x = 0
				twist.angular.z = 0
				cmd_vel_pub.publish(twist)

			# SI ENCUENTRA UN 1 A LA DERECHA
			elif bit > int(2 * (len(cam) / 3)):
				pub.publish("turn left")
				twist.linear.x = 0
				twist.angular.z = -angular_vel
				cmd_vel_pub.publish(twist)

			# SI HUBO UN ERROR EN EL ALGORITMO
			else:
				cmd_vel_pub.publish(twist)
				pub.publish(str(bit))
				pub.publish("No entro a nada :(")
		# SI SOLO HAY 0
		except ValueError as ve:
			pub.publish("keep forward")
			twist.linear.x = linear_vel
			twist.angular.z = 0
			cmd_vel_pub.publish(twist)

		## ESPERA 1 SEG ANTES DE VOLVER A ESCANEAR
		time.sleep(1)

		## PARO DE SEGURIDAD DESPUES DE UN SEGUNDO
		pub.publish("stop")
		twist.linear.x = 0
		twist.angular.z = 0
		cmd_vel_pub.publish(twist)

		silenCheckCam = False
		silenCheckArViz = False

pub = rospy.Publisher('/vision/instrucciones',String,queue_size = 10)
cmd_vel_pub = rospy.Publisher("teleop/cmd_vel", Twist, queue_size=1)
def main():
	rospy.init_node("lost_comms_recovery")
	sub = rospy.Subscriber('/vision/obstacle_bool',String, checkCam)
	subrviz = rospy.Subscriber('/visualization_marker', Marker, checkArViz)
	rate = rospy.Rate(2)
	rospy.spin()
