# Tips and Examples (for development)


#### Shell (and scripts) inside a Docker Container

Sometimes you would probably like to debug a thing or two inside the container, or perhaps run a script inside a container.

> Opening a shell inside an Alpine container: `docker-compose exec {container-name} /bin/sh`. Change {container-name} a container of desire: *api*, *db*, *web*, *nginx*.

> Executing a script in a container works the same way: `docker-compose exec {container-name} {my script}`. The *migrate-db* script calls the *flask* command inside the *api* container this way, for example.

#### General Docker tips

Sometimes you want to build all containers from scratch (including the database volume).

> 1. Stop all running containers: `docker-compose stop`
> 2. (Optional) Find the name of the (named) db volume: `docker volume ls`. The name is probably something like *finto-suggestions_volume_db*.
> 3. (Optional) Remove the volume `docker volume rm {volume-name}`.
> 4. Rebuild the containers `docker-compose build`.

> Delete all containers `docker rm $(docker ps -a -q) `

> Delete all volumes `docker volume rm $(docker volume ls -qf dangling=true)`

> Remove all images `docker rmi $(docker images -q)`. This is only useful to free some space from the drive.

#### Working with Flask shell

Flask offers a nifty shell for debugging. You can start a Python shell initialized with Flask context and database models within the api container by using the command `pipenv run shell` (alternatively `docker-compose exec api flask shell`).

The Flask shell has the Flask available and database models already initialized and imported, so twiddling with the SQLAlchemy ORM is quite easy this way. For example adding a User this way is easy:

```
$ pipenv run shell

Python 3.7.0 (default, Aug  4 2018, 02:41:57)
[GCC 6.4.0] on linux
App: app [production]
Instance: /app/instance
>>>
>>> u = models.User(name='Peter', email='peter@test.com', password='password', role=models.UserRoles.ADMIN)
>>> db.session.add(u)
>>> db.session.commit()
>>>
>>> db
>>> models.User.query.all()
[<User Peter>]
```

#### Working with database

You can use the psql cli to access the database the traditional way: `pipenv run psql`.
See an example terminal recording [here](documentation/img/pipenv-psql.svg).

For quickly dropping the database tables, you can call:
> `docker-compose exec db psql devdb -Udevuser -c "DROP OWNED BY devuser;"`. Modify credentials accordingly.
Run an upgrade after this to reinitialize: `pipenv run upgrade-db`.


#### Bugs and issues

Alembic doesn't properly support downgrading PostgreSQL ENUM types, which might occasionally cause an error. In this case you might need to drop enum types from the database manually. Do as follows:

1. `pipenv run psql`
2. `\dT` to list (enum) types
3. `drop type {typename}` to drop a type

