# Sample
There are two samples, one using the CTFd website hosted locally and the other using Outlook Web Access (OWA).

## CTFd
The actions in the json file tells sets up CTFd automatically, creates new pages and new challenges.

Go to the ```sample/CTFd``` and run ```docker-compose up```.
```console
whyare@BrowsingBot:~$ git clone https://github.com/CTFd/CTFd.git
whyare@BrowsingBot:~$ cd CTFd/
whyare@BrowsingBot:~/CTFd$ docker-compose up
```

Run the bot. (Please replace <ip_address> with the IP address of the machine running docker)
```console
whyare@BrowsingBot:~/webbrowsingbot/sample$ sudo docker run -it --rm \
browsing-bot \
--login "$(cat ctfd_login.json)" \
--action "$(cat ctfd_action.json)" \
<ip_address>:8000
```

## Outlook
Open the following files and edit the values in the ```<>``` brackets:
* outlook_login.json (\<email\> and \<password\>)
* outlook_action.json (\<toEmail\>)

Run the bot
```console
whyare@BrowsingBot:~/webbrowsingbot/sample$ sudo docker run -it --rm \
browsing-bot \
--login "$(cat outlook_login.json)" \
--action "$(cat outlook_action.json)" \
outlook.live.com
```
