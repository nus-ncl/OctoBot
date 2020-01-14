#!/bin/bash

#Set virtual display
Xvfb -ac :99 &
export DISPLAY=:99

#Run the actual jar
java -jar /bot/WebBrowsingBot.jar "$@" 