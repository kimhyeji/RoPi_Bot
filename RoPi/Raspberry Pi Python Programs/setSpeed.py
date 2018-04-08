import RoPi_SerialCom as ropi
from time import sleep

ropi.setSpeed(52)
ropi.moveForwards()
sleep(1)

ropi.setSpeed(20)
ropi.moveForwards()
sleep(1)

ropi.moveStop()
