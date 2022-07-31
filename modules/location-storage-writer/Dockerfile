# syntax = docker/dockerfile:1.0-experimental
# DOCKER_BUILDKIT=1 docker build . -f location/Dockerfile -t location --secret id=ca.key,src=ca.key

FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY location-storage-writer/ /service/location/ 

WORKDIR /service/location
RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/location.proto 

EXPOSE 5000
ENTRYPOINT [ "python", "locations.py" ]
