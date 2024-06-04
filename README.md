usage:

DEBUG=1 MESHTASTIC_TCP_HOST=192.168.1.123 uvicorn main:app

debug defaults off, any value turns it on
tcp host defaults to localhost

you will probably want to connect via localho.st:8000 or a similar thing


## Docker Compose
Clone repo and update the enviroment settings in the `docker-compose.yml`
Run `docker compose up -d` to start the container

### Re-build
To re-build the docker image, you can either remove the image `docker image ls` or run `docker compose up -d --build` to force the build