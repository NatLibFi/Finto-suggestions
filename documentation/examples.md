
### Installing Development Environment

Run `docker-compose up` in project's **root** directory.

**First installation (docker-compose up)**

<p align="center">
    <img src="https://cdn.rawgit.com/NatLibFi/Finto-suggestions/master/documentation/img/docker-compose-up.svg">
</p>


For database migrations, run `pipenv run migrate-db` in project's **api** directory. This is only needed if changes have been made to the database models (models.py).
After migration, upgrade database by running `pipenv run upgrade-db`


**Database Migration and Upgrade**

<p align="center">
    <img src="https://cdn.rawgit.com/NatLibFi/Finto-suggestions/master/documentation/img/migrate-and-upgrade.svg">
</p>

**
