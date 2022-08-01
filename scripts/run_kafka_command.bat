echo off
set arg1=%1 
 
kubectl exec -it %arg1% -- bash -c "kafka-topics --create --bootstrap-server localhost:29092 --replication-factor 1 --partitions 1 --topic Location_Creation --if-not-exists"
