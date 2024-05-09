<div align="center">
<h1 align="center">FastAPI Integrated with gRPC simple Calculator App</h1>
<h3 align="center">Sample Project of how to use grpc and fastapi in a microservice architecture</h3>
</div>
<p align="center">
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://fastapi.tiangolo.com/" target="_blank"> <img src="https://styles.redditmedia.com/t5_22y58b/styles/communityIcon_r5ax236rfw961.png" alt="fastapi" width="40" height="40"/> </a>
<a href="https://www.docker.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://grpc.io/" target="_blank"> <img src="https://grpc.io/img/logos/grpc-icon-color.png" alt="grpc" width="40" height="40"/> </a>
<a href="https://git-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a>
</p>

# Guideline
- [Guideline](#guideline)
- [Goal](#goal)
- [Development usage](#development-usage)
  - [Clone the repo](#clone-the-repo)
  - [Docker Compose](#docker-compose)
  - [Build everything](#build-everything)
- [License](#license)


# Goal
This project is meant to be a guidance of how to setup very simple grpc server


# Development usage
You'll need to have [Docker installed](https://docs.docker.com/get-docker/).
It's available on Windows, macOS and most distros of Linux. 

If you're using Windows, it will be expected that you're following along inside
of [WSL or WSL
2](https://nickjanetakis.com/blog/a-linux-dev-environment-on-windows-with-wsl-2-docker-desktop-and-more).

That's because we're going to be running shell commands. You can always modify
these commands for PowerShell if you want.


## Clone the repo
Clone this repo anywhere you want and move into the directory:
```bash
git clone https://github.com/Muhammadkomron/gRPC-calculator.git
```

## Docker Compose
The config file includes 2 services:
- calculator_api : fastapi application to handle requests
- calculator_grpc : grpc server to serve calculation

```yaml
version: "3.8"

volumes:
  calculator_api_volumes: {}
  calculator_grpc_volumes: {}

services:

  calculator_api:
    build:
      context: ./api
      dockerfile: ./Dockerfile
    container_name: calculator_api
    volumes:
      - calculator_api_volumes:/app:cached
    restart: on-failure
    ports:
      - "8000:8000"
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

  calculator_grpc:
    build:
      context: ./grpc
      dockerfile: ./Dockerfile
    container_name: calculator_grpc
    volumes:
      - calculator_grpc_volumes:/app:cached
    restart: on-failure
    expose:
      - 50051
      - 8000
    command: ["python", "main.py"]

```


## Build everything

*The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images and build the Python + requirements dependencies.*

```bash
docker compose up --build
```

Now that everything is built and running we can treat it like any other FastAPI
app. Visit <http://0.0.0.0:8000/docs> in your favorite browser.

**Note:** If you receive an error about a port being in use? Chances are it's because
something on your machine is already running on port 8000. then you have to change the docker-compose.yml file according to your needs.


# License

You can share the source code or use it in learning purposes.
