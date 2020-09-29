## Building testing environment with Vagrant

### Prerequisites

This Vagrant installation is tested with this following environment:

- Ubuntu Linux 16.04.03 LTS (but it should working newer version)
- Oracle VirtualBox 5.1.38
- Vagrant 2.2.10
- Vagrant Box (image) for Generic Ubuntu Linux 18.04 

### Download the Source Code 
 
Download the whole source of OctoBot software from the GitHub and move to 
`tests/vm`directory.
 
```console
ncl@host:~$ git clone https://github.com/nus-ncl/OctoBot
ncl@host:~$ cd OctoBot/tests/vm
```

### (Optional) Modify the `Vagrantfile` and `hosts` file 
 
By default this `Vagrantfile` only install and configure one controller (master)
and two worker (nodes). If you want to run more than two workers (up to 10 nodes),
you need to change this line in `Vagrantfile`
 
```console
...
  N = <number_of_worker_nodes>
... 
```

You need also add the additional worker node information in the `hosts` file.

```console
[node]
...
octobot<index>  ansible_ssh_host=127.0.0.1 ansible_ssh_port=220<index-1> ansible_user=vagrant
```

for example to add `octobot4` as the worker node, you need to add:

```console
octobot4  ansible_ssh_host=127.0.0.1 ansible_ssh_port=2203 ansible_user=vagrant
```

### Build the testing VMs

In order to start VirtualBox VMs installation and configuration, please use this
command:

```console
ncl@host:/mnt/OctoBot/tests/vm$ chmod 755 python-install.sh
ncl@host:/mnt/OctoBot/tests/vm$ vagrant up
```

### Verify you installation and configuration

In order to start verify all the VMs installation and configuration, you need 
to access to the `octobot0` (controller) node and ensure the Kubernetes cluster 
has been built successfully.

```console
ncl@host:~/vm$ vagrant ssh octobot0
vagrant@controller:~$ kubectl get nodes -o wide
```

### Troubleshooting

If the Vagrant process is stopped/hang while creating VMs (due to timeout or 
misconfiguration), you may force it to stop and destroy the problematic VMs 
before you can start the `vagrant up` again.

```console
ncl@host:/mnt/OctoBot/tests/vm$ vagrant destroy <problematic_vm_name>
ncl@host:/mnt/OctoBot/tests/vm$ vagrant up
```