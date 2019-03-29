# ABC

Annoying Bioinformatic Commands

## Requirements

### step 1 - install git

```bash
yum install git
```

### step 2 - intall docker

for centos7 -> [source](https://github.com/NaturalHistoryMuseum/scratchpads2/wiki/Install-Docker-and-Docker-Compose-%28Centos-7%29)

```bash
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install docker-ce
usermod -aG docker $(whoami)
systemctl enable docker.service
systemctl start docker.service
```


## Installation

```bash
git clone https://github.com/vincentzilliox/ABC.git
```

## Start Services

```bash
cd ABC
./restart_services.sh
```

## Interface

Go to: 
[localhost](https://0.0.0.0:5000)
