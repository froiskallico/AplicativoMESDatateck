#!/bin/sh

##################################################
# Script para instalação completa do sistema MES #
#                                                #
#                Powered by TRI                  #
#      Tecnologia | Resultados | Inovação        #
#                                                #
#        Author: Kallico Fróis - 2019/06         #
#                                                #
##################################################

### Package Manager Update
sudo apt-get update &
sudo apt-get upgrade -y

### Install Python3 and GIT
sudo apt-get install python3
sudo apt-get install git

### Clone APP Git Repo into TRI directory
git clone https://froiskallico@github.com/froiskallico/AplicativoMESDatateck TRI

### Install App Dependencies
pip install -r ~/TRI/requirements.txt

### Copy Systemctl Services and enable it
sudo cp ~/TRI/services/app.service /etc/systemd/system/
sudo cp ~/TRI/services/importaLista.service /etc/systemd/system/

sudo systemctl enable app.service
sudo systemctl enable importaLista.service

sudo systemctl daemon-reload
