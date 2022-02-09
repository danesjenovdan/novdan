#!/bin/bash

sudo docker login rg.fr-par.scw.cloud/djnd -u nologin -p $SCW_SECRET_TOKEN

# BUILD AND PUBLISH NOVDAN FRONTEND
sudo docker build -f novdan_frontend/Dockerfile -t novdan-frontend-staging:latest ./novdan_frontend
sudo docker tag novdan-frontend-staging:latest rg.fr-par.scw.cloud/djnd/novdan-frontend-staging:latest
sudo docker push rg.fr-par.scw.cloud/djnd/novdan-frontend-staging:latest

# BUILD AND PUBLISH NOVDAN API
sudo docker build -f novdan_api/Dockerfile -t novdan-api-staging:latest ./novdan_api
sudo docker tag novdan-api-staging:latest rg.fr-par.scw.cloud/djnd/novdan-api-staging:latest
sudo docker push rg.fr-par.scw.cloud/djnd/novdan-api-staging:latest
