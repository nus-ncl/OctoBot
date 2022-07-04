# Overview
The bot is specially designed to implement:
1. ssh concurrent session test
2. scp upload functionality
3. scp download functionality

# Compile the docker image
```shell
docker build -t ssh-bot:sshpass .
```
# Arguments
```shell
--REMOTE_SERVER     destination server, default='localhost'

--REMOTE_PORT       destination server port, default=22

--REMOTE_USERNAME   destination server login username, default={SSHD_USERNAME}

--REMOTE_PASSWORD   destination server login password, default={SSHD_PASSWORD}

--SSHD_USERNAME     SSHD server username

--SSHD_SERVER       SSHD server ip

--SSHD_PASSWORD     SSHD server password

--SSHD_PORT         SSH server port, default=22

--CONCURRENCY       1/0 to enable/disable concurrency test, default=0

--UPLOAD            1/0 to enable/disable scp upload little_file to \
                    REMOTE_SERVER:/tmp/little_file and you check \
                    results at remote server, default=0

--DOWNLOAD          1/0 to enable/disable scp download \
                    SSHD_SERVER:/tmp/downloaded_file and then \
                    you can check results from the output, default=0

```

# Prepare
1. Install the `openssh-server` at `SSHD_SERVER`
2. Enable ssh pasword login by adding this line
  `PasswordAuthentication yes` in /etc/ssh/sshd_config
```
and then:
- for `--CONCURRENCY 1`, nothing else to do


- for `--UPLOAD 1`, nothing else to do and it will upload the `little_file` by default. If you want to customize the 
  file to be uploaded, create your own `little_file` and re-build the image


- for `--DOWNLOAD 1`, make sure there is a file called `downloaded_file` under `/tmp` folder in the `REMOTE_SERVER`

```
# Run
##run it manually
```shell
docker run -d ssh-bot --SSHD_USERNAME <sshd_username> --SSHD_SERVER <sshd_server_ip> --SSHD_PASSWORD <sshd_password> --CONCURRENCY 1
docker run -d ssh-bot --SSHD_USERNAME <sshd_username> --SSHD_SERVER <sshd_server_ip> --SSHD_PASSWORD <sshd_password> --REMOTE_USERNAME <remote_username> --REMOTE_PASSWORD <remote_password> --UPLOAD 1
docker run -d ssh-bot --SSHD_USERNAME <sshd_username> --SSHD_SERVER <sshd_server_ip> --SSHD_PASSWORD <sshd_password> --REMOTE_USERNAME <remote_username> --REMOTE_PASSWORD <remote_password> --DOWNLOAD 1
```
*note: If you want to simply upload/download a file to/from the `SSHD_SERVER`, you MAY NOT specify put `<remote_username>` & `<remote_password>` since they're using 
the same value of `<sshd_username>`  & `<sshd_password>` respectively by default. 

##run it automatically
run it automatically using Octobot-Play(Plz check and amend the yaml file in `Octo-Play/ssh-bot-play/`)



