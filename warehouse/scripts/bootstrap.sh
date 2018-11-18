#!/usr/bin/env bash
echo "####---- Docker Host $(hostname) Provisioning ----####"
apt-get update

echo "#### Installing prerequisites."
apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
apt-get install -y curl

echo "#### Installing Docker."
curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce

echo "#### Adjusting user settings."
groupadd docker
usermod -aG docker vagrant
usermod -aG docker fury

echo "#### Docker installation done."