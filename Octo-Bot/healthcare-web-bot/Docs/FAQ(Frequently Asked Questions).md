# Frequently Asked Questions (FAQ)

Q: Why does my program crash in the docker container?

A: Try adding the ```--shm-size 2g``` or ```-v /dev/shm:/dev/shm``` to the ```sudo docker run web-crawler``` command in the ```run.sh``` file.([Click here for more information](https://github.com/SeleniumHQ/docker-selenium/pull/485))

##
Q: How do I login in with another username/password?

A: You can change the username/password that you want to login with in the ```login.json``` file found in ```config``` folder

##
Q: How do I change the values that I want to automate for patient records?

A: You can change the values that you want to login with in the ```measurement.json``` file found in ```config``` folder


##
Q: The bot sometimes fails when running in Octo-Play, why does it happen?

A: This is a known issue for this bot, caused by race conditions when 2 or more different bots try to login using the same account. However, this can be reduced by using more login files and by filling the login files with more admin accounts.

##
Q: Is the bot able to run if the NUSMed server is down or if the user is unable to establish any connection to the website?

A: This bot works by establishing a connection to the NUSMed website to scrape the information. Hence, if the server is down or if the user is unable to establish any connection to the website, the bot will not be able to scrape any information out.