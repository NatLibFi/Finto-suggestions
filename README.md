# Finto-suggestions (Ontology Suggestion Platform)

## Architecture

A Docker setup for development has been created with docker-compose. It consists of three containers: API (Python3.6/Flask), Frontend (Vue.js) and Nginx forward-proxy. Nginx proxies both Flask API (localhost:8080/api) and Vue.js frontend (localhost:8080/) to host machine's port 8080. API Uses a PostgreSQL database for data persistence.

```
                localhost:8080
                     +
                     |
+----------------------------------------+
|                    | :8080             |
|               +----v-----+             |
|               |          |             |
|               |  NGINX   |             |
|               |          |             |
|               +----------+             |
|                   |  |                 |
|             /api  |  |  /*             |
|                   |  |                 |
|         :8050     |  |    :8040        |
|      +----------+ |  | +----------+    |
|      |          | |  | |          |    |
| +---->   API    <-+  +->   WEB    |    |
| |    |          |      |          |    |
| |    +----------+      +----------+    |
| |     Flask API       Vue.js frontend  |
| |                                      |
| |       :5432                          |
| |    +----------+                      |
| |    |          |                      |
| +---->   PSQL   |                      |
|      |          |                      |
|      +----------+                      |
|                                        |
+----------------------------------------+

http://asciiflow.com/
```

```
.
├── api                     # Backend code (Python, Connexion, Flask etc.)
│   ├── api                 # API specific code, logic and Swagger API definitions
│   │   ├── logic
│   │   └── specification
│   ├── migrations          # Alembic migrations (with Flask-migrate plugin)
│   │   └── versions
│   └── tests               # Integration and unit tests
├── docker                  # Dockerfiles and configurations
│   ├── api
│   ├── nginx
│   └── web
└── web                     # Vue.js frontend
    ├── node_modules
    ├── public              # Static files
    ├── src                 # Frontend code (Javascript, Vue.js)
    │   ├── assets
    │   ├── components
    │   └── views
    └── tests               # Frontend tests
```

## Installation and Development

### Setting up Development Environment

FIRST: Copy or clone Git repository and checkout the `develop` branch

1.  Copy the .env.default file and rename it to .env (from project root)
2.  Modify the environment variables in .env as desired
3.  If you are not going to use Linux, download and install [Docker CE](https://docs.docker.com/install/) (The Docker Engine package is now called docker-ce) to your computer and Docker Compose should be included with the installation. If you are using Debian Linux, you should first install the [Docker Engine](https://docs.docker.com/engine/install/debian/) and then download and install [Doker Compose](https://docs.docker.com/compose/install/) separately. For Debian 10 Buster instruction can be found [here](https://computingforgeeks.com/install-docker-and-docker-compose-on-debian-10-buster/). 
3.1 For Debian 10 Buster:
    - sudo apt update
    - sudo apt -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common
    - curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
    - sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
    - sudo apt update
    - sudo apt -y install docker-ce docker-ce-cli containerd.io
    - sudo apt install -y curl
    - curl -s https://api.github.com/repos/docker/compose/releases/latest \
        | grep browser_download_url \
        | grep docker-compose-Linux-x86_64 \
        | cut -d '"' -f 4 \
        | wget -qi -
    - chmod +x docker-compose-Linux-x86_64
    - sudo mv docker-compose-Linux-x86_64 /usr/local/bin/docker-compose
    - docker-compose version
    - sudo usermod -aG docker $USER
    - newgrp docker
    - docker version
    - exit (log out and log in)
    - docker run --rm -it  --name test alpine:latest /bin/sh
    - cat /etc/os-release
    - exit
    - mv docker-compose.yml docker-compose.will_be_in_use
    - vim docker-compose.yml
    -> Paste and save the next following:
        version: '3'  
        services:
        web:
            image: nginx:latest
            ports:
            - "8080:80"
            links:
            - php
        php:
            image: php:7-fpm
    - docker-compose up -d
    - docker-compose down
    - mv docker-compose.yml docker-compose.ymlForTestingPurposes
    - mv docker-compose.will_be_in_use docker-compose.yml 


4.  Download and install [Python 3.7+](https://www.python.org/downloads/) and after that install pipenv with command `pip install pipenv`. Pipenv is used to install/remove packages and run scripts api-side.
5. Download and install latest LTS Node.Js (https://nodejs.org/en/download/)
6.  Start the freshly installed Docker
7.  Run `docker-compose up --build` in project's **root** folder (you can add `-d` to run this in the background). This command builds the required containers (api, web and nginx) and starts them. You can check the container status with a command `docker ps` in another command line tab.
8.  Initialize the database. In the api directory (while the containers are running), run `pipenv run upgrade-db`
9. Go to the frontpage (**localhost:8080**) and create a new user for comments originally imported from GitHub. This must be done in an empty but previously upgraded database. The user must be the first user in the system. It's user role is 'NORMAL' and id must be 1 (automatically set up by next val -function in the db).
10.  In web/.env.local, set VUE_APP_GITHUB_CLIENT_ID if you wanna use GitHub-based login/signup – the developer team will provide this for you.
11. Also, please see that all other environment keys are supplied, as some missing ones might make the system crash if not added.

When the application is running, you should find the application running on **localhost:8080**. The web frontend (a Vue.js app) can be found on the root url (localhost:8080/) and the API on localhost:8080/api. The API's visual documentation (Swagger UI) can be found on localhost:8080/api/ui/#/.

Great! Now you can start developing! Both the api and web services should reload automatically when changes are made.

Please see [a terminal recording](documentation/img/docker-compose-up.svg) of a successful setup.

### Halting Containers, Teardown

All the running (composed) containers can be halted with command `docker-compose down`.
You can remove previously built containers and volumes by executing `docker system prune -a` and `docker volume prune`. This is useful 

### Staging Installation

Our staging installation is half automated. When commit is noticed on the master branch, **drone.io** starts building new images for web and api, and these are then pushed **quay.io**. After these have finished, you will need to manually start the update process in the **portainer.io** service for the web and api services. If the new commits contain migrations, you will need to run them through the shell found at portainer.io. Documentation found [here](https://github.com/NatLibFi/Finto-suggestions/blob/master/documentation/HOWTO_update_and_fresh_install.md).

### Production Installation

Production installation will be automated in the same way as the staging environment – documentation found [here](https://github.com/NatLibFi/Finto-suggestions/blob/master/documentation/HOWTO_update_and_fresh_install.md).

### Development Workflow

Both the API and frontend can be developed simultaneously. All the changes to the code should update automatically without refreshing the browser or restarting the container.

### Frontend

The frontend is initialized with **vue-cli** (https://github.com/vuejs/vue-cli).

To add new dependencies, use `npm install package-name` or `npm install package-name --save-dev`. Afterwards, you will need to rebuild the containers by running `docker-compose build web`. You can also modify the package.json to add dependencies and make version updates.

The frontend can be run locally without Docker, too. Run `npm install` in the /web directory to install the required dependencies. Afterwards, you can start the development server by running `npm run serve`.

You will need [**node**](https://nodejs.org/en/download/) installed on your computer to use npm.

### Backend (API)

Our backend (API) is a simple Python webapp. Dependency management is handled by a Pipenv virtual environment.

Add new dependencies by running `pipenv install package-name` or `npm install package-name --dev` on your own computer (to update the Pipfile and Pipfile.lock). Afterwards, rebuild the api container `docker-compose build api` so that the changes are also installed within the containers. You need to have Python 3 and pipenv installed to do this locally.

#### Backend Commands

| **command**     | **description**                                                                                                       | **example**                                           |
|-----------------|-----------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| start           | Starts the Docker containers (docker-compose up)                                                                      | pipenv run start                                      |
| psql            | Opens a psql console within the db container                                                                          | pipenv run psql                                       |
| shell           | Opens an interactive Python shell within the api container. Flask context is automatically available.                 | pipenv run shell                                      |
| prune           | Prunes all blacklisted (/logout) access tokens. This should be run occasionally to keep the database clean.           | pipenv run prune                                      |
| test            | Runs Python API tests.                                                                                                | pipenv run test                                       |
| start-db        | Starts the database container.                                                                                        | pipenv run start-db                                   |
| migrate-db      | Creates a new Alembic migration file.                                                                                 | pipenv run migrate-db                                 |
| upgrade-db      | Upgrades the database (to the next migration version).                                                                | pipenv run upgrade-db                                 |
| downgrade-db    | Downgrades the database (to the previous migration version).                                                          | pipenv run downgrade-db                               |                          |
| proddata-import | Imports all old issues from github repository. You can limit how many rounds will it fetch by arguments loop-count=10 | pipenv run proddata-import                                       |

See [examples](documentation/examples.md) for additional tips and examples for development.

#### Database (migrations, accessing container etc.)

The database container runs a vendor Postgres Docker image on top of an Alpine container. Upon fresh installation, the database is initialized (currently) based on three environment variables set in .env file:

- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB

SQLAlchemy is used as an ORM for creating the database tables and further Flask-migrate (based on [Alembic](https://alembic.sqlalchemy.org/en/latest/)) is used for migrations.

Whenever you make changes to the database layout, a new migration needs to be created (check [Flask-migrate docs](https://flask-migrate.readthedocs.io/en/latest/)). Run `pipenv run migrate-db` in the project's **api** directory to automatically create a new migration file. Before upgrading the database, it's good practise to verify the migration file in the **migrations/versions** directory. Sometimes the migration file's content is not created automatically, as Flask-migrate does not notice any changes. Then you'll have to manually edit the file to include the migration changes you want.

After creating a new migration file, upgrade the database by running `pipenv run upgrade-db`.

In case you'd rather downgrade to a previous migration, run `pipenv run downgrade-db` and remove the latest migration file from **migrations/versions**.

Recording of an example migration / upgrade [here](documentation/img/migrate-and-upgrade.svg).

**You can access a psql prompt** with a command `pipenv run psql` (See Pipfile -- unfortunately it doesn't use environmental variables for login credentials at this point).

See the animation on using psql [here](documentation/img/pipenv-psql.svg).

### Continous deployment and git strategy

Our strategy for using version control is that the **master** branch handles the latest staging and production versions while the development features/fixes managed in the **develop** branch.

New features are created as feature or fix branches (**feature-<some_task>** or **fix-<some_task>**). When the feature is ready, a pull request is created that targets to the **develop** branch. After the develop branch has been tested locally, the branch is merged to the **master** branch. Changes to the master are automatically detected, and a new image is then built based on the updated master for the testing environment. When testing at the staging environment has been completed, the production version can be created.

The continous deployment flow service works semi-automatically. The service listens to commits on the **master** branch, and when a commit is pushed, it pulls the new version and builds the **api** and **web** images. Then it pushes them to **quay**: you have to add them by hand in the **portainer** service to use newest images for staging or production. See the flow graph underneath:

git: master/push -> drone.io -> pull git -> build -> push to quay

portainer: pull the newest image with tag:staging -> shut down the containers -> start the newest container with the newest image (this has to be made by the user)

### Bugs and quirks

**pytest**

Occasionally **pytest** isn't installed on the system when building the docker containers:

> OCI runtime exec failed: exec failed: container_linux.go:348: starting container process caused "exec: \"pytest\": executable file not found in $PATH": unknown

In that case, you'll need to install it manually in order to run tests: `docker-compose exec api pip install pytest`.

**sudo**

Sometimes when using Linux, you'll have to use the sudo command with all the commands or setup your local security priviledges. For example, you might have to use: `sudo npm install` instead of `npm install`.
