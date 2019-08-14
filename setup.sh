#/bin/sh

while true; do
	read -p "Please select your installation target? [Controller (c), Worker(w), All (a) or Exit (e)] " cwae
    case $cwae in
        [Cc]* ) echo "Installing Controller Node"; ansible-playbook -i hosts master-playbook.yml; exit;;
        [Ww]* ) echo "Installing Worker Nodes"; ansible-playbook -i hosts node-playbook.yml; exit;;
	[Aa]* ) echo "Installing Controller and Worker Nodes";exit;;
	[Ee]* ) exit;;
	* ) echo "Please select (c), (w) or (a)";;
    esac
done
