#!/bin/bash

#Set virtual display
Xvfb -ac :99 &
export DISPLAY=:99

#Run the actual jar
java -jar /bot/web-browsing-bot-1.0-SNAPSHOT-jar-with-dependencies.jar "$@" 
