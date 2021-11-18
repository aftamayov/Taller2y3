#!/bin/bash
Temp=$(cat /sys/bus/w1/devices/28-3c01d0753ed9/temperature)
Temp=$(echo "scale=2; $Temp/1000" | bc -l)
echo $(date +%Y%m%d\ %H:%M:%S)";"$Temp"°C" >> /home/pi/Sys_Emb/Taller_1/Punto2/$(date +%Y%m%d)_TEMPERATURA.csv

