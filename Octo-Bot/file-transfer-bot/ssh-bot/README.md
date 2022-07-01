# Overview
The bot is specially designed to implement:
1. ssh concurrent session test
2. scp upload functionality
3. scp download functionality

# Compile the docker image
```shell
docker build -t ssh-bot:latest .
```
# Arguments
```shell
--REMOTE_SERVER     destination server, default='localhost'

--REMOTE_PORT       destination server port, default=22

--REMOTE_USERNAME   destination server login username

--SSHD_USERNAME     SSHD server username

--SSHD_SERVER       SSHD server ip

--CONCURRENCY       1/0 to enable/disable concurrency test, default=0

--UPLOAD            1/0 to enable/disable scp upload little_file to \
                    REMOTE_SERVER:/tmp/little_file and you check \
                    results at remote server, default=0

--DOWNLOAD          1/0 to enable/disable scp download \
                    SSHD_SERVER:/tmp/downloaded_file and then \
                    you can check results from the output, default=0

```

# Prepare
To enable ssh login without password, this bot comes with a pair of private&public keys. You need to upload the public key
`id_rsa.pub` to the `SSHD_SERVER` by means of the utility `ssh-copy-id`.
```shell
ssh-copy-id -i id_rsa.pub <SSHD_USERNAME>@<SSHD_SERVER>
```
and then:
- for `--CONCURRENCY 1`, nothing else to do


- for `--UPLOAD 1`, nothing else to do and it will upload the `little_file` by default. If you want to customize the 
  file to be uploaded, create your own `little_file` and re-build the image


- for `--DOWNLOAD 1`, make sure there is a file called `downloaded_file` under `/tmp` folder in the `REMOTE_SERVER`
# Run
##run it manually
```shell
docker run -d ssh-bot --SSHD_USERNAME <sshd_username> --SSHD_SERVER <sshd_server_ip> --CONCURRENCY 1
docker run -d ssh-bot --SSHD_USERNAME <sshd_username> --SSHD_SERVER <sshd_server_ip> --REMOTE_USERNAME <remote_username> --UPLOAD 1
docker run -d ssh-bot --SSHD_USERNAME <sshd_username> --SSHD_SERVER <sshd_server_ip> --REMOTE_USERNAME <remote_username> --DOWNLOAD 1
```
*note: If you want to simply upload/download a file to/from the sshd_server, put `<remote_username>` the same as `<sshd_username>`  

##run it automatically
run it automatically using Octobot-Play(Plz check and amend the yaml file in this folder)



