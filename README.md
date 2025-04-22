# 10b [Individual/Pairs/Group] Migrate from One Database to Another

**Type**: Individual/Pairs/Group

You are allowed to work in pairs or groups of three for this assignment if you find that easier and less work.

Create a migration script that migrates data from one database to another. You can choose any two databases you like. They can be different paradigms or even the same paradigm.



## Initial setup

```bash
$ poetry init -n
$ poetry add alembic sqlalchemy mysqlclient psycopg2-binary python-dotenv
$ poetry run alembic init alembic
$ poetry shell
```

Update the `alembic.ini` with the database connection information. Example for MySQL:


If you are connecting to MySQL in Docker, ensure the mysqlclient library is properly installed and configured. Remember to have the mysql database running from the docker-compose.yaml file. 
Set the alembic.ini file like this to have alembic interact with the MySQL database:

```ini
sqlalchemy.url = mysql+mysqldb://root:rootpassword@127.0.0.1:3305/mydatabase
```

Or if you want to have Alembic interact with the Postgres Database:
```ini
sqlalchemy.url = postgresql+psycopg2://root:rootpassword@127.0.0.1:5432/mydatabase
```

### Creating a migration

```bash
$ alembic revision -m "suitable name for the migration"
```

Update the file that was generated within the `alembic\versions` with the migration codeto set up and take down this migration:

### Running the migration

```bash
$ alembic upgrade head
```

Rollback the migration:

```bash
$ alembic downgrade -1
```

---

### **Docker and Docker-Compose Commands**

- **Start the MySQL container in detached mode:**
```bash
$ docker-compose up -d
```

- **Rebuild the containers after making changes to the `docker-compose.yaml` file:**
```bash
$ docker-compose up -d --build
```

- **top the running containers:**
```bash
$ docker-compose down
```

- **Stop the running containers and remove associated volumes:**
```bash
$ docker-compose down -v
```

- **Connect to the MySQL database from within the container:**
```bash
$ docker exec -it mysql_database mysql -u root -prootpassword -D mydatabase
```
  - <details>
    <summary>Click to view MySQL CLI Commands</summary>

    1. **See All Databases**
    ```mysql
    SHOW DATABASES;
    ```
  
    2. **Select a Specific Database**
    ```mysql
    USE mydatabase;
    ```
  
    3. **See all Tables in the Selected Database**
    ```mysql
    SHOW TABLES;
    ```
  
    4. **Select All Rows from a Specifik Table**
    ```mysql
    SELECT * FROM table_name;
    ```
  
    5. **Exit the MySQL CLI**
    ```mysql
    EXIT;
    ```
  </details>

- **Connect to the Postgres database from within the container:**
```bash
$ docker exec -it postgresql_database psql -U root -d mydatabase
```
  - <details>
    <summary>Click to view Postgres CLI Commands</summary>

    1. **See All Databases**
    ```sql
    \l
    ```

    2. **Select a Specific Database**
    ```sql
    \c mydatabase
    ```

    3. **See All Tables in the Selected Database**
    ```sql
    \dt
    ```

    4. **Select All Rows from a Specific Table**
    ```sql
    SELECT * FROM table_name;
    ```

    5. **Exit the PostgreSQL CLI**
    ```sql
    \q
    ```
  </details>


## How to migrate data from one database to another

To migrate data from one database to another, follow one of these two guides.

### Migrate MySQL Database to the Postgres Database

<details>
  <summary>Migrate MySQL to Postgres</summary>

  <br>
  
  **1. Start the Docker Containers**
      
  Ensure the databases are running by starting the Docker containers:
  ```bash
  $ docker-compose up -d
  ```
    
  If the Docker containers are already running, reset the databases:
  ```bash
  $ docker-compose down -v
  ```
  
  **2. Set the MySQL Database up using Alembic**
    
  Make certain that the [`alembic.ini`](alembic.ini#L66) has the `sqlalchemy.url` set to be equal to the MySQL Connection URL:
  ```ini
  sqlalchemy.url = mysql+mysqldb://root:rootpassword@127.0.0.1:3305/mydatabase
  ```
    
  Run the Alembic upgrade command to set the MySQL database up, make certain that the MySQL Database container is ready to connect:
  ```bash
  $ poetry run alembic upgrade head
  ```

  Optional, check the MySQL database container has tables with data:
  ```bash
  $ docker exec -it mysql_database mysql -u root -prootpassword -D mydatabase
  ```

  **3. Migrate the data using the migrate_data.py script**

  Set up the [`migrate_data.py`](migrate_data.py#L51-52) script to have the MySQL URL set as the Source Database URL and the Postgres URL set as the Target Database URL:
  ```python
  source_db_url = MYSQL_URL
  target_db_url = POSTGRES_URL
  ```

  Run the [`migrate_data.py`](migrate_data.py) script:
  ```bash
  $ poetry run python migrate_data.py
  ```

  Optional, enter the postgresql_database container and see that the same data is within the Postgres Database as there is within the MySQL Database:
  ```bash
  $ docker exec -it postgresql_database psql -U root -d mydatabase
  ```

</details>



### Migrate Postgres Database to the MySQL Database

<details>
  <summary>Migrate Postgres to MySQL</summary>

  <br>
  
  **1. Start the Docker Containers**
      
  Ensure the databases are running by starting the Docker containers:
  ```bash
  $ docker-compose up -d
  ```
    
  If the Docker containers are already running, reset the databases:
  ```bash
  $ docker-compose down -v
  ```
  
  **2. Set the Postgres Database up using Alembic**
    
  Make certain that the [`alembic.ini`](alembic.ini#L66) has the `sqlalchemy.url` set to be equal to the Postgres Connection URL:
  ```ini
  sqlalchemy.url = postgresql+psycopg2://root:rootpassword@127.0.0.1:5432/mydatabase
  ```
    
  Run the Alembic upgrade command to set the Postgres database up, make certain that the Postgres Database container is ready to connect:
  ```bash
  $ poetry run alembic upgrade head
  ```

  Optional, check the Postgres database container has tables with data:
  ```bash
  $ docker exec -it postgresql_database psql -U root -d mydatabase
  ```

  **3. Migrate the data using the migrate_data.py script**

  Set up the [`migrate_data.py`](migrate_data.py#L51-52) script to have the Postgres URL set as the Source Database URL and the MySQL URL set as the Target Database URL:
  ```python
  source_db_url = POSTGRES_URL
  target_db_url = MYSQL_URL
  ```

  Run the [`migrate_data.py`](migrate_data.py) script:
  ```bash
  $ poetry run python migrate_data.py
  ```

  Optional, enter the mysql_database container and see that the same data is within the MySQL Database as there is within the Postgres Database:
  ```bash
  $ docker exec -it mysql_database mysql -u root -prootpassword -D mydatabase
  ```

</details>

