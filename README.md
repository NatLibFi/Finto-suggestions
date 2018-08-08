# Finto-suggestions (Ontology Suggestion Platform)

## Architecture

A Docker setup for development has been created with docker-compose. It consists of three containers: API (Python3.6/Flask), Frontend (Vue.js) and Nginx forward-proxy. Nginx proxies both Flask API (localhost:8080/api) and Vue.js frontend (localhost:8080/) to host machine's port 8080. API Uses a PostgreSQL database for data persistence.

```
                localhost:8080
                     +
                     |
+------------------------------------------+
|                    | :8080               |
|               +----v-----+               |
|               |          |               |
|               |  NGINX   |               |
|               |          |               |
|               +----------+               |
|                   |  |                   |
|             /api  |  |  /*               |
|                   |  |                   |
|         :8050     |  |    :8040          |
|      +----------+ |  | +----------+      |
|      |          | |  | |          |      |
| +---->   API    <-+  +->   WEB    |      |
| |    |          |      |          |      |
| |    +----------+      +----------+      |
| |     Flask API       Vue.js frontend    |
| |                                        |
| |       :5432                            |
| |    +----------+                        |
| |    |          |                        |
| +---->   PSQL   |                        |
|      |          |                        |
|      +----------+                        |
|                                          |
+------------------------------------------+


http://asciiflow.com/
```

```
.
├── api               # Python backend code (API)
├── docker            # Dockerfiles and configurations
│   ├── api
│   ├── nginx
│   └── web
└── web               # Vue.js frontend
    ├── node_modules
    ├── public        # Static files
    ├── src           # Frontend code
    └── tests         # Frontend tests
```

## Development Environment Installation

Download and install [Docker CE](https://docs.docker.com/install/) to your computer. Docker-compose should be included with the installation.

1.  Start the freshly installed Docker
2.  run `docker-compose up` in this project's root folder. This command builds the required containers (api, web and nginx) and starts them. Hitting `CTRL+C` should exit the output feed from docker. However the containers should still be running. You can check the container status with a command `docker ps`.
3.  Test the installation. Nginx should forward both the frontend and API to localhost:8080. You should see a simple Vue.js frontend running on localhost:8080/ (served from web directory)and a simple API on localhost:8080/api (served from api directory).
4.  All the running (composed) containers can be halted with command `docker-compose down`.

You can start developing! Both api and web services should reload automatically.

## Development Workflow

Both API and Frontend can be developed simultaneously. All the changes to the code should update automatically without any restarts.

## Frontend

Frontend is initialized with vue-cli (beta 3.0, https://github.com/vuejs/vue-cli).

Add new dependencies `npm install package-name` or `npm install package-name --save-dev`. In this case, you need to rebuild the containers by running `docker-compose build web`. You need to have node installed on your computer to do this. You could also just simply modify package.json.

Frontend can also be run locally (without docker). Please make sure that you have Python3 installed on your computer. Run `pip install pipenv && pipenv install` in /api directory to install required packages. After this you can start the api serve by running `pipenv run python app.py`.

## Backend (API)

Backend (API) is a simple Python webapp. Dependency management is handled by Pipenv ()

Add new dependencies by running `pipenv install package-name` or `npm install package-name --dev` on your own computer. Afterwards, rebuild api container `docker-compose build api`. You need to have Python3 and pipenv installed to do this locally.

Backend can be run locally (without docker). You should have node installed. Run `npm install` in /web directory to install required dependencies. After that you can start the development server by running `npm run serve`.