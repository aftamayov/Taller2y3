#include<wiringPi.h>
int main (void)
{
wiringPiSetup();
pinMode(0,OUTPUT);
int i = 0;
for(i = 0; i<20000;i++)
{
if (digitalRead(0)== LOW)
{
digitalWrite(0,HIGH);
}

if (digitalRead(0)== HIGH)
{
digitalWrite(0,LOW);
}
}
return 0;
}

