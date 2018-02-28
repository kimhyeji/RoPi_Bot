import RoPi_SerialCom
import time

while(1):
    a,b,c,d,e,f,g = RoPi_SerialCom.requestData()
    print(a,b,c,d,e,f,g)
    d11,d12,d13,d14,d16,d17,d18 = RoPi_SerialCom.requestBottomIRSensors()
    print(d11,d12,d13,d14,d16,d17,d18)
