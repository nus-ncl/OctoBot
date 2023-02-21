FROM adoptopenjdk/openjdk12:x86_64-ubuntu-jdk-12.0.2_10 

# Set up Chrome
RUN apt-get update
RUN apt-get install software-properties-common wget gnupg gnupg2 -y
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list

# Set up Firefox
RUN add-apt-repository ppa:mozillateam/ppa

# Install softwares
RUN apt-get update
RUN apt-get install firefox-esr xvfb -y
RUN apt-get install google-chrome-stable -y || true
RUN apt-get install -f -y

# Clean up
RUN apt-get autoremove
RUN apt-get autoclean

# Copies the actual jar file over
COPY web-browsing-bot/target/*.jar /bot/
COPY web-browsing-bot/target/classes/drivers/* /bot/drivers/

# Copy entrypoint file
COPY entrypoint.sh /bot/
RUN chmod +x /bot/entrypoint.sh
RUN chmod +x /bot/drivers/geckodriver
RUN chmod +x /bot/drivers/chromedriver

ENTRYPOINT ["/bot/entrypoint.sh"]
