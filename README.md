## Usage:

```
DEBUG=1 MESHTASTIC_TCP_HOST=192.168.1.123 uvicorn main:app
```

or

```
MESHTASTIC_BLE_MAC=AB:CD:EF:01:23:45 uvicorn main:app
```

`DEBUG` defaults off, any value turns it on
BLE is tried first; if empty, TCP is tried; if empty, `localhost` is tried

You will probably want to connect via `localho.st:8000` or something else that gives you a real hostname, because using plain `localhost` will have CORS restrictions.

At present TLS is not supported, but this could probably work behind Caddy or nginx or something like that. I just haven't tried it.

## Docker Compose

After cloning the repository, update the environment variables in `docker-compose.yml` to match TCP or BLE connection & debug settings as desired.

Run `docker compose up -d` to start the container

### Re-build

To re-build the docker image, you can either remove the image by using `docker image ls` and then `docker image rm` on the appropriate image, or run `docker compose up -d --build` to force a rebuild through docker-compose.
