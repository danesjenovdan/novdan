#!/bin/bash

sudo docker login rg.fr-par.scw.cloud/djnd -u nologin -p $SCW_SECRET_TOKEN

# BUILD AND PUBLISH NOVDAN
sudo docker build -f landing/novdan/Dockerfile -t novdan-frontend:latest ./landing/novdan
sudo docker tag novdan-frontend:latest rg.fr-par.scw.cloud/djnd/novdan-frontend:latest
sudo docker push rg.fr-par.scw.cloud/djnd/novdan-frontend:latest
