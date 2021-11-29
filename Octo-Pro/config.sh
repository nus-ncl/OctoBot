#!/bin/sh
# Script to configure OctoBot Provisioning component.
# Author : Aris C. Risdianto
# Update : November 2021
#
# Usage:
# ./config.sh
#
# Select between "c", "w", "a" or "e"

while true; do
	read -p "Please select your configuration target? [Controller (c), Worker(w), All (a), or Exit (e)] " cwae
    case $cwae in
        [Cc]* ) echo "Configuring Controller Node"; ansible-playbook -i hosts master-playbook.yml --tags configure; exit;;
        [Ww]* ) echo "Configuring Worker Nodes"; ansible-playbook -i hosts node-playbook.yml --tags configure; exit;;
        [Aa]* ) echo "Configuring Controller and Worker Nodes"; ansible-playbook -i hosts master-playbook.yml --tags configure; ansible-playbook -i hosts node-playbook.yml --tags configure; exit;;
        [Ee]* ) exit;;
        * ) echo "Please select (c), (w), (a) or (e)?";;
    esac
done
