#include <SmartInventor.h>
#include <Servo.h> 

int speed = 50;               //motor speed

Servo myservo1;      // create servo object to control a servo1
Servo myservo2;      // create servo object to control a servo2

int servo1angle = 90;
int servo2angle = 90;

int servoSteps = 5;

void setup()
{
  SmartInventor.DCMotorUse();  // DC Motor Use

  Serial.begin(115200);       // initialize serial communication at 9600 bits per second:
  
//Set up the digital inputs for the bottom IR sensors
  pinMode(11,INPUT);
  pinMode(12,INPUT);
  pinMode(13,INPUT);
  pinMode(14,INPUT);
  pinMode(16,INPUT);
  pinMode(17,INPUT);
  pinMode(18,INPUT);

  myservo1.attach(27);        // attaches the servo 1 on pin 27 to the servo object 
  myservo2.attach(28);        // attaches the servo 2 on pin 28 to the servo object 

  myservo1.write(servo1angle);          // servo1 to go to position in 90 degrees
  myservo2.write(servo2angle);          // servo2 to go to position in 90 degrees
  
  
}

void loop()
{
  
 byte readbyte;

  //check if the serial monitor has anything sent
 if(Serial.available() > 0)
 {
  readbyte = Serial.read();
  //if there is something sent via the serial monitor save the byte
 }
 
  switch(readbyte)
  {   
  case 76: //character "L"
  
  Serial.print(digitalRead(11));
  Serial.print(" ");
  Serial.print(digitalRead(12));
  Serial.print(" ");
  Serial.print(digitalRead(13));
  Serial.print(" ");
  Serial.print(digitalRead(14));
  Serial.print(" ");
  Serial.print(digitalRead(16));
  Serial.print(" ");
  Serial.print(digitalRead(17));
  Serial.print(" ");
  Serial.print(digitalRead(18));
  Serial.print(" ");
  //------------------------------------------------------------------------  
  case 77:// character "M" 
  SmartInventor.DCMove(forward,speed);                        
  break;  
  //------------------------------------------------------------------------
  case 78:// character "N" 
  SmartInventor.DCMove(backward,speed);         
  break; 
  //------------------------------------------------------------------------
  case 79:// character "O" 
  SmartInventor.DCMove(left,speed); 
  break;
  //------------------------------------------------------------------------
  case 80://character "P"
  SmartInventor.DCMove(right,speed);        
  
  break;
  //------------------------------------------------------------------------
  case 81: //character "Q"
  SmartInventor.DCMove(stop,speed);
  break;
  //------------------------------------------------------------------------
  case 82: //character "R"
  servo1angle = servo1angle - servoSteps;//decrease the position
    if(servo1angle<0)//CHECK NOT BELOW 0
    {
    servo1angle = 0;
    }
    //  Serial.print("servo1:");
    //  Serial.println(servo1angle);
        myservo1.write(servo1angle);
 
  break;
   //------------------------------------------------------------------------
  case 83: //character "S"
   servo1angle = servo1angle + servoSteps;//increase the position
     if(servo1angle>180)
    {
    servo1angle = 180;
    }
    //  Serial.print("servo1:");
    //  Serial.println(servo1angle);
        myservo1.write(servo1angle);
  
  break;
    //------------------------------------------------------------------------
     //========================================================
  case 84: //character "T"
    servo2angle = servo2angle - servoSteps;//decrease the position
   if(servo2angle<0)
    {
    servo2angle = 0;
    }
   //   Serial.print("servo2:");
   //   Serial.println(servo2angle);
        myservo2.write(servo2angle);
  
  break;
     //========================================================
  case 85: //character "U"
    servo2angle = servo2angle + servoSteps;//increase the position
     if(servo2angle>180)
    {
    servo2angle = 180;
    }

    //Serial.print("servo2:");
      //Serial.println(servo2angle);
        myservo2.write(servo2angle);
  break;
  
  
  //MOTOR SPEED
   //========================================================
     
  case 86: //character "V"
  speed = speed - 10;//increase the positio
     if(speed<0)
  {
  speed = 0;
  }
    //Serial.print("speed:");
  //Serial.println(speed);
  break;
  
     //========================================================
   case 87: //character "W"
   
   speed = speed + 10;//increase the position
     if(speed>100)
  {
  speed = 100;
  }
  //Serial.print("speed:");
  //Serial.println(speed);
  break;
  
  
  
  //SERVO STEP SIZE
  
  //========================================================
   case 88: //character "X"
     if(servoSteps<100)
  {
  servoSteps = servoSteps + 1;//increase the position
  }
  //Serial.print("servo step size:");
  //Serial.println(servoSteps);
  break;
 
    //========================================================
  case 89: //character "Y"
     if(servoSteps>0)
  {
  servoSteps = servoSteps - 1;//increase the position
  }
    //Serial.print("servo step size:");
  //Serial.println(servoSteps);
  break;
   //========================================================

  case 90: //character "Z"
  
  Serial.print(servo1angle);
  Serial.print(" ");
  Serial.print(servo2angle);
  Serial.print(" ");
  Serial.print(servoSteps);
  Serial.print(" ");
  Serial.print(speed);
  Serial.print(" ");
    Serial.print(analogRead(19));
  Serial.print(" ");
    Serial.print(analogRead(20));
  Serial.print(" ");
    Serial.print(analogRead(21));
  Serial.print(" ");
  
  Serial.println(" ");
  break;
   //========================================================

  
  default:
  break;
  
  }
  
}  












