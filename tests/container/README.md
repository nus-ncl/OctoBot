## Building Container-based Testing Environment with Kind

[Kind](https://kind.sigs.k8s.io/docs/) lets we run Kubernetes cluster on your 
local computer using Docker container “nodes”. So, this tool requires that you 
have Docker Container Engine installed and configured.

### Prerequisites

This Kind installation is tested with this following environment:

- Ubuntu Linux 18.04.04 LTS
- Docker Engine 5:20.10.0~3-0~ubuntu-bionic
- Kind 0.9.0
- Kubernetes 1.9.1
- kubectl 1.9.1


### Installation and Configuration

#### Install Docker Engine from Repository 
 
Please find below a combine steps to get started with Docker Engine on Ubuntu.
It consists of removing old version of Docker, install prerequisite packages, 
configure the repository, install Docker Engine and assign user to run Docker.
 
```console
sudo apt-get update
sudo apt-get -y autoremove docker docker-engine docker.io containerd runc
sudo apt-get -y install apt-transport-https ca-certificates \
    curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
```

The original installation procedure can be found 
[here](https://docs.docker.com/engine/install/ubuntu/

*Note*: You may need to logout and login again before go to the next step!

#### Install Kind Binary from the Repository 

Stable binaries are also available on the releases page. Stable releases are 
generally recommended for CI usage in particular. To install, download the 
binary for your platform from “Assets” and place this into your $PATH.

```console
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.9.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/bin/kind
```

The detail installation step can be found 
[here](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
 
#### Create cluster  
 
Creating a Kubernetes cluster in Kind is as simple as single command below:

```console
kind create cluster
```
The output will be something like this:
```console
Creating cluster "kind" ...
  ✓ Ensuring node image (kindest/node:v1.19.1) 🖼 
  ✓ Preparing nodes 📦  
  ✓ Writing configuration 📜 
  ✓ Starting control-plane 🕹️ 
  ✓ Installing CNI 🔌 
  ✓ Installing StorageClass 💾 
  Set kubectl context to "kind"
  You can now use your cluster with:
 
  kubectl cluster-info --context kind-kind
 
  Not sure what to do next? 😅 Check out https://kind.sigs.k8s.io/docs/user/quick-start/
```

The detail how to create cluster can be found 
[here](https://kind.sigs.k8s.io/docs/user/quick-start/#creating-a-cluster)

#### Install _kubectl_ from the Source Code 

The Kubernetes command-line tool, _kubectl_, allows you to run commands against 
Kubernetes clusters. You can use _kubectl_ to deploy applications, inspect and 
manage cluster resources, and view logs.

Please find below on how to download and install _kubectl_ and set it up for 
accessing your cluster. We select _kubectl_ `v1.19.1` release to match with 
Kubernetes version as mentioned in the Kind installation.

```console
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.19.1/bin/linux/amd64/kubectl
chmod +x ./kubectl 
sudo mv kubectl /usr/bin/
kubectl cluster-info
```

### Verification

Check Docker installation
```console
docker run hello-world
```

Check cluster installation
```console
kind get clusters
```

Check the Kubectl tools
```console
kubectl version --client
```

Check the deployment result
```console
kubectl apply -f https://k8s.io/examples/application/deployment.yaml
kubectl get pods
```

If everything are good, congratulation! You can continue to use our OctoBot.
Please start with *Octo-Play* guide 
[here](https://github.com/nus-ncl/OctoBot/tree/master/Octo-Play) or *Octo-App*
[here](https://github.com/nus-ncl/OctoBot/tree/master/Octo-App).