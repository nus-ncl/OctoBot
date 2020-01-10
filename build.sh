#Set permissions
chmod a+x *.sh &&

if [[ ! -d "web-browsing-bot/target/build/" ]]
then
    cd web-browsing-bot
    mvn clean install
    cd ..
fi

sudo docker build . -t browsing-bot
