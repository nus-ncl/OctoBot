FROM openjdk:11

#Install softwares
RUN apt-get update 
RUN apt-get install firefox-esr xvfb -y

#Copies the actual jar file over
COPY web-browsing-bot/target/build/*.jar /bot/
COPY web-browsing-bot/target/build/lib/* /bot/lib/
COPY web-browsing-bot/target/build/drivers/* /bot/drivers/

#Copy entrypoint file
COPY entrypoint.sh /usr/sbin/

ENTRYPOINT ["entrypoint.sh"]
