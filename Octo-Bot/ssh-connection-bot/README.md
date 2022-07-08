# Overview
The bot is specially designed to implement:
1. To create concurrent SSH session in SSHD Server
2. To create concurrent SSH session in REMOTE Server
3. To upload file through SSH server using SCP
4. To download file through SSH server using SCP

# Build the Docker image
Build before we can run the executor of the bot using this container image. 

```shell
docker build -t ssh-connection-bot:latest .
```
# Arguments
Some additional parameters that can be configured for the bot are:

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

--JUMP              1/0 to enable/disable jump test, default=0

--UPLOAD            1/0 to enable/disable scp upload little_file to \
                    REMOTE_SERVER:/tmp/little_file and you check \
                    results at remote server, default=0

--DOWNLOAD          1/0 to enable/disable scp download \
                    SSHD_SERVER:/tmp/downloaded_file and then \
                    you can check results from the output, default=0

```

# Preparation for the SSH server

1. Install the `openssh-server` at `SSHD_SERVER`
2. Enable ssh pasword login by adding this line
  `PasswordAuthentication yes` in /etc/ssh/sshd_config

and then:
- for `--CONCURRENCY 1` & `'--JUMP 1'`, nothing else to do. The 
result is printing 'hello' repeatedly


- for `--UPLOAD 1`, nothing else to do and it will upload the `little_file` by default. If you want to customize the 
  file to be uploaded, create your own `little_file` and re-build the image


- for `--DOWNLOAD 1`, make sure there is a file called `downloaded_file` under `/tmp` folder in the `REMOTE_SERVER`

# Run
## Run single bot manually
```shell
docker run -d ssh-connection-bot --SSHD_USERNAME <sshd_username> --SSHD_SERVER <sshd_server_ip> --SSHD_PASSWORD <sshd_password> --CONCURRENCY 1
docker run -d ssh-connection-bot --SSHD_USERNAME <sshd_username> --SSHD_SERVER <sshd_server_ip> --SSHD_PASSWORD <sshd_password> --REMOTE_SERVER <remote_server> --REMOTE_USERNAME <remote_username> --REMOTE_PASSWORD <remote_password> --JUMP 1
docker run -d ssh-connection-bot --SSHD_USERNAME <sshd_username> --SSHD_SERVER <sshd_server_ip> --SSHD_PASSWORD <sshd_password> --REMOTE_SERVER <remote_server> --REMOTE_USERNAME <remote_username> --REMOTE_PASSWORD <remote_password> --UPLOAD 1
docker run -d ssh-connection-bot --SSHD_USERNAME <sshd_username> --SSHD_SERVER <sshd_server_ip> --SSHD_PASSWORD <sshd_password> --REMOTE_SERVER <remote_server> --REMOTE_USERNAME <remote_username> --REMOTE_PASSWORD <remote_password> --DOWNLOAD 1
```
*note: If you want to simply upload/download a file to/from the `SSHD_SERVER`, you MAY NOT specify put `<remote_server>`, `<remote_username>` & `<remote_password>` since they're using 
the same value of `<sshd_server>`, `<sshd_username>`  & `<sshd_password>` respectively by default. 

## Run multiple bots automatically with Octo-Play
Use the template to run bots using Octo-Play (please check and amend the yaml file in [play-example](play-example/) directory)



