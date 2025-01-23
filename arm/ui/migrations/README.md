# ARM Flask-Alembic Help File

## Info

Generic single-database configuration
Whilst ARM supports MYSQL and SQLite, the default is MYSQL with SQLite only supported for migration
The default bind is against the MYSQL config

ARM uses [Flask-Alembic](https://flask-alembic.readthedocs.io/en/latest/use/), see the docs for more information.

Alembic documentation
- https://alembic.sqlalchemy.org/en/latest/

## Getting status
General status on the database
Run the below from the `/opt/arm/arm` folder

```bash
flash db show
```

## Adding to the database

Add a database migration, move to the below folder
Run the below from the `/opt/arm/arm` folder

`flask db migrate -m "description of the migration"`

## Resolving merge conflicts

If following multiple merges, sometimes there may be two database heads that need resolving.

```bash
flash db status
ERROR [flask_migrate] Error: Multiple head revisions are present for given argument 'head'; please specify a specific target revision, '<branchname>@head' to narrow to a specific head, or 'heads' for all heads
```

```bash
flask db heads
[2024-11-26 20:25:34,187] DEBUG ARM: __init__.create_app Starting ARM in [production] mode
[2024-11-26 20:25:34,187] DEBUG ARM: __init__.create_app Debugging pin: 12345
[2024-11-26 20:25:34,187] DEBUG ARM: __init__.create_app Mysql configuration: mysql+mysqlconnector://arm:*******@127.0.0.1/arm?charset=utf8mb4
[2024-11-26 20:25:34,187] DEBUG ARM: __init__.create_app SQLite Configuration: sqlite:////home/arm/db/arm.db
[2024-11-26 20:25:34,187] DEBUG ARM: __init__.create_app Login Disabled: True
[2024-11-26 20:25:34,187] INFO ARM: __init__.create_app Starting ARM UI on interface address - 127.0.0.1:5000
[2024-11-26 20:25:34,187] INFO ARM: __init__.create_app Setting log level to: DEBUG
[2024-11-26 20:25:34,221] DEBUG ARM: __init__.create_app Alembic Migration Folder: /opt/arm/arm/ui/migrations
6870a5546912 (head)
fa70591aea9e (head)
```

The two heads to merge are `6870a5546912 (head)` and `fa70591aea9e (head)`

Merge with the following command

```bash
flask db merge -m "merge 687 and fa7" 6870a5546912 fa70591aea9e
```

>!Note
> Due to the way Flask works, the above commands may not run as Flask-Alembic calls waitress
> Comment out the ui/__init__.py lines from "with app.app_context():" to just before "return app"