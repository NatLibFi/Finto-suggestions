
### Installing Development Environment

Run `docker-compose up` in project's **root** directory.

**First installation (docker-compose up)**

![docker-compose up](img/docker-compose-up.svg)

For database migrations, run `pipenv run migrate-db` in project's **api** directory. This is only needed if changes have been made to the database models (models.py).
After migration, upgrade database by running `pipenv run upgrade-db`


**Database Migration and Upgrade**

![docker-compose migrate-db && docker-compose upgrade-db](img/migrate-and-upgrade.svg)

**