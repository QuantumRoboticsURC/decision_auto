# decision_auto
## Quick Start

1. Ejecuta con el siguiente comando

```
$ roslaunch decision_auto decision_auto.launch
```
2. Lanzar el siguiente falso publicador

```
$ rostopic pub /vision/obstacle_bool std_msgs/String "'0000000000000000000000000000000000000000000000000000000000000000000000'"
```
```
$ rostopic pub /vision/obstacle_bool std_msgs/String "'1110000000000000000000000000000000000000000000000000000000000000000000'"
```
```
$ rostopic pub /vision/obstacle_bool std_msgs/String "'0000000000000000000000000000000000000000000000000000000000000000000111'"
```
```
$ rostopic pub /vision/obstacle_bool std_msgs/String "'0000000000000000000000000000000001110001110000000000000000000000000000'"
```

3. Normal output:

```
