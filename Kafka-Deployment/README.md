# Kafka-Deployment
## Overview
### Background
a dedicated deployment to Kafka, using the famous contributer confluentinc, following the steps in https://blog.datumo.io/setting-up-kafka-on-kubernetes-an-easy-way-26ae150b9ca8

### Running 

docker apply -f zookeper-deployment.yaml 

then run 

docker apply -f kafka-deployment.yaml