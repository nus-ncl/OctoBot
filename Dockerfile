FROM openjdk:11

# Set up Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list

# Install softwares
RUN apt-get update 
RUN apt-get install firefox-esr google-chrome-stable xvfb -y

# Copies the actual jar file over
COPY web-browsing-bot/target/build/*.jar /bot/
COPY web-browsing-bot/target/build/lib/* /bot/lib/
COPY web-browsing-bot/target/build/drivers/* /bot/drivers/

# Copy entrypoint file
COPY entrypoint.sh /usr/sbin/

ENTRYPOINT ["entrypoint.sh"]
