xhost +local:docker
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
docker run -d --network=dockernetworktesis --net-alias postgres -e POSTGRES_PASSWORD=postgres -v $(pwd)/postgresdata:/var/lib/postgresql/data 02da44b1d4a6
docker run --network=dockernetworktesis --net-alias facerecognition -m 8GB -it --rm -e DISPLAY=$DISPLAY -v $XSOCK:$XSOCK -v $XAUTH:$XAUTH -e XAUTHORITY=$XAUTH -v ${PWD}:/src -v $(pwd):/app -it c1b77b70f7d1
xhost -local:docker
