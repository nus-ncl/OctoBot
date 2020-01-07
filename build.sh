#Set permissions
chmod a+x *.sh &&

#Compile java program
cd web-browsing-bot &&
mvn clean install &&

cd .. &&
docker build . -t browsing-bot
