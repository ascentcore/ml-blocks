# ml-blocks

## Build

`docker build -t ml-blocks .`

`docker network create mlblocks_net`

`docker volume create ml-blocks-source`

`docker run -d --network mlblocks_net --hostname rabbitmqhost \
   --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management`

`docker run -d --name ml-blocks-container \
            -p 80:80 \
            --network mlblocks_net \
            --mount src="$(pwd)/app",target=/app/app,type=bind \
            --mount src="$(pwd)/ui/build",target=/app/ui,type=bind \
            --mount src="$(pwd)/data",target=/app/data,type=bind \
            ml-blocks`