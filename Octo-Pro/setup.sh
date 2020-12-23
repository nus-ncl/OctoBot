#!/bin/sh

sudo apt-get update
sudo apt-get install ansible -y

while true; do
	read -p "Please select your installation target? [Controller (c), Worker(w), All (a), Volume(v), or Exit (e)] " cwave
    case $cwave in
        [Cc]* ) echo "Installing Controller Node"; ansible-playbook -i hosts master-playbook.yml; exit;;
        [Ww]* ) echo "Installing Worker Nodes"; ansible-playbook -i hosts node-playbook.yml; exit;;
        [Aa]* ) echo "Installing Controller and Worker Nodes"; ansible-playbook -i hosts master-playbook.yml; ansible-playbook -i hosts node-playbook.yml; exit;;
        [Vv]* ) echo "Installing NFS and Configuring Shared Volumes"; ansible-playbook -i hosts volume-support-playbook.yaml; exit;;
        [Ee]* ) exit;;
        * ) echo "Please select (c), (w), (a) or (v) ?";;
    esac
done
