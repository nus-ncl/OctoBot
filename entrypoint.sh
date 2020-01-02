#!/bin/bash

#Set virtual display
Xvfb -ac :99 -screen 0 1280x1024x16 &
export DISPLAY=:99

#Run the actual jar
java -jar /bot/WebBrowsingBot.jar $@