# ml-blocks

## Build

`docker build -t ml-blocks .`

`docker volume create ml-blocks-source`

`docker run -d --name ml-blocks-container \
            -p 80:80 \
            --mount src="$(pwd)/app",target=/app/app,type=bind \
            --mount src="$(pwd)/ui/build",target=/app/ui,type=bind \
            --mount src="$(pwd)/data",target=/app/data,type=bind \
            ml-blocks`